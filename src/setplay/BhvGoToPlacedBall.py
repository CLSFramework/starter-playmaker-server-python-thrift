from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D
from src.setplay.BhvSetPlay import BhvSetPlay
from src.Tools import Tools

class BhvGoToPlacedBall:
    
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
        else:
            dash_speed = agent.playerTypes[wm.myself.id].player_size
            dash_power = Tools.GetDashPowerToKeepSpeed(agent, dash_speed, wm.myself.effort)
        # it is necessary to go to sub target point
        if abs(angle_diff) > dir_margin:
            actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(sub_target, 0.1, dash_power, dash_speed)))
        # dir diff is small. go to ball
        else:
            # body dir is not right
            if abs(wm.ball.angle_from_self - wm.myself.body_direction) > 1.5:
                actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall().execute(agent)))
            # dash to ball
            else:
                actions.append(PlayerAction(dash=Dash(dash_power)))
                
        return actions