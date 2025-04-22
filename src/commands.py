from items import get_item_with_name

class Command:
    def __init__(self, number_arguments: int) -> None:
        self.arguments: list[str] = [''] * number_arguments
    
    def process(self, player, world):
        pass

class JumpCommand(Command):
    def __init__(self) -> None:
        super().__init__(0)
    
    def process(self, player, world):
        return "You jump."

class MoveCommand(Command):
    def __init__(self) -> None:
        super().__init__(1)
    
    def process(self, player, world) -> str:
        player_room = world.state.get_room(player.current_room)

        if self.arguments[0] not in player_room.neighbors:
            return f"Invalid argument: '{self.arguments[0]}'"
        
        if player_room.neighbors[self.arguments[0]] != None:
            player.current_room = player_room.neighbors[self.arguments[0]]
            player_room = world.state.get_room(player.current_room)

            return f"You move {self.arguments[0]}.\n{player_room.describe()}"
        else:
            return "There is no room in that direction."

class GrabCommand(Command):
    def __init__(self):
        super().__init__(1)
    
    def process(self, player, world) -> str:
        item = self.arguments[0]

        player_room = world.state.get_room(player.current_room)

        if item not in player_room.items:
            return f"Item '{item}' not found here."

        player_room.items.remove(item)
        player.inventory.append(get_item_with_name(item))

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

            return item().use(recipient, player, world)
        
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
            if item and (type(item) in player.inventory or recipient in player_room.items):
                return item.description
            else:
                return "You don't see that."
        else:
            return world.state.current_room.describe()