from spell_enums import *

class Spell:
    def __init__(self, name, description, runes):
        self.name = name
        self.description = description
        self.runes = runes
    
    def get_details(self):
        _aspect = aspects[self.runes[0]]
        _range = ranges[self.runes[1]]
        _effect1 = effects[self.runes[2]]
        _duration1 = durations[self.runes[3]]
        _intensity1 = intensities[self.runes[4]]

        return _aspect, _range, _effect1, _duration1, _intensity1

    def cast(self, player, targ, world):
        a, r, e1, d1, i1 = self.get_details()
        
        target = None

        match r:
            case Range.SELF:
                target = player
            case Range.TARGET:
                target = targ
            case Range.ROOM:
                # SPECIAL
                pass
            case Range.WORLD:
                # ALSO SPECIAL
                pass
        
        