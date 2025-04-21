class Commands:
    NONE = 0

class GameState:
    def __init__(self):
        pass

class Game:
    def __init__(self):
        self.state = GameState()
        self.command = Commands.NONE
    
    def parse(self, text: str) -> None:
        self.command = Commands.NONE
    
    def update(self) -> str:
        return "This is a test of the 'Game' class."