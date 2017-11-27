from graphql import graphql

from .starwars_mutation_schema import StarWarsSchema

# Tests from https://github.com/graphql-python/graphql-core


def test_hero_name_query():
    query = '''
        query HeroNameQuery {
          hero {
            id
            name
          }
        }
    '''
    expected = {
        'hero': {
            'id': '2001',
            'name': 'R2-D2'
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected

    mutation = '''
        mutation CharacterNameMutation {
            updateCharacterName(id: "2001", newName: "R3-D3") {
                id
                name
            }
        }
    '''
    expected = {
        'updateCharacterName': {
            'id': '2001',
            'name': 'R3-D3'
        }
    }
    result = graphql(StarWarsSchema, mutation)
    assert not result.errors
    assert result.data == expected
