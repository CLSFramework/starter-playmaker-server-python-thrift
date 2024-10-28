from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from soccer.ttypes import PlayerAction, Turn, WorldModel, HeliosSetPlay
from src.setplay.BhvSetPlay import BhvSetPlay

class SetPlayDecisionMaker(IDecisionMaker):
    def __init__(self):
        pass
    
    def make_decision(agent: IAgent, wm: WorldModel):
        actions = list(reversed(BhvSetPlay.Decision(agent)))
        for i in actions:
            agent.add_action(i)
        #agent.add_action(PlayerAction(helios_set_play=HeliosSetPlay()))