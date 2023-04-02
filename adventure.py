import copy
import sys
import json
from operator import itemgetter
from constants import IMP_ROOM_KEYS, SUPPORTED_VERBS, VALID_KEYWORDS, ABBREVIATED_EXITS
from utils import verb_processors


class Adventure:
    def __init__(self, rooms=None):
        if rooms is None:
            rooms = []
        self.rooms = rooms
        self.current_room_id = 0
        self.inventory = []
        self.has_user_quit = False
        self.last_typed_verb = ''

    def __getitem__(self, key):
        return self.__dict__[f"{key}"]

    def __setitem__(self, key, value):
        self.__dict__[f"{key}"] = value

    @staticmethod
    def validate_rooms(self):
        total_rooms = len(self.rooms)
        for room in self.rooms:
            fields = [str(i).lower() for i in room.keys()]
            necessary_keys_present = set(IMP_ROOM_KEYS).issubset(set(fields))
            if not necessary_keys_present:
                return False
            exits = room['exits']
            for i in list(exits.values()):
                if int(i) < 0 or int(i) >= total_rooms:
                    return False
        return True

    def show_room_details(self):
        current_room_id = self.__getitem__('current_room_id')
        rooms = self.__getitem__('rooms')
        room = rooms[current_room_id]
        name, desc, exits = itemgetter('name', 'desc', 'exits')(room)
        items = room.get('items', [])
        print("> {name}\n\n{desc}\n".format(name=name, desc=desc))
        if len(items):
            print("Items: {items}\n".format(items=' '.join(items)))
        print("Exits: {exits}\n".format(exits=' '.join(exits)))

    @staticmethod
    def query_validator(query=''):
        if not len(query):
            return False
        verb = query.lower().split(' ')[0]
        if verb in VALID_KEYWORDS or verb in ABBREVIATED_EXITS:
            return True

        return False

    def query_processor(self, query=''):
        words = query.strip().lower().split(' ')
        verb, rest = words[0], words[1:]
        if verb == SUPPORTED_VERBS['QUIT']:
            print("Goodbye!")
            self.__setitem__('has_user_quit', True)
            return
        if verb in ABBREVIATED_EXITS:
            rest = [ABBREVIATED_EXITS[verb]]
            verb = SUPPORTED_VERBS['GO']
        current_room_id = self.__getitem__('current_room_id')
        rooms = self.__getitem__('rooms')
        inventory = self.__getitem__('inventory')
        directions = rooms[current_room_id].get('exits', {})
        items = rooms[current_room_id].get('items', [])
        return_value = verb_processors[verb](rest, directions, items, inventory)
        if verb == SUPPORTED_VERBS['GO'] and return_value:
            new_direction = return_value
            if new_direction in directions:
                print(f"You go {new_direction}")
                self.__setitem__('current_room_id', directions[new_direction])
        if verb == SUPPORTED_VERBS['GET'] and return_value:
            item_to_get = return_value
            all_items = rooms[current_room_id].get('items', [])
            if len(all_items):
                rest_items = list(filter(lambda item: item != item_to_get, all_items))
                self.rooms[self.current_room_id]['items'] = copy.deepcopy(rest_items)
                inventory.append(item_to_get)
                self.__setitem__('inventory', inventory)
        if verb == SUPPORTED_VERBS['DROP'] and return_value:
            item_to_drop = return_value
            rem_items = list(filter(lambda item: item != item_to_drop, self.inventory))
            all_items = rooms[current_room_id].get('items', [])
            all_items.append(item_to_drop)
            self.rooms[self.current_room_id]['items'] = copy.deepcopy(all_items)
            self.__setitem__('inventory', copy.deepcopy(rem_items))