# from pyparsing import col
from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
import time
from soccer.ttypes import PlayerAction, HeliosChainAction


class WithBallDecisionMaker(IDecisionMaker):
    def __init__(self):
        pass
    
    sum_time = 0
    count = 0
    def make_decision(self, agent: IAgent):
        agent.add_action(PlayerAction(helios_chain_action=HeliosChainAction(lead_pass=True,
                                                                                  direct_pass=True,
                                                                                  through_pass=True,
                                                                                  simple_pass=True,
                                                                                  short_dribble=True,
                                                                                  long_dribble=True,
                                                                                  simple_shoot=True,
                                                                                  simple_dribble=True,
                                                                                  cross=True)))