from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from soccer.ttypes import Body_HoldBall, LoggerLevel, PlayerAction
from src.Shoot import Shoot
from pyrusgeom.vector_2d import Vector2D
from src.Pass import Pass
from src.Dribble import Dribble
from src.ClearBall import ClearBall
from src.Tools import Tools

class BhvBasicOffensiveKick:
    def __init__(self):
        pass
    
    sum_time = 0
    count = 0
    def Decision(agent: IAgent):
 
        agent.add_log_message(LoggerLevel.TEAM ,
                                    f": DM_WithBall" ,
                                        agent.wm.myself.position.x ,
                                            agent.wm.myself.position.y - 2 ,
                                                '\033[31m')
        actions = []
        actions += [shoot] if (shoot := Shoot.Decision(agent)) is not None else []
        opps = Tools.OpponentsFromSelf(agent)
        nearest_opp = Vector2D( opps[0] if opps else None)
        nearest_opp_dist = nearest_opp.dist(agent.wm.myself.position) if nearest_opp else 1000.0 
        
        if nearest_opp_dist < 10:
            actions += [passing] if (passing := Pass.Decision(agent)) is not None else []
            
        actions += [dribble] if (dribble := Dribble.Decision(agent)) is not None else []
        
        if nearest_opp_dist > 2.5:
            actions.append(PlayerAction(body_hold_ball=Body_HoldBall()))

        actions.append(ClearBall.Decision(agent))
        
        #Sending actions' queue
        return actions
        '''agent.add_action(PlayerAction(helios_chain_action=HeliosChainAction(lead_pass=True,
                                                                                  direct_pass=True,
                                                                                  through_pass=True,
                                                                                  simple_pass=True,
                                                                                  short_dribble=True,
                                                                                  long_dribble=True,
                                                                                  simple_shoot=True,
                                                                                  simple_dribble=True,
                                                                                  cross=True)))'''