from collections import namedtuple

Human = namedtuple('Human', 'id name friends appearsIn homePlanet')

# EPISODE
# 0 -> Star Wars
# 1 -> Empire Strikes Back
# 2 -> Return of the Jedi


luke = Human(
    id='1000',
    name='Luke Skywalker',
    friends=['1002', '1003', '2000', '2001'],
    appearsIn=[0, 1, 2],
    homePlanet='Tatooine',
)

vader = Human(
    id='1001',
    name='Darth Vader',
    friends=['1004'],
    appearsIn=[0, 1, 2],
    homePlanet='Tatooine',
)

han = Human(
    id='1002',
    name='Han Solo',
    friends=['1000', '1003', '2001'],
    appearsIn=[0, 1, 2],
    homePlanet=None,
)

leia = Human(
    id='1003',
    name='Leia Organa',
    friends=['1000', '1002', '2000', '2001'],
    appearsIn=[0, 1, 2],
    homePlanet='Alderaan',
)

tarkin = Human(
    id='1004',
    name='Wilhuff Tarkin',
    friends=['1001'],
    appearsIn=[0],
    homePlanet=None,
)

humanData = {
    '1000': luke,
    '1001': vader,
    '1002': han,
    '1003': leia,
    '1004': tarkin,
}

Droid = namedtuple('Droid', 'id name friends appearsIn primaryFunction')

threepio = Droid(
    id='2000',
    name='C-3PO',
    friends=['1000', '1002', '1003', '2001'],
    appearsIn=[0, 1, 2],
    primaryFunction='Protocol',
)

artoo = Droid(
    id='2001',
    name='R2-D2',
    friends=['1000', '1002', '1003'],
    appearsIn=[0, 1, 2],
    primaryFunction='Astromech',
)

droidData = {
    '2000': threepio,
    '2001': artoo,
}


def get_character(id):
    return humanData.get(id) or droidData.get(id)


def get_friends(character):
    return map(get_character, character.friends)


def get_hero(episode):
    if episode == 1:
        return luke
    return artoo


def get_human(id):
    return humanData.get(id)


def get_droid(id):
    return droidData.get(id)
