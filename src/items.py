class Item:
    def __init__(self, name: str, description: str, needs_recipient: bool = False) -> None:
        self.name: str = name
        self.description: str = description
        self.needs_recipient: bool = needs_recipient

        self.fail_message: str = ""

    def try_use(self, recipient: str, game) -> bool:
        if self.needs_recipient and recipient == '':
            self.fail_message = "This item requires a recipient."
            return False
        if not self.needs_recipient and recipient:
            self.fail_message = "This item does not require a recipient."
            return False
        return True

    def use(self, recipient: str, game) -> str:
        return ''

class Knife(Item):
    def __init__(self):
        super().__init__("Knife", "A small knife.", True)
    
    def use(self, recipient: str, game) -> str:
        if self.try_use(recipient, game):
            if recipient in game.current_room.entities:
                game.current_room.entities.remove(recipient)
                return f"You viciously stab the {recipient}."
            else:
                return f"There is no {recipient} here."
        return self.fail_message

def get_item_with_name(name: str) -> Item:
    match name:
        case "knife":
            return Knife()
        case _:
            return None