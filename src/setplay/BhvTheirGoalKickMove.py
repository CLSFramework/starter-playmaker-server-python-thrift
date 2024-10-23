from src.IAgent import IAgent
from src.setplay.BhvSetPlay import BhvSetPlay
from soccer.ttypes import *
from Strategy import *
from pyrusgeom.vector_2d import Vector2D
from Tools import Tools
from pyrusgeom.soccer_math import inertia_n_step_point
from pyrusgeom.ray_2d import Ray2D
from pyrusgeom.size_2d import Size2D
from pyrusgeom.rect_2d import Rect2D

class BhvTheirGoalKickMove:

    @staticmethod
    def execute(agent: IAgent) -> bool:
        expand_their_penalty = Rect2D(
            Vector2D(agent.serverParams.their_penalty_area_line_x - 0.75,
                      -agent.serverParams.penalty_area_half_width - 0.75),
            Size2D(agent.serverParams.penalty_area_length + 0.75,
                   (agent.serverParams.penalty_area_half_width*2) + 1.5)
        )

        wm = agent.wm
        actions = []
        actions += BhvTheirGoalKickMove.do_chase_ball(agent)

        intersection = Vector2D()
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_velocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)
        if ball_velocity.r()  > 0.2: # '''vel.r''' TODO
            if not expand_their_penalty.contains(ball_position) or  expand_their_penalty.intersection(Ray2D(ball_position, wm.ball.velocity.angle), intersection, None) != 1:
                return BhvTheirGoalKickMove.do_normal(agent)
        else:
            if (wm.ball.position.x > agent.serverParams.their_penalty_area_line_x + 7.0 and
                abs(wm.ball.position.y) < (agent.serverParams.goal_width/2.0) + 2.0):
                return BhvTheirGoalKickMove.do_normal(agent)

            intersection.set_x(agent.serverParams.their_penalty_area_line_x() - 0.76)
            intersection.set_y(wm.ball.position.y)

        min_dist = 100.0
        Tools.get_nearest_teammate(agent, intersection)
        if min_dist < wm.myself.position.dist(intersection):
            return BhvTheirGoalKickMove.do_normal(agent)

        dash_power = agent.serverParams.max_dash_power * 0.8

        if intersection.x() < agent.serverParams.their_penalty_area_line_x() and wm.myself.position.x > agent.serverParams.their_penalty_area_line_x - 0.5:
            intersection.set_y(agent.serverParams.penalty_area_half_width - 0.5)
            if wm.myself.position.y < 0.0:
                intersection.set_y(intersection.y() * -1.0)
        elif intersection.y() > agent.serverParams.penalty_area_half_width and abs(wm.myself.position.y) < agent.serverParams.penalty_area_half_width() + 0.5:
            intersection.set_y(agent.serverParams.penalty_area_half_width + 0.5)
            if wm.myself.position.y < 0.0:
                intersection.y(intersection.y() * -1.0)

        dist_thr = max(wm.ball.dist_from_self * 0.07, 1.0)
        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(intersection.x(), intersection.y()), dist_thr, dash_power)))
        actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall(0)))
        
        return actions

    @staticmethod
    def do_normal(agent: IAgent):
        wm = agent.wm
        actions = []
        dash_power = BhvSetPlay.get_set_play_dash_power(agent)
        targ = Strategy.get_home_pos(wm, wm.myself.uniform_number)
        target_point = Vector2D(targ.x, targ.y)

        # Attract to ball
        if target_point.x() > 25.0 and (target_point.y() * wm.ball.position.y < 0.0 or target_point.abs_y() < 10.0):
            y_diff = wm.ball.position.y - target_point.y()
            target_point.set_y(target_point.y() + y_diff * 0.4)

        # Check penalty area
        if wm.myself.position.x > agent.serverParams.their_penalty_area_line_x and target_point.abs_y() < agent.serverParams.penalty_area_half_width():
            target_point.set_y(agent.serverParams.penalty_area_half_width + 0.5)
            if wm.myself.position.y < 0.0:
                target_point.set_y(target_point.y() * -1)

        dist_thr = max(wm.ball.dist_from_self * 0.07, 1.0)
        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(target_point.x(), target_point.y()), dist_thr, dash_power)))
        actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall(0)))
        
        return actions

    @staticmethod
    def do_chase_ball(agent: IAgent) -> bool:
        wm = agent.wm
        actions = []
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_velocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)

        if ball_velocity.r() < 0.2:
            return []

        self_min = wm.intercept_table.self_reach_steps

        if self_min > 10:
            return []

        get_pos = Vector2D(Tools.inertia_point(ball_position, ball_velocity,self_min, agent.serverParams.ball_decay))

        pen_x = agent.serverParams.their_penalty_area_line_x - 1.0
        pen_y = agent.serverParams.penalty_area_half_width + 1.0
        their_penalty = Rect2D(
            Vector2D(pen_x, -pen_y),
            Size2D(agent.serverParams.penalty_area_length + 1.0,
                   (agent.serverParams.penalty_area_half_width*2) - 2.0)
        )
        if their_penalty.contains(get_pos):
            return []

        if (get_pos.x() > pen_x and
            wm.myself.position.x < pen_x and
            abs(wm.myself.position.y) < pen_y - 0.5):
            return []


        # Can chase!!
        agent.add_log_text(LoggerLevel.TEAM,f"{__file__}:GKickGetBall")
        actions.append(PlayerAction(body_intercept=Body_Intercept()))
        actions.append(PlayerAction()(neck_turn_to_ball_or_scan=Neck_TurnToBallOrScan(0)))
        return actions
