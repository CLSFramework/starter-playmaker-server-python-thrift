from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
from src.BhvBasicMove import BhvBasicMove


class NoBallDecisionMaker(IDecisionMaker):
    def __init__(self):
        pass
    
    def make_decision(self, agent: IAgent):
        # Queued actions are reversed and send here
        bhv_basic_move_actions = list(reversed(BhvBasicMove.Decision(agent)))
        for act in bhv_basic_move_actions:
            agent.add_action(act)