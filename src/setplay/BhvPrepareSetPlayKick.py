from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.angle_deg import AngleDeg
from src.setplay.BhvGoToPlacedBall import BhvGoToPlacedBall

class BhvPrepareSetPlayKick:

    s_rest_wait_cycle = -1
    
    def __init__(self, ball_place_angle: float, wait_cycle: float):
        self.M_ball_place_angle = ball_place_angle
        self.M_wait_cycle = wait_cycle

    def Decision(self, agent: IAgent) -> bool:
        actions = []
        
        # Not reach the ball side
        actions += BhvGoToPlacedBall(self.M_ball_place_angle).Decision(agent)

        # Reach to ball side
        if self.s_rest_wait_cycle < 0:
            self.s_rest_wait_cycle = self.M_wait_cycle

        if self.s_rest_wait_cycle == 0:
            if (agent.wm.myself.stamina < agent.serverParams.stamina_max * 0.9 or agent.wm.myself.seetime != agent.wm.cycle): #TODO
                self.s_rest_wait_cycle = 1

        if self.s_rest_wait_cycle > 0:
            if agent.wm.game_mode_type == GameModeType.KickOff_:
                moment = AngleDeg(agent.serverParams.visible_angle)
                actions.append(PlayerAction(turn=Turn(moment)))
            else:
                actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))

            self.s_rest_wait_cycle -= 1

            return actions

        self.s_rest_wait_cycle = -1
        return []
