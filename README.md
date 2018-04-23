[![PyPI version](https://badge.fury.io/py/idlewild.svg)](https://badge.fury.io/py/idlewild)

Idlewild
=======

Use the amazing Python PLY library to parse GraphQL IDL into a schema.

### Purpose

Idlewild is a Python library for creating GraphQL schemas from GraphQL IDL format. Optionally it also allows you to register data fetchers for fields and these can be implemented in your own application.

It was inspired by a similar idea in JVM called [graphql-java-tools](https://github.com/graphql-java/graphql-java-tools).

It is very small and consists of a parser, builder and tools module. The parser uses PLY to build a simple grammar which the builder turns into a GraphQL schema using [graphql-core](https://github.com/graphql-python/graphql-core).

As stated on [graphql-core](https://github.com/graphql-python/graphql-core):

* An overview of the GraphQL language is available in the [README](https://github.com/facebook/graphql/blob/master/README.md) for the [Specification for GraphQL](https://github.com/facebook/graphql).

* Examples can be found in [tests](https://github.com/gando999/idlewild/tree/master/tests) in this repository.


### Concepts


To build a schema, we need only a schema definition in this [form](http://graphql.org/learn/schema):

    schema {
        query: QueryType
    }

    type QueryType {
        hero(episode: Episode): Character
        human(id : String) : Human
        droid(id: ID!): Droid
    }

    ...

At the time of building the schema we can attach data fetchers or type resolvers to fields.

    from idlewild.schematools import (
        parse_and_build_idl_file,
        setup_logging
    )

    from .fixtures import (
       get_hero,
       get_human,
       get_droid,
       get_friends,
    )

    datafetchers = {
        'human': lambda human, info, **args: get_human(args['id']),
        'droid': lambda droid, info, **args: get_droid(args['id']),
        'hero': lambda root, info, **args: get_hero(args.get('episode')),
        'friends': lambda character, *_: get_friends(character),
    }

    interface_resolvers = {
        'Character': lambda character, info: (
            'Human' if get_human(character.id) else 'Droid'
         )
    }

    # Build the schema
    schema = parse_and_build_idl_file(
        'starwars.graphqls',
        resolver_mappings=datafetchers,
        interface_resolver_mappings=interface_resolvers,
    )

    StarWarsSchema = schema
