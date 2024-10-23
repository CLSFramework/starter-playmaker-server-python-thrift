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

        if BhvTheirGoalKickMove.do_chase_ball(agent):
            return True

        intersection = Vector2D()

        if wm.ball.velocity.dist  > 0.2: # '''vel.r''' TODO
            if not expand_their_penalty.contains(wm.ball.position) or \
                    expand_their_penalty.intersection(Ray2D(wm.ball.position, wm.ball.velocity.angle), 
                                                      intersection, None) != 1:
                BhvTheirGoalKickMove.do_normal(agent)
                return True
        else:
            if (wm.ball.position.x > agent.serverParams.their_penalty_area_line_x() + 7.0 and
                abs(wm.ball.position.y) < (agent.serverParams.goal_width/2.0) + 2.0):
                BhvTheirGoalKickMove.do_normal(agent)
                return True

            intersection.x = agent.serverParams.their_penalty_area_line_x() - 0.76
            intersection.y = wm.ball.position.y

        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: penalty area intersection ({intersection.x:.1f} {intersection.y:.1f})")

        min_dist = 100.0
        Tools.get_nearest_teammate(intersection, 10, min_dist)
        if min_dist < wm.myself.position.dist(intersection):
            BhvTheirGoalKickMove.do_normal(agent)
            return True

        dash_power = agent.serverParams.max_dash_power() * 0.8

        if intersection.x < agent.serverParams.their_penalty_area_line_x() and \
           wm.myself.position.x > agent.serverParams.their_penalty_area_line_x() - 0.5:
            intersection.y = agent.serverParams.penalty_area_half_width() - 0.5
            if wm.myself.position.y < 0.0:
                intersection.y *= -1.0
        elif intersection.y > agent.serverParams.penalty_area_half_width() and \
             abs(wm.myself.position.y) < agent.serverParams.penalty_area_half_width() + 0.5:
            intersection.y = agent.serverParams.penalty_area_half_width() + 0.5
            if wm.myself.position.y < 0.0:
                intersection.y *= -1.0

        dist_thr = max(wm.ball.dist_from_self * 0.07, 1.0)

        if not BodyGoToPoint(intersection, dist_thr, dash_power).execute(agent):
            agent.add_action(PlayerAction(body_turn_to_ball=Body_TurnToBall(0)))
        
        agent.add_action(PlayerAction(neck_scan_field=Neck_ScanField(0)))
        return True

    @staticmethod
    def do_normal(agent: IAgent):
        wm = agent.wm
        dash_power = Bhv_SetPlay.get_set_play_dash_power(agent)

        target_point = Vector2D(Strategy.get_home_pos(wm, wm.myself.uniform_number))

        # Attract to ball
        if target_point.x > 25.0 and (target_point.y * wm.ball.position.y < 0.0 or target_point.abs_y() < 10.0):
            y_diff = wm.ball.position.y - target_point.y
            target_point.y += y_diff * 0.4

        # Check penalty area
        if wm.myself.position.x > agent.serverParams.their_penalty_area_line_x() and \
           target_point.abs_y() < agent.serverParams.penalty_area_half_width():
            target_point.y = agent.serverParams.penalty_area_half_width() + 0.5
            if wm.myself.position.y < 0.0:
                target_point.y *= -1.0

        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: doNormal target_point({target_point.x:.1f} {target_point.y:.1f})")

        dist_thr = max(wm.ball.dist_from_self * 0.07, 1.0)
        if not BodyGoToPoint(target_point, dist_thr, dash_power).execute(agent):
            agent.add_action(PlayerAction(body_turn_to_ball=Body_TurnToBall(0)))
        
        agent.add_action(PlayerAction(neck_turn_to_ball_or_scan=Neck_TurnToBallOrScan(0)))

    @staticmethod
    def do_chase_ball(agent: IAgent) -> bool:
        wm = agent.wm

        if wm.ball.velocity.r < 0.2: #TODO
            return False

        self_min = wm.intercept_table.self_reach_steps

        if self_min > 10:
            return False

        get_pos = Vector2D(Tools.inertia_point(wm.ball.position,wm.ball.velocity,self_min,ServerParam.ball_decay))

        pen_x = agent.serverParams.their_penalty_area_line_x() - 1.0
        pen_y = agent.serverParams.penalty_area_half_width() + 1.0
        their_penalty = Rect2D(
            Vector2D(pen_x, -pen_y),
            Size2D(agent.serverParams.penalty_area_length() + 1.0,
                   (agent.serverParams.penalty_area_half_width*2) - 2.0)
        )
        if their_penalty.contains(get_pos):
            return False

        if (get_pos.x > pen_x and
            wm.myself.position.x < pen_x and
            abs(wm.myself.position.y) < pen_y - 0.5):
            return False

        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: doChaseBall. cycle = {self_min}  get_pos({get_pos.x:.2f} {get_pos.y:.2f})")

        # Can chase!!
        agent.add_log_text(LoggerLevel.TEAM,f"{__file__}:GKickGetBall")
        agent.add_action(PlayerAction(body_intercept=Body_Intercept()))
        agent.add_action(PlayerAction(neck_turn_to_ball_or_scan=Neck_TurnToBallOrScan(0)))
        return True
