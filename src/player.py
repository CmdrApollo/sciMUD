from typing import Any
from commands import *
from colors import *

from constants import goodbye_message

import os
import json

nothing_message = colored("You do nothing.", yellow)
forbidden_words = ['to', 'on', 'a', 'an', 'the', 'for', 'towards', 'at', 'with']

def get_player_data(filename: str) -> dict[str, Any]:
    path = os.path.join('data', 'players', filename + '.json')

    if os.path.exists(path):
        return json.load(open(path))

    return {}

class EntityStatus:
    NONE = 1 << 0
    ONFIRE = 1 << 1
    FROZEN = 1 << 2
    UNDERWATER = 1 << 3
    ASLEEP = 1 << 4
    INTOXICATED = 1 << 5
    SHOCKED = 1 << 6
    BLIND = 1 << 7
    SICK = 1 << 8

class Player:
    def __init__(self, world) -> None:
        self.is_new_player = True

        self.potential_name = ""
        self.name = ""

        self.password = ""

        self.health = 10
        self.max_health = self.health

        self.magic = 10
        self.max_magic = self.magic

        self.temperature = 100
        self.max_temperature = self.temperature

        self.inventory = []

        self.just_started = True

        self.world = world

        self.current_room = world.state.global_rooms[0].name

        self.message_from_world = ""

        self.awaiting_password = True

        self.status = EntityStatus.NONE

    def save_to_file(self) -> None:
        data = {}
        
        data["name"] = self.name
        data["password"] = self.password

        data["health"] = self.health
        data["max_health"] = self.max_health
        
        data["magic"] = self.magic
        data["max_magic"] = self.max_magic
        
        data["temperature"] = self.temperature
        data["max_temperature"] = self.max_temperature

        data["current_room"] = self.current_room

        data["inventory"] = [i.name for i in self.inventory]
        
        with open(os.path.join('data', 'players', self.name + '.json'), 'w') as f:
            json.dump(data, f)
            
            f.close()

    def prompt(self) -> str:
        if self.just_started:
            self.just_started = False

            return "".join(["Welcome To\n\n",
            colored("  .=*888888888h.                  ", gray) + colored("    j&                                        \n", white),
            colored(" h8888888888888*            &h    ", gray) + colored("   j 8 j8h.  &8h.   &.     h.            &.   \n", white),
            colored("88h.                8             ", gray) + colored("  j* h8   *;8j ;88  h8     88            88   \n", white),
            colored("&8888888888888h.  .h        h     ", gray) + colored("j&*  h8    88   88  h8     88            88   \n", white),
            colored(" *8888888888888h jh8       8h          ", gray) + colored("j8    &h   &j  h8     88      j888h.88   \n", white),
            colored("              .hj*h!      j &.         ", gray) + colored("h8    h8  *8   h8     88    j=     888   \n", white),
            colored(".j8888888888888&  *88888=h  *88888h.   ", gray) + colored("h8    h8  88  j**;   j88   j*8    j888  j\n", white),
            colored("!8888888888888*    *88888*   *88888*   ", gray) + colored("&;    *&  *&=j*  *;8j**&==j  ;=&8j***&=j*\n", white),
            "\nEnter your character's name:\n"])
        else:
            if self.message_from_world:
                m = self.message_from_world
                self.message_from_world = ""
                return m
            return ""

    def parse(self, text: str) -> str:
        if not len(text):
            return nothing_message
        
        if self.name == "":
            if self.potential_name == "":
                self.potential_name = text.lower().strip().capitalize()
            
                return f"Is the name '{self.potential_name}' correct? (y/n)"
            else:
                match text.lower().strip():
                    case 'y':
                        self.name = self.potential_name

                        data = get_player_data(self.name)

                        if data:
                            self.name = data["name"]
                            self.password = data["password"]

                            self.health = data["health"]
                            self.max_health = data["max_health"]
                            
                            self.magic = data["magic"]
                            self.max_magic = data["max_magic"]
                            
                            self.temperature = data["temperature"]
                            self.max_temperature = data["max_temperature"]

                            self.current_room = data["current_room"]

                            self.inventory = [get_item_with_name(name) for name in data["inventory"]]

                            self.is_new_player = False
                            return f"Character with name {self.name} found! Please enter your password:"
                        else:
                            return f"Character with name {self.name} not found... Creating a new character. Please choose a password:"
                    case 'n':
                        self.potential_name = ''
                    case _:
                        self.potential_name = ''
                
                return "Enter your character's name:\n"
        
        if self.awaiting_password:
            if self.is_new_player:
                self.password = text.strip()

                self.world.send_message_to_players_in_room(self, f"Player '{self.name}' joins the game.", self.current_room)

                self.awaiting_password = False

                return f"Password set. Welcome to sciMUD! Including you, there are currently {len(self.world.players)} players active."
            else:
                if text.strip() == self.password:
                    self.world.send_message_to_players_in_room(self, f"Player '{self.name}' joins the game.", self.current_room)

                    self.awaiting_password = False

                    return f"Password correct. Welcome to sciMUD! Including you, there are currently {len(self.world.players)} players active."
                else:
                    return "Incorrect password. Please enter your password."
                
        stripped_text = text.lower().strip()

        if stripped_text == "quit":
            return goodbye_message

        for a in aliases:
            stripped_text = stripped_text.replace(a[0], a[1])

        verb, *args = stripped_text.split(' ')
        args = list(filter(lambda x: x not in forbidden_words, args))

        if verb in commands:
            self.command = commands[verb]
            if len(args) >= self.command.number_arguments:
                self.command.arguments = args
                r = self.command.process(self, self.world)
                self.save_to_file()
                return r
            else:
                return colored(f"Incorrect number of arguments. Expected (at least) {len(self.command.arguments)}.", red)
        else:
            return nothing_message