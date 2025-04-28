from typing import Any
import os
import json

from rooms import Room
from player import Player
from commands import *
from colors import *

class WorldState:
    def __init__(self, world) -> None:
        self.just_started = True

        self.global_rooms = []

        for filename in ['yaatr.json', 'yaatr_dungeon.json']:
            with open(os.path.join("data", "locations", filename)) as f:
                data = json.load(f)

                for room in data["rooms"]:
                    self.global_rooms.append(Room(world, room["name"], room["description"], room["items"], room["entities"], {
                        'north': room["north"],
                        'south': room["south"],
                        'east': room["east"],
                        'west': room["west"]
                    }, room["drawing"]))
                
                f.close()
    
    def get_room(self, name: str) -> Room:
        for r in self.global_rooms:
            if r.name == name:
                return r
        
        return None

class World:
    def __init__(self) -> None:
        self.state: WorldState = WorldState(self)
        self.command: Command = None
        self.players: dict[str, Player] = {}
    
    def get_player_with_name(self, name: str) -> Player:
        for _, p in self.players.items():
            if p.name == name:
                return p
        
        return None

    def send_message_to_players_in_room(self, from_player: Player, message: str, room: str) -> None:
        for _, player in self.players.items():
            if player.current_room == room and player.name and player != from_player:
                player.message_from_world = message
        
    def send_message_to_player(self, to_player: Player, message: str) -> None:
        to_player.message_from_world = message