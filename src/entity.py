class EntityStatus:
    NONE = 1 << 0   # 00000001
    ONFIRE = 1 << 1 # 00000010
    FROZEN = 1 << 2 # 00000100
    UNDERWATER = 1 << 3
    ELECTRIFIED = 1 << 6
    WET = 1 << 9

class Entity:
    def __init__(self, name: str, description: str):
        self.status = 0
        self.name = name
        self.description = description
    
    def on_world_tick(self, world):
        # TODO: use lupa to allow for scripting of objects directly from world editor?
        pass