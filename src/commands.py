from items import get_item_with_name

class Command:
    def __init__(self, number_arguments: int) -> None:
        self.number_arguments: int = number_arguments
        self.arguments: list[str] = [''] * self.number_arguments
    
    def process(self, player, world):
        pass

class SayCommand(Command):
    def __init__(self) -> None:
        super().__init__(2)
    
    def process(self, player, world):
        message = ' '.join(self.arguments[:-1])
        other = self.arguments[-1].capitalize()
        other_obj = world.get_player_with_name(other)
        if other_obj:
            if other_obj.current_room == player.current_room:
                world.send_message_to_player(other_obj, f"{player.name} says to you, '{message}'.")
                return f"You speak to {other}."
            else:
                return f"{other} is not in the same room as you."
        else:
            return f"Player '{other}' does not exist."

class ShoutCommand(Command):
    def __init__(self) -> None:
        super().__init__(1)
    
    def process(self, player, world):
        world.send_message_to_players_in_room(player, f"You hear {player.name} shout out, saying '{' '.join(self.arguments)}'.", player.current_room)
        return "You shout."

class JumpCommand(Command):
    def __init__(self) -> None:
        super().__init__(0)
    
    def process(self, player, world):
        world.send_message_to_players_in_room(player, f"Player '{player.name}' jumps.", player.current_room)
        return "You jump."

class MoveCommand(Command):
    def __init__(self) -> None:
        super().__init__(1)
    
    def process(self, player, world) -> str:
        player_room = world.state.get_room(player.current_room)

        if self.arguments[0] not in player_room.neighbors:
            return f"Invalid argument: '{self.arguments[0]}'"
        
        if player_room.neighbors[self.arguments[0]] != None:
            world.send_message_to_players_in_room(player, f"Player '{player.name}' leaves the room.", player.current_room)

            world.send_message_to_players_in_room(player, f"Player '{player.name}' walks into the room.", player_room.neighbors[self.arguments[0]])

            player.current_room = player_room.neighbors[self.arguments[0]]
            player_room = world.state.get_room(player.current_room)

            return f"You move {self.arguments[0]}.\n{player_room.describe(player)}"
        else:
            return "There is no room in that direction."

class GrabCommand(Command):
    def __init__(self):
        super().__init__(1)
    
    def process(self, player, world) -> str:
        item = ' '.join(self.arguments).lower()

        player_room = world.state.get_room(player.current_room)

        if item not in player_room.items:
            return f"Item '{item}' not found here."

        player_room.items.remove(item)
        player.inventory.append(get_item_with_name(item))

        world.send_message_to_players_in_room(player, f"Player '{player.name}' grabs {item}.", player.current_room)

        return f"You grab the {item}."

class UseCommand(Command):
    def __init__(self):
        super().__init__(1)
    
    def process(self, player, world) -> str:
        item = get_item_with_name(self.arguments[0])

        if item in player.inventory:
            recipient = ''

            if len(self.arguments) > 1:
                recipient = self.arguments[1]

            return item.use(recipient, player, world)
        
        return "You don't have that item."

class LookCommand(Command):
    def __init__(self):
        super().__init__(0)
    
    def process(self, player, world) -> str:
        recipient = ''

        player_room = world.state.get_room(player.current_room)

        if len(self.arguments) > 0:
            recipient = self.arguments[0]
            item = get_item_with_name(recipient)
            if item and (item in player.inventory or recipient in player_room.items):
                return item.description
            else:
                return "You don't see that."
        else:
            return world.state.get_room(player.current_room).describe(player)

class SearchCommand(Command):
    def __init__(self):
        super().__init__(0)
    
    def process(self, player, world) -> str:
        # TODO make it so that individual players track revealed items
        player_room = world.state.get_room(player.current_room)

        if len(player_room.hidden_items):
            h = player_room.hidden_items.copy()

            for i in player_room.hidden_items[::-1]:
                player_room.items.append(i)
                player_room.hidden_items.remove(i)

            return f"You dig through the room, you found {'some items' if len(h) > 1 else 'an item'}!"
        
        return "You search the room far and wide, but fail to find anything."

class HeatCommand(Command):
    def __init__(self):
        super().__init__(1)

    def process(self, player, world):
        other = self.arguments[-1].capitalize()
        other_obj = world.get_player_with_name(other)
        if other_obj:
            if other_obj.current_room == player.current_room:
                world.send_message_to_player(other_obj, f"{player.name} huddles next to you, restoring some of your warmth.")
                return f"You huddle next to {other}. You feel warm."
            else:
                return f"{other} is not in the same room as you."
        else:
            return f"Player '{other}' does not exist."

commands = {
    'jump': JumpCommand(),

    'move': MoveCommand(),
    'walk': MoveCommand(),
    'go': MoveCommand(),
    'm': MoveCommand(),

    'grab': GrabCommand(),
    'get': GrabCommand(),
    'take': GrabCommand(),
    'g': GrabCommand(),

    'use': UseCommand(),
    'u': UseCommand(),

    'look': LookCommand(),
    'l': LookCommand(),

    'search': SearchCommand(),
    'se': SearchCommand(),

    'say': SayCommand(),
    'talk': SayCommand(),
    's': SayCommand(),

    'shout': ShoutCommand(),
    'yell': ShoutCommand(),
    'sh': ShoutCommand(),

    'heat': HeatCommand(),
    'warm': HeatCommand(),
    'cuddle': HeatCommand()
}

aliases = [
    ('stab', 'use knife')
]