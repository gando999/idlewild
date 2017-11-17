from graphql import graphql

from .starwars_schema import StarWarsSchema


def test_hero_name_query():
    query = '''
        query HeroNameQuery {
          hero {
            name
          }
        }
    '''
    expected = {
        'hero': {
            'name': 'R2-D2'
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_hero_name_and_friends_query():
    query = '''
        query HeroNameAndFriendsQuery {
          hero {
            id
            name
            friends {
              name
            }
          }
        }
    '''
    expected = {
        'hero': {
            'id': '2001',
            'name': 'R2-D2',
            'friends': [
                {'name': 'Luke Skywalker'},
                {'name': 'Han Solo'},
                {'name': 'Leia Organa'},
            ]
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected
