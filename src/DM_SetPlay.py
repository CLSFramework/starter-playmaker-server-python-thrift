from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from soccer.ttypes import PlayerAction, Turn, WorldModel, HeliosSetPlay


class SetPlayDecisionMaker(IDecisionMaker):
    def __init__(self):
        pass
    
    def make_decision(self, agent: IAgent, wm: WorldModel):
        agent.add_action(PlayerAction(helios_set_play=HeliosSetPlay()))