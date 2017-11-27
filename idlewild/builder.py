from collections import OrderedDict
import logging

from graphql import (
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
    GraphQLEnumType,
    GraphQLInt,
    GraphQLFloat,
    GraphQLBoolean,
    GraphQLID,
    GraphQLNonNull,
    GraphQLList,
    GraphQLArgument,
)

from graphql.type.definition import (
    GraphQLEnumValue,
    GraphQLInterfaceType,
)

GRAPHQL_SCALARS = {
    'Int': GraphQLInt,
    'Float': GraphQLFloat,
    'String': GraphQLString,
    'Boolean': GraphQLBoolean,
    'ID': GraphQLID
}


LOGGER = logging.getLogger("idlewild")


class UnregisteredError(Exception):
    pass


class SchemaMappingsInvalid(Exception):
    pass


class Builder:

    def __init__(
            self, resolver_map=None,
            interface_resolver_map=None):
        self.types = {}
        self.enums = {}
        self.interfaces = {}
        self.schema = None
        self.resolver_map = (
            resolver_map
            if resolver_map is not None else {}
        )
        self.interface_resolver_map = (
            interface_resolver_map
            if interface_resolver_map is not None else {}
        )

    def build(self, items):
        root = None  # root has to be last
        for item in items:
            item_id, *_ = item
            if item_id == 'SCHEMADEF':
                root = item
            else:
                self.eval(item)
        self.eval(root)

    def eval(self, item):
        item_id, *_ = item
        if item_id == 'TYPE':
            return self.register_type(item)
        if item_id == 'INTERFACE':
            return self.register_interface(item)
        if item_id == 'ENUM':
            return self.register_enum(item)
        if item_id == 'SCHEMADEF':
            return self.register_schemadef(item)
        raise ValueError(
            'item {} did was not correctly defined'.format(item)
        )

    def register_enum(self, item):
        _, enum_name, enum_values = item

        def create_values(enum_values):
            value_dict = OrderedDict()
            for count, name in list(enumerate(enum_values)):
                value_dict[name] = GraphQLEnumValue(count)
            return value_dict

        enum = GraphQLEnumType(
            name=enum_name,
            values=create_values(enum_values)
        )

        self.enums[enum_name] = enum
        LOGGER.info('Registered ENUM {}'.format(enum_name))

    def _resolve_base_type(self, type_ref):
        base_type = {
            **GRAPHQL_SCALARS,
            **self.types,
            **self.interfaces,
            **self.enums,
            **self.interfaces}.get(type_ref)
        if base_type is None:
            LOGGER.error('Could not resolve {}'.format(type_ref))
            raise UnregisteredError
        return base_type

    def _extract_type_info(self, field_type_info):
        is_list, type_info = field_type_info
        _, is_nullable, type_ref = type_info
        return is_list, is_nullable, type_ref

    def _build_field_type(self, field_type_info):
        is_list, is_nullable, type_ref = (
            self._extract_type_info(field_type_info)
        )
        base_type = self._resolve_base_type(type_ref)

        if is_nullable == 'NON-NULLABLE':
            base_type = GraphQLNonNull(base_type)
        if is_list == 'GRAPHQL_LIST':
            base_type = GraphQLList(base_type)
        if is_list == 'GRAPHQL_NON-NULLABLE_LIST':
            base_type = GraphQLNonNull(GraphQLList(base_type))

        return base_type

    def _build_args(self, args_list):
        target_args = []
        for arg in args_list:
            name_and_args, field_type_info = arg
            _, name, *_ = name_and_args
            target_args.append(
                (name, GraphQLArgument(
                    self._build_field_type(field_type_info)
                 )))
        return dict(target_args)

    def _build_fields(self, fields):
        target_fields = []
        for field in fields:
            name_and_args, field_type_info = field
            _, name, _, args_list = name_and_args
            target_fields.append(
                (name, GraphQLField(
                    self._build_field_type(field_type_info),
                    args=self._build_args(args_list),
                    resolver=self.resolver_map.get(name),
                 )))
        return dict(target_fields)

    def register_interface(self, item):
        _, interface_name, interface_fields = item

        interface = GraphQLInterfaceType(
            name=interface_name,
            fields=lambda: dict(self._build_fields(interface_fields)),
            resolve_type=lambda x, y: self._resolve_base_type(
                self.interface_resolver_map.get(interface_name)(x, y)
            )
        )

        self.interfaces[interface_name] = interface
        LOGGER.info('Registered INTERFACE {}'.format(interface_name))

    def register_type(self, item):
        _, type_name, implements, field_list = item

        target_type = GraphQLObjectType(
            name=type_name,
            fields=lambda: self._build_fields(field_list),
            interfaces=lambda: (
                (self._resolve_base_type(implements),)
                if implements else None
             )
        )
        self.types[type_name] = target_type
        LOGGER.info('Registered TYPE {}'.format(type_name))

    def register_schemadef(self, item):
        _, _, definition_list = item  # TODO: tidy this
        query_type_map = {}
        for definition in definition_list:
            root_id_info, root_type_info = definition
            _, query_type, *_ = root_id_info  # query or mutation
            _, root_item_info = root_type_info
            _, root_name = root_type_info
            _, _, root_target = root_name
            query_type_map[query_type] = self._resolve_base_type(root_target)
            LOGGER.info(
                'Registered ROOT [{}] of {}'.format(query_type, root_target)
            )
        self.schema = GraphQLSchema(
            **query_type_map
        )
        LOGGER.info('Created ROOT schema')
