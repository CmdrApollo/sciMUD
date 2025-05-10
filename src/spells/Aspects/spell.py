from abc import abstractmethod, ABC
from spell_enums import Effect
class Spell(ABC):
    def __init__(self, e1):
        self.cast = getattr(self, self.effects[e1].__name__)

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