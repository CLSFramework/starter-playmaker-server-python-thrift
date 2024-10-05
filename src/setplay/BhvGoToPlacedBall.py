from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D
from src.setplay.BhvSetPlay import BhvSetPlay
from src.Tools import Tools

class Bhv_GoToPlacedBall:
    
    def __init__(self, angle: float):
        self.M_ball_place_angle = angle  
        pass

    def Decision(self, agent: IAgent):
        actions = []
        
        dir_margin = 15.0
        sp = agent.serverParams
        wm = agent.wm
        angle_diff = wm.ball.angle_from_self - self.M_ball_place_angle

        if abs(angle_diff) < dir_margin and wm.ball.dist_from_self < (agent.playerTypes[wm.myself.id].player_size + sp.ball_size + 0.08):
            # already reach
            return actions

        # decide sub-target point
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        sub_target = ball_position + Vector2D.polar2vector(2.0, self.M_ball_place_angle + 180.0)

        dash_power = 20.0
        dash_speed = -1.0
        if wm.ball.dist_from_self > 2.0:
            dash_power = BhvSetPlay.get_set_play_dash_power(agent)
        else: #TODO
            dash_speed = agent.playerTypes[wm.myself.id].player_size
            dash_power = Tools.GetDashPowerToKeepSpeed(agent, dash_speed, wm.myself.effo) #TODO
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