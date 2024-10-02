from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D

class Bhv_GoToPlacedBall:
    
    def __init__(self):
        self.M_ball_place_angle = 0.0  
        pass

    def execute(self, agent: IAgent):
        dir_margin = 15.0
        sp = agent.serverParams
        wm = agent.wm
        angle_diff = wm.ball.angle_from_self - self.M_ball_place_angle

        if abs(angle_diff) < dir_margin and wm.ball.dist_from_self < (agent.serverParams.player_size + sp.ball_size + 0.08):
            # already reach
            return False

        # decide sub-target point
        sub_target = wm.ball.position + Vector2D.polar2vector(2.0, self.M_ball_place_angle + 180.0)

        dash_power = 20.0
        dash_speed = -1.0
        if wm.ball.dist_from_self > 2.0:
            dash_power = Bhv_SetPlay.get_set_play_dash_power(agent)
        else:
            dash_speed = sp.player_size
            dash_power = wm.self.player_type.get_dash_power_to_keep_speed(dash_speed, wm.self.effort)

        # it is necessary to go to sub target point
        if abs(angle_diff) > dir_margin:
            Logger.team(f"{__file__}: go to sub-target({sub_target.x:.1f}, {sub_target.y:.1f})")
            Body_GoToPoint(sub_target, 0.1, dash_power, dash_speed).execute(agent)
        # dir diff is small. go to ball
        else:
            # body dir is not right
            if abs(wm.ball.angle_from_self - wm.self.body) > 1.5:
                Logger.team(f"{__file__}: turn to ball")
                Body_TurnToBall().execute(agent)
            # dash to ball
            else:
                Logger.team(f"{__file__}: dash to ball")
                agent.do_dash(dash_power)

        agent.set_neck_action(Neck_ScanField())

        return True