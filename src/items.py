import json
# import jsonschema
from pathlib import Path

#TODO: probably change this to be found inside of project settings file or something, in case of restructuring
ITEMS_PATH = Path(__file__).parent.parent / "data" / "items"

class Item:
    def __init__(self, name: str, description: str, needs_recipient: bool = False) -> None:
        #TODO: add weight
        self.name: str = name
        self.description: str = description
        self.needs_recipient: bool = needs_recipient

        self.fail_message: str = ""

    def try_use(self, recipient: str, player, world) -> bool:
        if self.needs_recipient and recipient == '':
            self.fail_message = "This item requires a recipient."
            return False
        if not self.needs_recipient and recipient:
            self.fail_message = "This item does not require a recipient."
            return False
        return True

    def use(self, recipient: str, player, world) -> str:
        return ''
    
class Weapon(Item):
    def __init__(self, name: str,verb: str, description: str, stats: dict[str,float]):
        super().__init__(name, description, True)
        self.verb = verb
        self.stats = stats

    def use(self, recipient: str, player, world) -> str:
        if self.try_use(recipient, player, world):
            if recipient in world.state.get_room(player.current_room).entities:
                # TODO instead of just removing, make it so
                # that there is health and proper combat
                
                world.state.get_room(player.current_room).entities.remove(recipient)
                world.send_message_to_players_in_room(player, f"Player '{player.name}' stabs the {recipient}.", player.current_room)
                
                return f"You viciously {self.verb} the {recipient}."
            else:
                return f"There is no {recipient} here."
        return self.fail_message

WEAPONS: list[Weapon] = []
#consumables: list[Consumable] = []
#wearables: list[Wearable] = []

with open(ITEMS_PATH / "weapons.json") as f:
    data = json.load(f)

weapons_list = data["items"]

for w in weapons_list:
    WEAPONS.append(Weapon(
        w['name'],
        w['verb'],
        w['description'],
        w['stats']
    ))

def get_weapon_with_name(name: str) -> Weapon:
    for w in WEAPONS:
        if w.name.lower() == name.lower():
            return w
    
    return None

def get_item_with_name(name: str) -> Item:
    # TODO all three types
    return get_weapon_with_name(name)