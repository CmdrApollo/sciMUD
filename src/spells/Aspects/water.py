from .spell import Spell

class Water(Spell):
    # a, r, e1, d1, i1
    def FirstEffect(self): 
        print("First Effect")

    def SecondEffect(self):
        raise NotImplementedError

    def ThirdEffect(self):
        raise NotImplementedError

    def FourthEffect(self):
        raise NotImplementedError

    def FifthEffect(self):
        raise NotImplementedError

