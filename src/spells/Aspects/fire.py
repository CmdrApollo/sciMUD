from .spell import Spell

class Fire(Spell):
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

