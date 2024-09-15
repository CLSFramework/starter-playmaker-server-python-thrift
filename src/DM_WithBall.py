# from pyparsing import col
from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from soccer.ttypes import Body_HoldBall, LoggerLevel, PlayerAction
from src.Shoot import Shoot
from src.Pass import Pass
from src.Dribble import Dribble
from src.ClearBall import ClearBall
from src.Tools import Tools

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
        
        wm = agent.wm
        
        Shoot.decision(agent)
        opps = Tools.OpponentsFromSelf(agent)
        nearest_opp = opps[0] if opps else None
        nearest_opp_dist = nearest_opp.dist_from_self if nearest_opp else 1000.0
        
        if nearest_opp_dist < 10:
            Pass.Decision(agent)
            
        Dribble.Decision(agent)
        
        if nearest_opp_dist > 2.5:
            agent.add_action(PlayerAction(body_hold_ball=Body_HoldBall()))

        ClearBall.Decision(agent)
        '''agent.add_action(PlayerAction(helios_chain_action=HeliosChainAction(lead_pass=True,
                                                                                  direct_pass=True,
                                                                                  through_pass=True,
                                                                                  simple_pass=True,
                                                                                  short_dribble=True,
                                                                                  long_dribble=True,
                                                                                  simple_shoot=True,
                                                                                  simple_dribble=True,
                                                                                  cross=True)))'''