from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from src.DM_WithBall import WithBallDecisionMaker
from src.DM_NoBall import NoBallDecisionMaker


class PlayOnDecisionMaker(IDecisionMaker):
    def __init__(self):
        self.withBallDecisionMaker = WithBallDecisionMaker()
        self.noBallDecisionMaker = NoBallDecisionMaker()
        pass
    
    def make_decision(self, agent: IAgent):
        if agent.wm.myself.is_kickable:
            self.withBallDecisionMaker.make_decision(agent)
        else:
            self.noBallDecisionMaker.make_decision(agent)