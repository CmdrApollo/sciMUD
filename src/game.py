from typing import Any

nothing_message = "You do nothing."

class Room:
    def __init__(self, idx: int, description: str, neighbors: dict[str, Any]):
        self.idx: int = idx
        self.description: str = description
        self.neighbors: dict[str, Any] = neighbors

class GameState:
    def __init__(self) -> None:
        self.global_rooms = [
            Room(0, "You find yourself in a well-lit tavern. There are a few patrons sprinkled throughout the building. To the west you see a dingy store-room.", {
                'north': None,
                'south': None,
                'east': None,
                'west': 1
            }),
            Room(1, "You walk into the dingy room. You can barely see. To the east you see a well lit tavern.", {
                    'north': None,
                    'south': None,
                    'east': 0,
                    'west': None
            })
        ]

        self.current_room = self.global_rooms[0]

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
            state.current_room = state.global_rooms[state.current_room.neighbors[self.arguments[0]]]
            return f"You move {self.arguments[0]}.\n{state.current_room.description}"
        else:
            return "There is no room in that direction."

class Game:
    def __init__(self) -> None:
        self.state: GameState = GameState()
        self.command: Command = None
    
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