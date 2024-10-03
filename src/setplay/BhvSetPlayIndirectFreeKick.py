import math
from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.segment_2d import Segment2D
from pyrusgeom.circle_2d import Circle2D

class Bhv_SetPlayIndirectFreeKick:
    def __init__(self):
        pass

    def execute(self, agent):
        wm = agent.wm
        our_kick = (wm.game_mode.type == 'BackPass' and wm.game_mode.side == wm.their_side) or \
                   (wm.game_mode.type == 'IndFreeKick' and wm.game_mode.side == wm.our_side) or \
                   (wm.game_mode.type == 'FoulCharge' and wm.game_mode.side == wm.their_side) or \
                   (wm.game_mode.type == 'FoulPush' and wm.game_mode.side == wm.their_side)

        if our_kick:
            print(f"({__file__}): (execute) our kick")
            if Bhv_SetPlay.is_kicker(agent):
                self.do_kicker(agent)
            else:
                self.do_offense_move(agent)
        else:
            print(f"({__file__}): (execute) their kick")
            self.do_defense_move(agent)

        return True

    def do_kicker(self, agent):
        # go to ball
        if Bhv_GoToPlacedBall(0.0).execute(agent):
            return

        # wait
        if self.do_kick_wait(agent):
            return

        # kick to the teammate exist at the front of their goal
        if self.do_kick_to_shooter(agent):
            return

        wm = agent.wm
        max_kick_speed = wm.self.kick_rate * ServerParam.i.max_power

        # pass
        #Bhv_BasicOffensiveKick().pass(agent, 1) TODO
        # wait(2)
        if wm.get_set_play_count() <= 3:
            Body_TurnToPoint(Vector2D(50.0, 0.0)).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return

        # no teammate
        if not wm.teammates_from_ball() or \
           wm.teammates_from_ball()[0].dist_from_self() > 35.0 or \
           wm.teammates_from_ball()[0].pos().x < -30.0:
            real_set_play_count = int(wm.time().cycle - wm.last_set_play_start_time().cycle)
            if real_set_play_count <= ServerParam.i.drop_ball_time() - 3:
                print(f"({__file__}): (doKick) real set play count = {real_set_play_count} <= drop_time-3, wait...")
                Body_TurnToPoint(Vector2D(50.0, 0.0)).execute(agent)
                agent.set_neck_action(Neck_ScanField())
                return

            target_point = Vector2D(ServerParam.i.pitch_half_length(),
                                   (-1 + 2 * wm.time().cycle % 2) * (ServerParam.i.goal_half_width() - 0.8))
            ball_speed = max_kick_speed

            agent.debug_client.add_message("IndKick:ForceShoot")
            agent.debug_client.set_target(target_point)
            print(f"({__file__}):  kick to goal ({target_point.x:.1f} {target_point.y:.1f}) speed={ball_speed:.2f}")

            Body_KickOneStep(target_point, ball_speed).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return

        # kick to the teammate nearest to opponent goal
        goal = Vector2D(ServerParam.i.pitch_half_length(), wm.self().pos().y * 0.8)

        min_dist = 100000.0
        receiver = None

        for t in wm.teammates_from_ball():
            if t.pos_count() > 5:
                continue
            if t.dist_from_ball() < 1.5:
                continue
            if t.dist_from_ball() > 20.0:
                continue
            if t.pos().x > wm.offside_line_x():
                continue

            dist = t.pos().dist(goal) + t.dist_from_ball()
            if dist < min_dist:
                min_dist = dist
                receiver = t

        target_point = goal
        target_dist = 10.0
        if not receiver:
            target_dist = wm.teammates_from_self()[0].dist_from_self()
            target_point = wm.teammates_from_self()[0].pos()
        else:
            target_dist = receiver.dist_from_self()
            target_point = receiver.pos()
            target_point.x += 0.6

        ball_speed = self.calc_first_term_geom_series_last(1.8, target_dist, ServerParam.i.ball_decay())
        ball_speed = min(ball_speed, max_kick_speed)

        agent.debug_client.add_message(f" IndKick:ForcePass{ball_speed:.3f}")
        agent.debug_client.set_target(target_point)
        print(f"({__file__}):  pass to nearest teammate ({target_point.x:.1f} {target_point.y:.1f}) speed={ball_speed:.2f}")

        Body_KickOneStep(target_point, ball_speed).execute(agent)
        agent.set_neck_action(Neck_ScanField())
        agent.add_say_message(BallMessage(agent.effector().queued_next_ball_pos(), agent.effector().queued_next_ball_vel()))

    def do_kick_wait(self, agent):
        wm = agent.wm

        face_point = Vector2D(50.0, 0.0)
        face_angle = (face_point - wm.self().pos()).th()

        if wm.time().stopped() > 0:
            print(f"({__file__}): (doKickWait) stoppage time")
            Body_TurnToPoint(face_point).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return True

        if abs(face_angle - wm.self().body()) > 5.0:
            print(f"({__file__}): (doKickWait) turn to the front of goal")
            agent.debug_client.add_message("IndKick:TurnTo")
            agent.debug_client.set_target(face_point)
            Body_TurnToPoint(face_point).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return True

        if wm.get_set_play_count() <= 10 and not wm.teammates_from_self():
            print(f"({__file__}): (doKickWait) no teammate")
            agent.debug_client.add_message("IndKick:NoTeammate")
            agent.debug_client.set_target(face_point)
            Body_TurnToPoint(face_point).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return True

        return False

    def do_kick_to_shooter(self, agent):
        wm = agent.wm

        goal = Vector2D(ServerParam.i.pitch_half_length(), wm.self().pos().y * 0.8)

        min_dist = 100000.0
        receiver = None

        for t in wm.teammates_from_ball():
            if t.pos_count() > 5:
                continue
            if t.dist_from_ball() < 1.5:
                continue
            if t.dist_from_ball() > 20.0:
                continue
            if t.pos().x > wm.offside_line_x():
                continue
            if t.pos().x < wm.ball().pos().x - 3.0:
                continue
            if abs(t.pos().y) > ServerParam.i.goal_half_width() * 0.5:
                continue

            goal_dist = t.pos().dist(goal)
            if goal_dist > 16.0:
                continue

            dist = goal_dist * 0.4 + t.dist_from_ball() * 0.6

            if dist < min_dist:
                min_dist = dist
                receiver = t

        if not receiver:
            print(f"({__file__}): (doKicToShooter) no shooter")
            return False

        max_ball_speed = wm.self().kick_rate * ServerParam.i.max_power

        target_point = receiver.pos() + receiver.vel()
        target_point.x += 0.6

        target_dist = wm.ball().pos().dist(target_point)

        ball_reach_step = math.ceil(self.calc_length_geom_series(max_ball_speed, target_dist, ServerParam.i.ball_decay()))
        ball_speed = self.calc_first_term_geom_series(target_dist, ServerParam.i.ball_decay(), ball_reach_step)

        ball_speed = min(ball_speed, max_ball_speed)

        agent.debug_client.add_message(f"IndKick:KickToShooter{ball_speed:.3f}")
        agent.debug_client.set_target(target_point)
        print(f"({__file__}):  pass to nearest teammate ({target_point.x:.1f} {target_point.y:.1f}) ball_speed={ball_speed:.2f} reach_step={ball_reach_step}")

        Body_KickOneStep(target_point, ball_speed).execute(agent)
        agent.set_neck_action(Neck_ScanField())

        return True

    def get_avoid_circle_point(self, wm, point):
        SP = ServerParam.i

        circle_r = SP.goal_area_length() + 0.5 if wm.game_mode.type == 'BackPass' else SP.center_circle_r() + 0.5
        circle_r2 = circle_r ** 2

        print(f"({__file__}): (get_avoid_circle_point) point=({point.x:.1f} {point.y:.1f})")

        if point.x < -SP.pitch_half_length() + 3.0 and abs(point.y) < SP.goal_half_width():
            while point.x < wm.ball(). pos().x and point.x > -SP.pitch_half_length() and wm.ball().pos().dist2(point) < circle_r2:
                point.x = (point.x - SP.pitch_half_length()) * 0.5 - 0.01
                print(f"({__file__}): adjust x ({point.x:.1f} {point.y:.1f})")

        if point.x < -SP.pitch_half_length() + 0.5 and abs(point.y) < SP.goal_half_width() + 0.5 and \
           wm.self().pos().x < -SP.pitch_half_length() and abs(wm.self().pos().y) < SP.goal_half_width():
            print(f"({__file__}): (get_avoid_circle_point) ok. already in our goal")
            return point

        if wm.ball().pos().dist2(point) < circle_r2:
            rel = point - wm.ball().pos()
            rel.set_length(circle_r)
            point = wm.ball().pos() + rel

            print(f"({__file__}): (get_avoid_circle_point) circle contains target. adjusted=({point.x:.2f} {point.y:.2f})")

        return Bhv_SetPlay.get_avoid_circle_point(wm, point)

    def do_offense_move(self, agent):
        wm = agent.wm

        target_point = Strategy.i.get_home_position(wm, wm.self().unum())
        target_point.x = min(wm.offside_line_x() - 1.0, target_point.x)

        nearest_dist = 1000.0
        teammate = wm.get_teammate_nearest_to(target_point, 10, nearest_dist)
        if nearest_dist < 2.5:
            target_point += (target_point - teammate.pos()).set_length_vector(2.5)
            target_point.x = min(wm.offside_line_x() - 1.0, target_point.x)

        dash_power = wm.self().get_safety_dash_power(ServerParam.i.max_dash_power())

        dist_thr = wm.ball().dist_from_self() * 0.07
        if dist_thr < 0.5:
            dist_thr = 0.5

        agent.debug_client.add_message("IndFK:OffenseMove")
        agent.debug_client.set_target(target_point)
        agent.debug_client.add_circle(target_point, dist_thr)

        if not Body_GoToPoint(target_point, dist_thr, dash_power).execute(agent):
            turn_point = (ServerParam.i.their_team_goal_pos() + wm.ball().pos()) * 0.5

            Body_TurnToPoint(turn_point).execute(agent)
            print(f"({__file__}):  our kick. turn to ({turn_point.x:.1f} {turn_point.y:.1f})")

        if target_point.x > 36.0 and \
           (wm.self().pos().dist(target_point) > max(wm.ball().pos().dist(target_point) * 0.2, dist_thr) + 6.0 or \
            wm.self().stamina() < ServerParam.i.stamina_max() * 0.7):
            if not wm.self().stamina_model().capacity_is_empty():
                agent.debug_client.add_message("Sayw")
                agent.add_say_message(WaitRequestMessage())

        agent.set_neck_action(Neck_TurnToBallOrScan(0))

    def do_defense_move(self, agent: IAgent):
        SP = ServerParam.i
        wm = agent.wm

        target_point = Strategy.i.get_home_position(wm, wm.self().unum())
        adjusted_point = self.get_avoid_circle_point(wm, target_point)

        print(f"({__file__}): their kick adjust target to ({target_point.x:.1f} {target_point.y:.1f})->({adjusted_point.x:.1f} {adjusted_point.y:.1f})")

        dash_power = wm.self().get_safety_dash_power(SP.max_dash_power())

        dist_thr = wm.ball().dist_from_self() * 0.07
        if dist_thr < 0.5:
            dist_thr = 0.5

        if adjusted_point != target_point and \
           wm.ball().pos().dist(target_point) > 10.0 and \
           wm.self().inertia_final_point().dist(adjusted_point) < dist_thr:
            print(f"({__file__}): reverted to the first target point")
            adjusted_point = target_point

        collision_dist = wm.self().player_type().player_size() + SP.goal_post_radius() + 0.2

        goal_post_l = Vector2D(-SP.pitch_half_length() + SP.goal_post_radius(),
                               -SP.goal_half_width() - SP.goal_post_radius())
        goal_post_r = Vector2D(-SP.pitch_half_length() + SP.goal_post_radius(),
                               +SP.goal_half_width() + SP.goal_post_radius())
        dist_post_l = wm.self().pos().dist(goal_post_l)
        dist_post_r = wm.self().pos().dist(goal_post_r)

        nearest_post = goal_post_l if dist_post_l < dist_post_r else goal_post_r
        dist_post = min(dist_post_l, dist_post_r)

        if dist_post < collision_dist + wm.self().player_type().real_speed_max() + 0.5:
            post_circle = Circle2D(nearest_post, collision_dist)
            move_line = Segment2D(wm.self().pos(), adjusted_point)

            if post_circle.intersection(move_line, None, None) > 0:
                post_angle = (nearest_post - wm.self().pos()).th()
                if nearest_post.y < wm.self().pos().y:
                    adjusted_point = nearest_post
                    adjusted_point += Vector2D.from_polar(collision_dist + 0.1, post_angle - 90.0)
                else:
                    adjusted_point = nearest_post
                    adjusted_point += Vector2D.from_polar(collision_dist + 0.1, post_angle + 90.0)

                dist_thr = 0.05
                print(f"({__file__}): adjust to avoid goal post. ({adjusted_point.x:.2f} {adjusted_point.y:.2f})")

        agent.debug_client.add_message("IndFKMove")
        agent.debug_client.set_target(adjusted_point)
        agent.debug_client.add_circle(adjusted_point, dist_thr)

        if not Body_GoToPoint(adjusted_point, dist_thr, dash_power).execute(agent):
            Body_TurnToBall().execute(agent)
            print(f"({__file__}):  their kick. turn to ball")

        agent.set_neck_action(Neck_TurnToBall())