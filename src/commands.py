from items import get_item_with_name

class Command:
    def __init__(self, number_arguments: int) -> None:
        self.arguments: list[str] = [''] * number_arguments
    
    def process(self, game):
        pass

class JumpCommand(Command):
    def __init__(self) -> None:
        super().__init__(0)
    
    def process(self, state):
        return "You jump."

class MoveCommand(Command):
    def __init__(self) -> None:
        super().__init__(1)
    
    def process(self, state) -> str:
        if self.arguments[0] not in state.current_room.neighbors:
            return f"Invalid argument: '{self.arguments[0]}'"
        
        if state.current_room.neighbors[self.arguments[0]] != None:
            state.current_room = state.get_room(state.current_room.neighbors[self.arguments[0]])
            return f"You move {self.arguments[0]}.\n{state.current_room.describe()}"
        else:
            return "There is no room in that direction."

class GrabCommand(Command):
    def __init__(self):
        super().__init__(1)
    
    def process(self, state) -> str:
        item = self.arguments[0]

        if item not in state.current_room.items:
            return f"Item '{item}' not found here."

        state.current_room.items.remove(item)
        state.player.inventory.append(get_item_with_name(item))

        return f"You grab the {item}."

class GrabCommand(Command):
    def __init__(self):
        super().__init__(1)
    
    def process(self, state) -> str:
        item = self.arguments[0]

        if item not in state.current_room.items:
            return f"Item '{item}' not found here."

        state.current_room.items.remove(item)
        state.player.inventory.append(type(get_item_with_name(item)))

        return f"You grab the {item}."

class UseCommand(Command):
    def __init__(self):
        super().__init__(1)
    
    def process(self, state) -> str:
        item = get_item_with_name(self.arguments[0])

        if type(item) in state.player.inventory:
            recipient = ''

            if len(self.arguments) > 1:
                recipient = self.arguments[1]

            return item.use(recipient, state)
        
        return "You don't have that item."