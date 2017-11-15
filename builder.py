from collections import OrderedDict

from graphql import (
    graphql,
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
    GraphQLEnumType,
)

from graphql.type.definition import GraphQLEnumValue

#schema = GraphQLSchema(
#  query= GraphQLObjectType(
#    name='RootQueryType',
#    fields={
#      'hello': GraphQLField(
#        type= GraphQLString,
#        resolver=lambda *_: 'world'
#      )
#    }
#  )
#)

class Builder:

    def __init__(self):
        self.types = {}
        self.enums = {}
        self.interfaces = {}

    def build(self, items):
        for item in items:
            self.eval(item)

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
        print('Registered ENUM {}'.format(enum))

    def register_interface(self, item):
        _, interface_name, interface_fields = item 

        #for field in interface_fields:
        #    self._build_field(field)

        #interface = GraphQLInterfaceType(
        #    name=interface_name
        print('Registered INTERFACE {}'.format(interface_name))

    def register_type(self, item):
        print('Got TYPE')

    def register_schemadef(self, item):
        print('Got SCHEMADEF')
