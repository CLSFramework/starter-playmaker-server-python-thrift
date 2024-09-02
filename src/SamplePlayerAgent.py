from abc import ABC
from src.DecisionMaker import DecisionMaker
from src.IAgent import IAgent
from src.FormationStrategy import FormationStrategy
from soccer.ttypes import WorldModel, PlayerActions


class SamplePlayerAgent(IAgent, ABC):
    def __init__(self):
        super().__init__()
        self.decisionMaker = DecisionMaker()
        self.strategy = FormationStrategy()
        self.wm: WorldModel = None
    
    def get_actions(self, wm:WorldModel) -> PlayerActions:
        self.wm = wm
        self.actions.clear()
        self.strategy.update(wm)
        self.decisionMaker.make_decision(self)
        actions = PlayerActions()
        actions.actions = []
        actions.actions.extend(self.actions)
        return actions
    
    def get_strategy(self):
        return self.strategy