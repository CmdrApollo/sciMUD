from commands import *
from colors import *

nothing_message = colored("You do nothing.", yellow)
forbidden_words = ['to', 'on', 'a', 'an', 'the', 'for', 'towards', 'at', 'with']

class Player:
    def __init__(self, world):
        self.potential_name = ""
        self.name = ""

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

    def prompt(self):
        if self.just_started:
            self.just_started = False

            return "".join(["Welcome To\n\n",
            colored("  .=*888888888h.                  ", gray) + colored("    j&                                        \n", white),
            colored(" h8888888888888*            &h    ", gray) + colored("   j 8 j8h.  &8h.   &.     h.            &.   \n", white),
            colored("88h.                8             ", gray) + colored("  j* h8   *;8j ;88  h8     88            88   \n", white),
            colored("&8888888888888h.  .h        h     ", gray) + colored("j&*  h8    88   88  h8     88            88   \n", white),
            colored(" *8888888888888h jh8       8h          ", gray) + colored("j8    &h   &j  h8     88      j888h.88   \n", white),
            colored("              .hj*h.      j &.         ", gray) + colored("h8    h8  *8   h8     88    j=     888   \n", white),
            colored(".j8888888888888*  *88888=h  *88888h.   ", gray) + colored("h8    h8  88  j**;   j88   j*8    j888  j\n", white),
            colored("!8888888888888*    *88888*   *88888*   ", gray) + colored("&;    *&  *&=j*  *;8j**&==j  ;=&8j***&=j*\n", white),
            "\nEnter your character's name:\n"])
            # "+-----------------------------+\n",
            # f"|                        {colored('__  ', green)}|\n",
            # f"|{colored('       ', cyan)} {colored('|\\  /|  |   |  |  \\ ', green)}|\n",
            # f"|{colored('       ', cyan)} {colored('| \\/ |  |   |  |   |', green)}|\n",
            # f"|{colored(' _  _ o', cyan)} {colored('|    |  |   |  |   |', green)}|\n",
            # f"|{colored('(  /  |', cyan)} {colored('|    |  |   |  |   |', green)}|\n",
            # f"|{colored('_) \\_ |', cyan)} {colored('|    |.  \\__|. |__/.', green)}|\n",
            # "+-----------------------------+\n"])
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
            
                return f"Really name your character '{self.potential_name}'? (y/n)"
            else:
                match text.lower().strip():
                    case 'y':
                        self.name = self.potential_name

                        self.world.send_message_to_players_in_room(self, f"Player '{self.name}' joins the game.", self.current_room)

                        return self.world.state.get_room(self.current_room).describe(self)
                    case 'n':
                        self.potential_name = ''
                    case _:
                        self.potential_name = ''
                
                return "Enter your character's name:\n"
        
        stripped_text = text.lower().strip()

        for a in aliases:
            stripped_text = stripped_text.replace(a[0], a[1])

        verb, *args = stripped_text.split(' ')
        args = list(filter(lambda x: x not in forbidden_words, args))

        if verb in commands:
            self.command = commands[verb]
            if len(args) >= self.command.number_arguments:
                self.command.arguments = args
                return self.command.process(self, self.world)
            else:
                return colored(f"Incorrect number of arguments. Expected (at least) {len(self.command.arguments)}.", red)
        else:
            return nothing_message