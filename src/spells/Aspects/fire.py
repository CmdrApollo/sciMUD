from .spell import Spell
from ...items import Item, ItemStatus

class Fire(Spell):
    # a, r, e1, d1, i1
    def FirstEffect(self): 
        for e in self.targets:
            if issubclass(e, Item):
                e.status |= ItemStatus.ONFIRE
        print("First Effect")

    def SecondEffect(self):
        raise NotImplementedError

    def ThirdEffect(self):
        raise NotImplementedError

    def FourthEffect(self):
        raise NotImplementedError

    def FifthEffect(self):
        raise NotImplementedError

