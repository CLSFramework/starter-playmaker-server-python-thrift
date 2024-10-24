import math
from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.segment_2d import Segment2D
from pyrusgeom.circle_2d import Circle2D
from soccer.ttypes import *
from src.setplay.BhvSetPlay import BhvSetPlay
from src.setplay.BhvGoToPlacedBall import BhvGoToPlacedBall
from src.Pass import Pass
from src.Tools import Tools
from src.setplay.BhvSetPlay import BhvSetPlay
from src.Strategy import Strategy
import pyrusgeom.soccer_math as smath
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
import math

class BhvSetPlayIndirectFreeKick:
    def __init__(self):
        pass

    def Decision(agent: IAgent):
        wm = agent.wm
        our_kick = (wm.game_mode_type == GameModeType.BackPass_ and wm.game_mode_side != wm.our_side) or (wm.game_mode_type == GameModeType.IndFreeKick_ and wm.game_mode_side == wm.our_side) or (wm.game_mode_type == GameModeType.FoulCharge_ and wm.game_mode_side != wm.our_side) or (wm.game_mode_type == GameModeType.FoulPush_ and  wm.game_mode_side != wm.our_side ) 
        our_kick = True

        if our_kick:
            if BhvSetPlay.is_kicker(agent):
                return BhvSetPlayIndirectFreeKick.do_kicker(agent)
            else:
                return BhvSetPlayIndirectFreeKick.do_offense_move(agent)
        else:
            return BhvSetPlayIndirectFreeKick.do_defense_move(agent)

        return []

    def do_kicker(agent: IAgent):
        # go to ball
        actions = []
        actions += BhvGoToPlacedBall.Decision(agent=agent)

        # wait
        actions += BhvSetPlayIndirectFreeKick.do_kick_wait(agent)

        # kick to the teammate exist at the front of their goal
        actions += BhvSetPlayIndirectFreeKick.do_kick_to_shooter(agent)

        wm = agent.wm
        max_kick_speed = wm.self.kick_rate * agent.serverParams.max_power

        # pass
        actions += Pass.Decision(agent)
        # wait(2)
        if wm.set_play_count <= 3:
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(50, 0))))

        # no teammate
        if not Tools.TeammatesFromBall(agent) or Tools.TeammatesFromBall()[0].dist_from_self > 35.0 or Tools.TeammatesFromBall()[0].position.x < -30.0:
            real_set_play_count = int(wm.cycle - wm.last_set_play_start_time)
            if real_set_play_count <= agent.serverParams.drop_ball_time - 3:
                actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(50, 0))))


            target_point = Vector2D(agent.serverParams.pitch_half_length,
                                   (-1 + 2 * wm.cycle % 2) * (agent.serverParams.goal_width / 2 - 0.8))
            ball_speed = max_kick_speed
            actions.append(PlayerAction(body_kick_one_step=Body_KickOneStep(RpcVector2D(target_point.x(), target_point.y()), ball_speed)))
            
            return actions

        # kick to the teammate nearest to opponent goal
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        goal = Vector2D(agent.serverParams.pitch_half_length, self_position.y() * 0.8)

        min_dist = 100000.0
        receiver = None

        for t in Tools.TeammatesFromBall(agent):
            if t.dist_from_ball < 1.5:
                continue
            if t.dist_from_ball > 20.0:
                continue
            if t.position.x > wm.offside_line_x:
                continue
            t_position = Vector2D(t.position.x, t.position.y)
            dist = t_position.dist(goal) + t.dist_from_ball
            if dist < min_dist:
                min_dist = dist
                receiver = t

        target_point = goal
        target_dist = 10.0
        if not receiver:
            target_dist = Tools.TeammatesFromSelf(agent)()[0].dist_from_self
            target_point = Tools.TeammatesFromSelf()[0].position
        else:
            target_dist = receiver.dist_from_self
            target_point = receiver.position
            target_point.x += 0.6

        ball_speed = Tools.calc_first_term_geom_series_last(1.8, target_dist, agent.serverParams.ball_decay)
        ball_speed = min(ball_speed, max_kick_speed)

        actions.append(PlayerAction(body_kick_one_step=Body_KickOneStep(target_point, ball_speed)))
        return actions
        #agent.add_say_message(BallMessage(agent.effector().queued_next_ball_pos(), agent.effector().queued_next_ball_vel())) #TODO

    def do_kick_wait(self, agent: IAgent):
        wm = agent.wm
        actions = []
        face_point = Vector2D(50.0, 0.0)
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        face_angle = (face_point - self_position).th()

        if wm.time_stopped > 0:
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(face_point.x(), face_point.y()))))

        if abs(face_angle - wm.self().body()) > 5.0:
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(face_point.x(), face_point.y()))))

        if wm.set_play_count <= 10 and not Tools.TeammatesFromSelf(agent):
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(face_point.x(), face_point.y()))))

        return actions

    def do_kick_to_shooter(self, agent: IAgent):
        wm = agent.wm
        actions = []
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        goal = Vector2D(agent.serverParams.pitch_half_length, self_position.y() * 0.8)

        min_dist = 100000.0
        receiver = None

        for t in Tools.TeammatesFromBall(agent):
            if t.dist_from_ball < 1.5:
                continue
            if t.dist_from_ball > 20.0:
                continue
            if t.position.x > wm.offside_line_x:
                continue
            if t.position.x < wm.ball.position.x - 3.0:
                continue
            if abs(t.position.y) > agent.serverParams.goal_width / 2 * 0.5:
                continue
            t_position = Vector2D(t.position.x, t.position.y)
            goal_dist = t_position.dist(goal)
            if goal_dist > 16.0:
                continue

            dist = goal_dist * 0.4 + t.dist_from_ball * 0.6

            if dist < min_dist:
                min_dist = dist
                receiver = t

        if not receiver:
            return actions
        
        max_ball_speed = wm.myself.kick_rate * agent.serverParams.max_power
        receiver_pos = Vector2D(receiver.position.x, receiver.position.y)
        receiver_vel = Vector2D(receiver.velocity.x, receiver.velocity.y)
        target_point = receiver_pos + receiver_vel
        target_point.x += 0.6
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        target_dist = ball_position.dist(target_point)

        ball_reach_step = math.ceil(calc_length_geom_series(max_ball_speed, target_dist, agent.serverParams.ball_decay))
        ball_speed = calc_first_term_geom_series(target_dist, agent.serverParams.ball_decay, ball_reach_step)

        ball_speed = min(ball_speed, max_ball_speed)

        actions.append(PlayerAction(body_kick_one_step=Body_KickOneStep(RpcVector2D(target_point.x(), target_point.y()), ball_speed)))
        return actions

    def get_avoid_circle_point(self, agent: IAgent, point: Vector2D):
        SP = agent.serverParams
        wm = agent.wm
        
        circle_r = SP.goal_area_length + 0.5 if wm.game_mode_type == GameModeType.BackPass_ else SP.center_circle_r + 0.5
        circle_r2 = circle_r ** 2

        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        if point.x() < -SP.pitch_half_length + 3.0 and abs(point.y()) < SP.goal_width / 2:
            while point.x() < wm.ball.position.x and point.x() > -SP.pitch_half_length and ball_position.dist2(point) < circle_r2:
                point.x = (point.x() - SP.pitch_half_length) * 0.5 - 0.01

        if point.x() < -SP.pitch_half_length + 0.5 and abs(point.y()) < SP.goal_width / 2 + 0.5 and wm.myself.position.x < -SP.pitch_half_length and abs(wm.myself.position.y) < SP.goal_width / 2:
            return point

        if ball_position.dist2(point) < circle_r2:
            rel = point - ball_position
            rel.set_length(circle_r)
            point = ball_position + rel


        return BhvSetPlay.get_avoid_circle_point(wm, point)

    def do_offense_move(self, agent: IAgent):
        wm = agent.wm
        actions = []
        target_point = Strategy.get_home_pos(wm, wm.myself.uniform_number)
        target_point.x = min(wm.offside_line_x - 1.0, target_point.x)
        target_point_vector2d = Vector2D(target_point.x, target_point.y)

        nearest_dist = 1000.0
        
        teammate = Tools.GetTeammateNearestTo(agent, target_point)
        teammate_pos = Vector2D(teammate.posicion.x, teammate.position.y)
        if nearest_dist < 2.5:
            target_point_vector2d += (target_point_vector2d - teammate_pos).set_length_vector(2.5)
            target_point_vector2d.x() = min(wm.offside_line_x - 1.0, target_point_vector2d.x())

        dash_power = 50
        dash_power = wm.myself.get_safety_dash_power()


        dist_thr = wm.ball.dist_from_self * 0.07
        if dist_thr < 0.5:
            dist_thr = 0.5

        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(target_point_vector2d.x(), target_point_vector2d.y()), dist_thr, dash_power)))
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        turn_point = (RpcVector2D(agent.serverParams.pitch_half_length, 0) + ball_position) * 0.5
        actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(turn_point.x(), turn_point.y()))))
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        if target_point.x > 36.0 and (self_position.dist(target_point) > max(ball_position.dist(target_point) * 0.2, dist_thr) + 6.0 or wm.myself.stamina < agent.serverParams.stamina_max * 0.7):
            if not wm.myself.stamina_capacity == 0:
                actions.append(PlayerAction(say=WaitRequestMessage()))
        actions.append(PlayerAction(neck_turn_to_ball_or_scan=Neck_TurnToBallOrScan(0)))
        
        return actions

    def do_defense_move(self, agent: IAgent):
        actions = []
        SP = agent.serverParams
        wm = agent.wm
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        self_velocity = Vector2D(wm.myself.velocity.x, wm.myself.velocity.y)
        target = Strategy.get_home_pos(wm, wm.myself.uniform_number)
        target_point = Vector2D(target.x, target.y)
        adjusted_point = BhvSetPlayIndirectFreeKick.get_avoid_circle_point(agent, target_point)

        dash_power = wm.myself.get_safety_dash_power

        dist_thr = wm.ball.dist_from_self * 0.07
        if dist_thr < 0.5:
            dist_thr = 0.5

        if adjusted_point != target_point and ball_position.dist(target_point) > 10.0 and Tools.inertia_final_point(agent.playerTypes[agent.wm.myself.id], self_position, self_velocity).dist(adjusted_point) < dist_thr:
            adjusted_point = target_point

        collision_dist = agent.playerTypes[agent.wm.myself.id].player_size + SP.goal_post_radius + 0.2

        goal_post_l = Vector2D(-SP.pitch_half_length + SP.goal_post_radius, -SP.goal_width / 2 - SP.goal_post_radius)
        goal_post_r = Vector2D(-SP.pitch_half_length + SP.goal_post_radius, +SP.goal_width / 2 + SP.goal_post_radius)
        dist_post_l = self_position.dist(goal_post_l)
        dist_post_r = self_position.dist(goal_post_r)

        nearest_post = goal_post_l if dist_post_l < dist_post_r else goal_post_r
        dist_post = min(dist_post_l, dist_post_r)

        if dist_post < collision_dist + agent.playerTypes[agent.wm.myself.id].real_speed_max  + 0.5:
            post_circle = Circle2D(nearest_post, collision_dist)
            move_line = Segment2D(self_position, adjusted_point)

            if post_circle.intersection(move_line, None, None) > 0:
                post_angle = (nearest_post - self_position).th()
                if nearest_post.y() < self_position.y():
                    adjusted_point = nearest_post
                    adjusted_point += Vector2D.from_polar(collision_dist + 0.1, post_angle - 90.0)
                else:
                    adjusted_point = nearest_post
                    adjusted_point += Vector2D.from_polar(collision_dist + 0.1, post_angle + 90.0)

                dist_thr = 0.05
        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(adjusted_point.x(), adjusted_point.y(), dist_thr, dash_power))))
        actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))

        return actions