from src.IAgent import IAgent
from soccer.ttypes import *

class IntentionWaitAfterSetPlayKick:

    def __init__(self):
        pass

    def finished(agent: IAgent) -> bool:
        wm = agent.wm

        if wm.kickable_opponent_existance:
            return True

        if not wm.myself.is_kickable:
            return True

        return False

    def execute(self, agent: IAgent) -> bool:
        return [PlayerAction(bhv_body_neck_to_ball=Bhv_BodyNeckToBall())]
