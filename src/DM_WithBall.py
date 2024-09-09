# from pyparsing import col
from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
import time
import logging
from soccer.ttypes import *
from src.Shoot import Shoot

class WithBallDecisionMaker(IDecisionMaker):
    def __init__(self):
        pass
    
    sum_time = 0
    count = 0
    def make_decision(self, agent: IAgent):

        agent.add_log_message(LoggerLevel.TEAM ,
                                    f": DM_WithBall" ,
                                        agent.wm.myself.position.x ,
                                            agent.wm.myself.position.y - 2 ,
                                                '\033[31m')
        #Shoot.decision(self, agent)
        agent.add_action(PlayerAction(helios_chain_action=HeliosChainAction(lead_pass=True,
                                                                                  direct_pass=True,
                                                                                  through_pass=True,
                                                                                  simple_pass=True,
                                                                                  short_dribble=True,
                                                                                  long_dribble=True,
                                                                                  simple_shoot=True,
                                                                                  simple_dribble=True,
                                                                                  cross=True)))