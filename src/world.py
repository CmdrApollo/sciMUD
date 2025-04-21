from typing import Any
import os
import json

from rooms import Room
from player import Player
from commands import *

nothing_message = "You do nothing."
forbidden_words = ['to', 'on', 'a', 'an', 'the', 'for', 'towards', 'at', 'with']

class WorldState:
    def __init__(self) -> None:
        self.just_started = True

        self.player = Player()

        self.global_rooms = []

        with open(os.path.join("data", "rooms.json")) as f:
            data = json.load(f)

            for room in data["rooms"]:
                self.global_rooms.append(Room(room["name"], room["description"], room["items"], room["entities"], {
                    'north': room["north"],
                    'south': room["south"],
                    'east': room["east"],
                    'west': room["west"]
                }))
            
            f.close()

        self.current_room = self.global_rooms[0]
    
    def get_room(self, name: str) -> Room:
        for r in self.global_rooms:
            if r.name == name:
                return r
        
        return None

class World:
    def __init__(self) -> None:
        self.state: WorldState = WorldState()
        self.command: Command = None
    
    def prompt(self):
        if self.state.just_started:
            self.state.just_started = False

            return "Welcome To:\n\n" \
            "                          __  \n" \
            "          |\\  /|  |   |  |  \\ \n" \
            "    |   | | \\/ |  |   |  |   | \n" \
            "|/\\ |   | |    |  |   |  |   | \n" \
            "|   | /\\| |    |  |   |  |   | \n" \
            "|   | \\/| |    |.  \\__|. |__/. \n" \
            f"\n{self.state.current_room.describe()}\n" 
        else:
            return ""

    def parse(self, text: str) -> None:
        if not len(text):
            return nothing_message
        
        commands = {
            'jump': JumpCommand(),

            'move': MoveCommand(),
            'go': MoveCommand(),
            'm': MoveCommand(),

            'grab': GrabCommand(),
            'get': GrabCommand(),
            'take': GrabCommand(),
            'g': GrabCommand(),

            'use': UseCommand(),
            'u': UseCommand(),

            'look': LookCommand(),
            'l': LookCommand()
        }
        
        stripped_text = text.lower().strip()

        stripped_text = stripped_text.replace('stab', 'use knife')

        verb, *args = stripped_text.split(' ')
        args = list(filter(lambda x: x not in forbidden_words, args))

        if verb in commands:
            self.command = commands[verb]
            if len(args) >= len(self.command.arguments):
                self.command.arguments = args
                return self.command.process(self.state)
            else:
                return f"Incorrect number of arguments. Expected (at least) {len(self.command.arguments)}."
        else:
            return nothing_message