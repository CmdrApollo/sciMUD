from typing import Any

class Room:
    def __init__(self, name: str, description: str, items: list[str], neighbors: dict[str, Any]) -> None:
        self.name: str = name
        self.description: str = description
        self.items: list[str] = items
        self.neighbors: dict[str, Any] = neighbors
    
    def describe(self) -> str:
        return self.description + (f"\nYou see: {','.join([a.capitalize() for a in self.items])}" if len(self.items) else '')
