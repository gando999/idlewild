import os

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

setup_logging()

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

# Load the file
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Build the schema
schema = parse_and_build_idl_file(
    os.path.join(__location__, 'starwars.graphqls'),
    resolver_mappings=datafetchers,
    interface_resolver_mappings=interface_resolvers,
)

StarWarsSchema = schema
