from spell_enums import *
from complexity_enums import complexity

class Spell:
    def __init__(self, name, description, runes):
        self.name = name
        self.description = description
        self.runes = runes

        self._complexity_to_gold = 100
        self._complexity_to_mana = 8

        self._mana_scaling = 1.11

        print("{ " + f"Name: {self.name}, Complexity: {self._calculate_complexity()}, Gold Cost: {self._calculate_gold_cost()}, Mana Cost: {self._calculate_mana_cost()}" + " }")
    
    def get_details(self):
        _aspect = aspects[self.runes[0]]
        _range = ranges[self.runes[1]]
        _effect1 = effects[self.runes[2]]
        _duration1 = durations[self.runes[3]]
        _intensity1 = intensities[self.runes[4]]

        return _aspect, _range, _effect1, _duration1, _intensity1

    def _calculate_complexity(self):
        final_complexity = 1

        for r in self.runes: final_complexity *= complexity[r]

        return final_complexity
    
    def _calculate_gold_cost(self):
        return self._calculate_complexity() * self._complexity_to_gold
    
    def _calculate_mana_cost(self):
        return round(pow(self._calculate_complexity() * self._complexity_to_mana, self._mana_scaling))

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

if __name__ == "__main__":
    Spell("Fire-shot", "A low intensity version of the Fireball spell.", "*X.3-") #Fire, Target, First Effect, Medium Duration, High intensity
    Spell("Fireball", "Fireball spell.", "*X.3+") #Fire, Target, First Effect, Medium Duration, High intensity
    Spell("Set the World Ablaze", "Ouch.", "*_.M#") #Fire, Target, First Effect, Long Duration, Insane intensity
    Spell("Room-wide Douse", "Drenches everyone in the room.", "~O.`=") #Water, Room, First Effect, Short Duration, Medium intensity
    Spell("Blind", "Blinds a target.", "GX.`-") #Darkness, Target, First Effect, Short Duration, Low intensity