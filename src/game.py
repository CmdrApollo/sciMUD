from typing import Any
import os
import json

nothing_message = "You do nothing."

class Room:
    def __init__(self, name: str, description: str, neighbors: dict[str, Any]) -> None:
        self.name: str = name
        self.description: str = description
        self.neighbors: dict[str, Any] = neighbors

class GameState:
    def __init__(self) -> None:
        self.just_started = True

        self.global_rooms = []

        with open(os.path.join("data", "rooms.json")) as f:
            data = json.load(f)

            for room in data["rooms"]:
                self.global_rooms.append(Room(room["name"], room["description"], {
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

class Command:
    def __init__(self, number_arguments: int) -> None:
        self.arguments: list[str] = [''] * number_arguments
    
    def process(self, game: GameState):
        pass

class JumpCommand(Command):
    def __init__(self) -> None:
        super().__init__(0)
    
    def process(self, state: GameState):
        return "You jump."

class MoveCommand(Command):
    def __init__(self) -> None:
        super().__init__(1)
    
    def process(self, state: GameState):
        if self.arguments[0] not in state.current_room.neighbors:
            return f"Invalid argument: '{self.arguments[0]}'"
        
        if state.current_room.neighbors[self.arguments[0]] != None:
            state.current_room = state.get_room(state.current_room.neighbors[self.arguments[0]])
            return f"You move {self.arguments[0]}.\n{state.current_room.description}"
        else:
            return "There is no room in that direction."

class Game:
    def __init__(self) -> None:
        self.state: GameState = GameState()
        self.command: Command = None
    
    def prompt(self):
        if self.state.just_started:
            self.state.just_started = False

            return "Welcome To:\n\n" \
            "                        __  \n" \
            "          |\\  /| |   | |  \\ \n" \
            "    |   | | \\/ | |   | |   | \n" \
            "|/\\ |   | |    | |   | |   | \n" \
            "|   | /\\| |    | |   | |   | \n" \
            "|   | \\/| |    | |___| |__/  \n" 
        else:
            return ""

    def parse(self, text: str) -> None:
        if not len(text):
            return nothing_message
        
        commands = {
            'jump': JumpCommand(),
            'move': MoveCommand()
        }
        
        verbs = text.lower().strip().split(' ')

        if verbs[0] in commands:
            self.command = commands[verbs[0]]
            if len(verbs[1:]) == len(self.command.arguments):
                self.command.arguments = verbs[1:]
                return self.command.process(self.state)
            else:
                return f"Incorrect number of arguments. Expected {len(self.command.arguments)}."
        else:
            return nothing_message