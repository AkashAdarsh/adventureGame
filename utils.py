from constants import VALID_EXITS, SUPPORTED_VERBS, VERBS_THAT_REQUIRE_ARG


def go_processor(*args):
    rest, directions = args[0], args[1]
    if directions is None:
        directions = []
    if rest is None:
        rest = []
    if not len(rest):
        print("Sorry, you need to 'go' somewhere.")
        return None
    to_go = rest[0].lower()
    if len(rest) > 1 or to_go not in VALID_EXITS:
        print('Enter a valid exit!')
        return None
    if to_go not in directions:
        print(f"There's no way to go {to_go}")
        return None
    return to_go


def get_processor(*args):
    rest, items = args[0], args[2]
    if rest is None:
        rest = []
    if items is None:
        items = []
    if len(rest) <= 0:
        print("Sorry, you need to 'get' something")
        return None
    if len(rest) > 1:
        print('Enter a single item!')
        return None
    item_to_get = rest[0].lower()
    if item_to_get not in items:
        print("There's no {item} anywhere.".format(item=item_to_get))
        return None
    print(f"You pick up the {item_to_get}")
    return item_to_get


def inventory_processor(*args):
    inventory = args[3]
    if not len(inventory):
        print("You're not carrying anything")
        return None
    print('Inventory:\n  {items}'.format(items='\n  '.join(inventory)))


def look_processor(*args):
    pass


def help_processor(*args):
    verbs = []
    for verb in list(SUPPORTED_VERBS.values()):
        text = f"{verb}"
        if verb in VERBS_THAT_REQUIRE_ARG:
            text += ' ...'
        verbs.append(text)
    print("You can run the following commands:\n{verbs}\n".format(verbs='\n'.join(verbs)))


def drop_processor(*args):
    rest, inventory = args[0], args[3]
    if rest is None:
        rest = []
    if inventory is None:
        inventory = []
    if len(rest) <= 0:
        print("Sorry, you need to 'drop' something")
        return None
    if len(rest) > 1:
        print('Enter a single item!')
        return None
    item_to_drop = rest[0].lower()
    if item_to_drop not in inventory:
        print("There's no {item} in your inventory.".format(item=item_to_drop))
        return None
    print(f"You drop the {item_to_drop}")
    return item_to_drop


verb_processors = {
    SUPPORTED_VERBS['GO']: go_processor,
    SUPPORTED_VERBS['LOOK']: look_processor,
    SUPPORTED_VERBS['GET']: get_processor,
    SUPPORTED_VERBS['INVENTORY']: inventory_processor,
    SUPPORTED_VERBS['HELP']: help_processor,
    SUPPORTED_VERBS['DROP']: drop_processor
}
