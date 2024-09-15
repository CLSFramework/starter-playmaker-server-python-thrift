from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
from soccer.ttypes import PlayerAction, Body_Intercept, Neck_TurnToBall, Body_GoToPoint, DebugClient, LoggerLevel, HeliosBasicMove
from src.BhvBasicMove import BhvBasicMove


class NoBallDecisionMaker(IDecisionMaker):
    def __init__(self):
        pass
    
    def make_decision(self, agent: IAgent):
        BhvBasicMove.Decision(agent)
        