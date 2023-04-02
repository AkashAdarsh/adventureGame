import copy

IMP_ROOM_KEYS = ['name', 'desc', 'exits']
SUPPORTED_VERBS = {
    'GO': 'go',
    'GET': 'get',
    'LOOK': 'look',
    'INVENTORY': 'inventory',
    'QUIT': 'quit',
    'HELP': 'help',
    'DROP': 'drop'
}
VERBS_THAT_REQUIRE_ARG = [SUPPORTED_VERBS['GO'], SUPPORTED_VERBS['GET'], SUPPORTED_VERBS['DROP']]
VALID_KEYWORDS = copy.deepcopy(list(SUPPORTED_VERBS.values()))
VALID_EXITS = ['north', 'south', 'east', 'west', 'northeast', 'northwest', 'southeast', 'southwest']
ABBREVIATED_EXITS = {
    'n': 'north',
    's': 'south',
    'e': 'east',
    'w': 'west',
    'ne': 'northeast',
    'nw': 'northwest',
    'se': 'southeast',
    'sw': 'southwest'
}
