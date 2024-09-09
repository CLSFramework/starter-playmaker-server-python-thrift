from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
from src.Tools import *
from pyrusgeom import vector_2d
from soccer.ttypes import *
import numpy as np 


class Pass:

    def __init__(self):
        pass

    def Decision(agent: IAgent):
        Targets = agent.wm.teammates
        
