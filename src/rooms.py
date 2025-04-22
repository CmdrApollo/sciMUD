from typing import Any

class Room:
    def __init__(self, world, name: str, description: str, items: list[str], entities: list[str], neighbors: dict[str, Any]) -> None:
        self.world = world

        self.name: str = name
        self.description: str = description
        self.items: list[str] = items
        self.entities: list[str] = entities
        self.neighbors: dict[str, Any] = neighbors
    
    def describe(self, player) -> str:
        players = list(filter(lambda p: p.current_room == self.name and p != player, self.world.players.values()))

        return self.description + (f"\nItems: {','.join([a.capitalize() for a in self.items])}" if len(self.items) else '') + (f"\nPlayers: {','.join([p.name for p in players])}" if len(players) else '')