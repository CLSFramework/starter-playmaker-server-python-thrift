from src.IDecisionMaker import IDecisionMaker
from src.DM_PlayOn import PlayOnDecisionMaker
from src.DM_SetPlay import SetPlayDecisionMaker
from src.IAgent import IAgent
from soccer.ttypes import PlayerAction, HeliosGoalie, HeliosPenalty, HeliosSetPlay, GameModeType


class DecisionMaker(IDecisionMaker):
    def __init__(self):
        self.playOnDecisionMaker = PlayOnDecisionMaker()
        self.setPlayDecisionMaker = SetPlayDecisionMaker()
    
    def make_decision(self, agent: IAgent):
        if agent.wm.myself.is_goalie:
            agent.add_action(PlayerAction(helios_goalie=HeliosGoalie()))
        else:
            if agent.wm.game_mode_type == GameModeType.PlayOn:
                self.playOnDecisionMaker.make_decision(agent)
            elif agent.wm.is_penalty_kick_mode:
                agent.add_action(PlayerAction(helios_penalty=HeliosPenalty()))
            else:
                agent.add_action(PlayerAction(helios_set_play=HeliosSetPlay()))