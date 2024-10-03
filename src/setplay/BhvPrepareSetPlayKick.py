from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.angle_deg import AngleDeg

class BhvPrepareSetPlayKick:

    def __init__(self):
        self.s_rest_wait_cycle = -1

    def execute(self, agent: IAgent) -> bool:
        # Not reach the ball side
        if BhvGoToPlacedBall(M_ball_place_angle).execute(agent):
            return True

        # Reach to ball side
        if self.s_rest_wait_cycle < 0:
            self.s_rest_wait_cycle = M_wait_cycle

        if self.s_rest_wait_cycle == 0:
            if (agent.wm.myself.stamina() < agent.serverParams.stamina_max * 0.9 or
                    agent.wm.seeTime() != agent.wm.cycle):
                self.s_rest_wait_cycle = 1

        if self.s_rest_wait_cycle > 0:
            if agent.wm.game_mode_type == GameModeType.KickOff_:
                moment = AngleDeg(agent.serverParams.visible_angle)
                agent.doTurn(moment)
            else:
                BodyGoToPoint().execute(agent)

            agent.setNeckAction(NeckScanField())
            self.s_rest_wait_cycle -= 1

            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: wait. rest cycles={self.s_rest_wait_cycle}")
            return True

        self.s_rest_wait_cycle = -1
        return False
