import pytest

from graphql import (
    GraphQLEnumType,
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
)

from idlewild.builder import Builder


@pytest.fixture
def plain_builder():
    return Builder()


@pytest.fixture
def generic_graphql_field():
    return GraphQLField(type=GraphQLString)


@pytest.fixture
def generic_graphql_object(generic_graphql_field):
    return GraphQLObjectType(
        'foo', fields={'bar': generic_graphql_field}
    )


@pytest.fixture
def field_query_args():
    return ('FIELD', 'query', 'ARGS', [])


@pytest.fixture
def field_atom_nullable_querytype():
    return (
        'GRAPHQL_ATOM', ('GRAPHQL_TYPE', 'NULLABLE', 'QueryType')
    )


@pytest.fixture
def field_atom_nullable_stringtype():
    return (
        'GRAPHQL_ATOM', ('GRAPHQL_TYPE', 'NULLABLE', 'String')
    )


@pytest.fixture
def schemadef_node(field_query_args, field_atom_nullable_querytype):
    return (
        'SCHEMADEF', 'schema',
        [(field_query_args, field_atom_nullable_querytype)]
    )


@pytest.fixture
def type_node(field_query_args, field_atom_nullable_stringtype):
    return (
        'TYPE', 'Foo', 'Bar',
        [('FooBar', field_atom_nullable_stringtype)]
    )


@pytest.fixture
def enum_node():
    return (
        'ENUM', 'FooCategory',
        ['BarThing1', 'BarThing2']
    )


def test_schemadef(
        plain_builder, schemadef_node,
        generic_graphql_object, generic_graphql_field):

    plain_builder.types = {'QueryType': generic_graphql_object}
    plain_builder.build([schemadef_node])

    schema = plain_builder.schema
    query_type = schema.get_query_type()
    fields = query_type.fields

    assert fields['bar'] == generic_graphql_field


def test_type(
        plain_builder, type_node,
        schemadef_node, generic_graphql_object):

    plain_builder.types = {'QueryType': generic_graphql_object}
    plain_builder.build([schemadef_node, type_node])

    types = plain_builder.types

    assert 'Foo' in types
    foo_object = types['Foo']
    assert foo_object.name == 'Foo'

    assert 'QueryType' in types
    query_object = types['QueryType']
    assert query_object.name == 'foo'


def test_enum(
        plain_builder, enum_node,
        generic_graphql_object, schemadef_node):

    plain_builder.types = {'QueryType': generic_graphql_object}
    plain_builder.build([schemadef_node, enum_node])

    enums = plain_builder.enums

    assert 'FooCategory' in enums
    enum_object = enums['FooCategory']
    assert isinstance(enum_object, GraphQLEnumType)

    values = enum_object.values
    assert len(values) == 2

    names = [value.name for value in values]
    assert 'BarThing1' in names
    assert 'BarThing2' in names
