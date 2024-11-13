from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from soccer.ttypes import LoggerLevel
from src.BhvBasicOffensiveKick import BhvBasicOffensiveKick


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
        basic_offensive_kick_actions = list(reversed(BhvBasicOffensiveKick.Decision(agent)))
        
        for act in basic_offensive_kick_actions:
            if act == None:
                continue
            agent.add_action(act)
        
        '''agent.add_action(PlayerAction(helios_chain_action=HeliosChainAction(lead_pass=True,
                                                                                  direct_pass=True,
                                                                                  through_pass=True,
                                                                                  simple_pass=True,
                                                                                  short_dribble=True,
                                                                                  long_dribble=True,
                                                                                  simple_shoot=True,
                                                                                  simple_dribble=True,
                                                                                  cross=True)))'''