from typing import Any
import os
import json

from rooms import Room
from player import Player
from commands import *
from colors import *

class WorldState:
    def __init__(self) -> None:
        self.just_started = True

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
    
    def get_room(self, name: str) -> Room:
        for r in self.global_rooms:
            if r.name == name:
                return r
        
        return None

class World:
    def __init__(self) -> None:
        self.state: WorldState = WorldState()
        self.command: Command = None
        self.players: dict[str, Player] = {}

    '''
    Takes a string as input and echoes it to the currently active room in the world. What if there are multiple active rooms?
    This could become a problem later when we implement summoning and the players are in different rooms.
    For now let's just pretend that doesn't happen.
    '''
    def room_message(self, message: str):
        pass #write this later