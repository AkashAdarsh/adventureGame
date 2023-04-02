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
        room = self.rooms[self.current_room_id]
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
            self.has_user_quit = True
            return
        if verb in ABBREVIATED_EXITS:
            rest = [ABBREVIATED_EXITS[verb]]
            verb = SUPPORTED_VERBS['GO']
        directions = self.rooms[self.current_room_id].get('exits', {})
        items = self.rooms[self.current_room_id].get('items', [])
        return_value = verb_processors[verb](rest, directions, items, self.inventory)
        if verb == SUPPORTED_VERBS['GO'] and return_value:
            new_direction = return_value
            if new_direction in directions:
                print(f"You go {new_direction}.")
                self.current_room_id = directions[new_direction]
        if verb == SUPPORTED_VERBS['GET'] and return_value:
            item_to_get = return_value
            all_items = self.rooms[self.current_room_id].get('items', [])
            if len(all_items):
                rest_items = list(filter(lambda item: item != item_to_get, all_items))
                self.rooms[self.current_room_id]['items'] = copy.deepcopy(rest_items)
                self.inventory.append(item_to_get)
        if verb == SUPPORTED_VERBS['DROP'] and return_value:
            item_to_drop = return_value
            rem_items = list(filter(lambda item: item != item_to_drop, self.inventory))
            all_items = self.rooms[self.current_room_id].get('items', [])
            all_items.append(item_to_drop)
            self.rooms[self.current_room_id]['items'] = copy.deepcopy(all_items)
            self.inventory = copy.deepcopy(rem_items)
        self.last_typed_verb = verb

    def start_game(self):
        while not self.has_user_quit:
            if self.last_typed_verb not in [SUPPORTED_VERBS['GET'], SUPPORTED_VERBS['INVENTORY'],
                                            SUPPORTED_VERBS['QUIT'], SUPPORTED_VERBS['HELP']]:
                self.show_room_details()
            try:
                query = input('What would you like to do? ')
                is_valid_query = self.query_validator(query)
                if not is_valid_query:
                    print('Please enter a valid verb!!!\n')
                    continue
                self.query_processor(query)
            except EOFError:
                print("\nUse 'quit' to exit.")
                self.last_typed_verb = SUPPORTED_VERBS['QUIT']


def main():
    file_path = sys.argv[1]
    with open(file_path, 'r') as f:
        data = json.load(f)
        adventure = Adventure(data)
        if not adventure.validate_rooms(adventure):
            print('Invalid Map provided!!!')
            return
        adventure.start_game()


if __name__ == "__main__":
    main()
