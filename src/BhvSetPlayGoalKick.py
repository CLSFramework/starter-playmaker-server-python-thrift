import math
from src.IAgent import IAgent
import math
from src.Dribble import Dribble
from soccer.ttypes import *
from src.Tools import Tools
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.soccer_math import inertia_n_step_point
from pyrusgeom.ray_2d import Ray2D
from pyrusgeom.segment_2d import Segment2D
from pyrusgeom.circle_2d import Circle2D
from pyrusgeom.size_2d import Size2D
from pyrusgeom.rect_2d import Rect2D
from pyrusgeom.line_2d import Line2D

class BhvSetPlayGoalKick:
    def execute(self, agent:IAgent):
        print(f"{__file__}: Bhv_SetPlayGoalKick")
        
        if self.is_kicker(agent):
            self.do_kick(agent)
        else:
            self.do_move(agent)
        
        return True

    def do_kick(self, agent):
        if self.do_second_kick(agent):
            return
        
        if self.go_to_placed_ball(agent):
            print(f"{__file__}: (doKick) go to ball")
            return
        
        if self.do_kick_wait(agent):
            return
        
        if self.do_pass(agent):
            return
        
        if self.do_kick_to_far_side(agent):
            return
        
        real_set_play_count = agent.wm.time().cycle() - agent.wm.last_set_play_start_time().cycle()
        if real_set_play_count <= agent.server_param().drop_ball_time() - 10:
            agent.debug_client().add_message(f"GoalKick:FinalWait{real_set_play_count}")
            agent.body_turn_to_ball()
            agent.set_neck_action(NeckScanField())
            return
        
        agent.debug_client().add_message("GoalKick:Clear")
        print(f"{__file__}: clear ball")
        agent.body_clear_ball()
        agent.set_neck_action(NeckScanField())

    def do_second_kick(self, agent:IAgent):
        wm = agent.wm
        
        if wm.ball().pos().x < -wm.server_param().pitch_half_length + wm.server_param().goal_area_length + 1.0 and \
           abs(wm.ball().pos().y) < wm.server_param().goal_area_width * 0.5 + 1.0:
            return False
        
        print(f"{__file__}: (doSecondKick) ball is moving.")
        
        if wm.self().is_kickable():
            if self.do_pass(agent):
                return True
            
            agent.debug_client().add_message("GoalKick:Clear")
            print(f"{__file__}: (doSecondKick) clear ball")
            agent.body_clear_ball()
            agent.set_neck_action(NeckScanField())
            return True
        
        if self.do_intercept(agent):
            return True
        
        ball_final = wm.ball().inertia_final_point()
        agent.debug_client().add_message("GoalKick:GoTo")
        agent.debug_client().set_target(ball_final)
        print(f"{__file__}: (doSecondKick) go to ball final point({ball_final.x:.2f} {ball_final.y:.2f})")
        
        if not agent.body_go_to_point(ball_final, 2.0, wm.server_param().max_dash_power):
            print(f"{__file__}: (doSecondKick) turn to center")
            agent.body_turn_to_point(Vector2D(0.0, 0.0))
        
        agent.set_neck_action(NeckScanField())
        return True

    def do_kick_wait(self, agent:IAgent):
        wm = agent.wm
        real_set_play_count = wm.time().cycle() - wm.last_set_play_start_time().cycle()

        if real_set_play_count >= wm.server_param().drop_ball_time() - 10:
            print(f"{__file__}: (doKickWait) real set play count = {real_set_play_count} > drop_time-10, no wait")
            return False

        if self.is_delaying_tactics_situation(agent):
            agent.debug_client().add_message("GoalKick:Delaying")
            print(f"{__file__}: (doKickWait) delaying")
            agent.body_turn_to_ball()
            agent.set_neck_action(NeckScanField())
            return True
        
        if abs(wm.ball().angle_from_self() - wm.self().body()) > 3.0:
            agent.debug_client().add_message("GoalKick:TurnToBall")
            agent.body_turn_to_ball()
            agent.set_neck_action(NeckScanField())
            return True
        
        if wm.get_set_play_count() <= 6:
            agent.debug_client().add_message(f"GoalKick:Wait{wm.get_set_play_count()}")
            agent.body_turn_to_ball()
            agent.set_neck_action(NeckScanField())
            return True

        # Additional conditions would follow here...

        return False

    def do_pass(self, agent:IAgent):
        #BhvBasicOffensiveKick().pass(agent, 1) TODO
        return False

    def do_intercept(self, agent:IAgent):
        wm = agent.wm
        if wm.ball().pos().x < -wm.server_param().pitch_half_length + wm.server_param().goal_area_length + 1.0 and \
           abs(wm.ball().pos().y) < wm.server_param().goal_area_width * 0.5 + 1.0:
            return False
        
        if wm.self().is_kickable():
            return False

        self_min = wm.intercept_table().self_step()
        mate_min = wm.intercept_table().teammate_step()
        if self_min > mate_min:
            print(f"{__file__}: (doIntercept) other ball kicker")
            return False
        
        trap_pos = wm.ball().inertia_point(self_min)
        if (trap_pos.x > wm.server_param().our_penalty_area_line_x - 8.0 and 
            abs(trap_pos.y) > wm.server_param().penalty_area_half_width - 5.0) or \
           wm.ball().vel().r2() < 0.25:
            agent.debug_client().add_message("GoalKick:Intercept")
            print(f"{__file__}: (doIntercept) intercept")
            agent.body_intercept()
            agent.set_neck_action(NeckScanField())
            return True
        
        return False

    def do_move(self, agent:IAgent):
        if self.do_intercept(agent):
            return
        
        wm = agent.wm
        dash_power = self.get_set_play_dash_power(agent)
        dist_thr = max(wm.ball().dist_from_self() * 0.07, 1.0)

        target_point = Strategy.get_home_position(wm, wm.self().unum())
        target_point.y += wm.ball().pos().y * 0.5

        if abs(target_point.y) > wm.server_param().pitch_half_width - 1.0:
            target_point.y = sign(target_point.y) * (wm.server_param().pitch_half_width - 1.0)

        if wm.self().stamina() > wm.server_param().stamina_max * 0.9:
            nearest_opp = wm.get_opponent_nearest_to_self(5)
            if nearest_opp and nearest_opp.dist_from_self() < 3.0:
                add_vec = wm.ball().pos() - target_point
                add_vec.set_length(3.0)

                time_val = wm.time().cycle() % 60
                if time_val < 20:
                    pass
                elif time_val < 40:
                    target_point += add_vec.rotated_vector(90.0)
                else:
                    target_point += add_vec.rotated_vector(-90.0)

                target_point.x = min(max(-wm.server_param().pitch_half_length, target_point.x), wm.server_param().pitch_half_length)
                target_point.y = min(max(-wm.server_param().pitch_half_width, target_point.y), wm.server_param().pitch_half_width)

        agent.debug_client().add_message("GoalKickMove")
        agent.debug_client().set_target(target_point)

        if not agent.body_go_to_point(target_point, dist_thr, dash_power):
            agent.body_turn_to_ball()

        if (wm.self().pos().dist(target_point) > wm.ball().pos().dist(target_point) * 0.2 + 6.0 or 
            wm.self().stamina() < wm.server_param().stamina_max * 0.7):
            if not wm.self().stamina_model().capacity_is_empty():
                agent.debug_client().add_message("Sayw")
                agent.add_say_message(WaitRequestMessage())

        agent.set_neck_action(NeckScanField())

    def do_kick_to_far_side(self, agent:IAgent):
        wm = agent.wm
        
        target_point = Vector2D(wm.server_param().our_penalty_area_line_x - 5.0, 
                                wm.server_param().penalty_area_half_width)
        if wm.ball().pos().y > 0.0:
            target_point.y *= -1.0

        ball_move_dist = wm.ball().pos().dist(target_point)
        ball_first_speed = self.calc_first_term_geom_series_last(0.7, ball_move_dist, wm.server_param().ball_decay)
        ball_first_speed = min(wm.server_param().ball_speed_max, ball_first_speed)
        ball_first_speed = min(wm.self().kick_rate * wm.server_param().max_power, ball_first_speed)

        accel = target_point - wm.ball().pos()
        accel.set_length(ball_first_speed)

        kick_power = min(wm.server_param().max_power, accel.r() / wm.self().kick_rate)
        kick_angle = accel.th()

        print(f"{__file__}: (doKickToFarSide) target=({target_point.x:.2f} {target_point.y:.2f}) dist={ball_move_dist:.3f} ball_speed={ball_first_speed:.3f}")
        print(f"{__file__}: (doKickToFarSide) kick_power={kick_power} kick_angle={kick_angle.degree()}")

        agent.do_kick(kick_power, kick_angle - wm.self().body())
        agent.set_neck_action( neckscanfield)

        return True
