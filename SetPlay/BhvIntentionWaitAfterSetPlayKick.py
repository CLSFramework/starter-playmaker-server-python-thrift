from src.IAgent import IAgent
from soccer.ttypes import *

class IntentionWaitAfterSetPlayKick:

    def __init__(self):
        pass

    def finished(self, agent: IAgent) -> bool:
        wm = agent.wm

        if wm.kickable_opponent():
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: finished. exist kickable opponent")
            return True

        if not wm.self().is_kickable():
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: finished. no kickable")
            return True

        return False

    def execute(self, agent: IAgent) -> bool:
        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (execute) wait after set play kick")

        agent.debug_client().add_message("Intention:Wait")

        BhvNeckBodyToBall().execute(agent)

        return True
