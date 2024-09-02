from abc import ABC, abstractmethod
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
from soccer.ttypes import WorldModel


class IPositionStrategy(ABC):
    @abstractmethod
    def getPosition(self, uniform_number) -> Vector2D:
        pass
    
    @abstractmethod
    def update(self, wm: WorldModel):
        pass
    