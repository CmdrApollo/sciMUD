from typing import Any
from abc import abstractmethod, ABC
from spell_enums import Effect
class Spell(ABC):
    def __init__(self, details, targets: list[Any]):
        self.details = details
        self.targets = targets
        
        self.a, self.r, self.e1, self.d1, self.i1 = self.details
        self.cast = getattr(self, self.effects[self.e1].__name__)

    @abstractmethod
    def FirstEffect(self):
        pass

    @abstractmethod
    def SecondEffect(self):
        pass

    @abstractmethod
    def ThirdEffect(self):
        pass

    @abstractmethod
    def FourthEffect(self):
        pass

    @abstractmethod
    def FifthEffect(self):
        pass

    effects = {
        Effect.FIRST: FirstEffect,
        Effect.SECOND: SecondEffect,
        Effect.THIRD: ThirdEffect,
        Effect.FOURTH: FourthEffect,
        Effect.FIFTH: FifthEffect
    }