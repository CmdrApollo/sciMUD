from commands import *
from colors import *

nothing_message = colored("You do nothing.", yellow)
forbidden_words = ['to', 'on', 'a', 'an', 'the', 'for', 'towards', 'at', 'with']

class Player:
    def __init__(self, world):
        self.health = 10
        self.max_health = self.health

        self.magic = 10
        self.max_magic = self.magic

        self.inventory = []

        self.just_started = True

        self.world = world

        self.current_room = world.state.global_rooms[0].name
    
    def prompt(self):
        if self.just_started:
            self.just_started = False

            return "Welcome To\n\n" \
            f"                          {colored('__  ', red)}\n" \
            f"          {colored('|\\  /|  |   |  |  \\ ', red)}\n" \
            f"{colored('    |   |', magenta)} {colored('| \\/ |  |   |  |   | ', red)}\n" \
            f"{colored('|/\\ |   |', magenta)} {colored('|    |  |   |  |   | ', red)}\n" \
            f"{colored('|   | /\\|', magenta)} {colored('|    |  |   |  |   | ', red)}\n" \
            f"{colored('|   | \\/|', magenta)} {colored('|    |.  \\__|. |__/. ', red)}\n" \
            f"\n{self.world.state.get_room(self.current_room).describe()}\n" 
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
                return self.command.process(self, self.world)
            else:
                return colored(f"Incorrect number of arguments. Expected (at least) {len(self.command.arguments)}.", red)
        else:
            return nothing_message