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

class Bhv_SetPlayFreeKick:
    def execute(self, agent: IAgent):
        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: Bhv_SetPlayFreeKick")
        if Bhv_SetPlay.is_kicker(agent):
            self.doKick(agent)
        else:
            self.doMove(agent)
        return True

    def doKick(self, agent:IAgent):
        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKick)")
        
        # go to the ball position
        if Bhv_GoToPlacedBall(0.0).execute(agent):
            return

        # wait
        if self.doKickWait(agent):
            return

        # kick
        wm = agent.wm
        max_ball_speed = wm.myself.kickRate() * ServerParam.i().maxPower()

        # pass
        #Bhv_BasicOffensiveKick().pass(agent, 1) TODO

        # kick to the nearest teammate
        nearest_teammate = wm.getTeammateNearestToSelf(10, False)  # without goalie
        if nearest_teammate and nearest_teammate.distFromSelf() < 20.0 and (
            nearest_teammate.pos().x > -30.0 or nearest_teammate.distFromSelf() < 10.0):
            
            target_point = nearest_teammate.inertiaFinalPoint()
            target_point.x += 0.5

            ball_move_dist = wm.ball().pos().dist(target_point)
            ball_reach_step = math.ceil(calc_length_geom_series(max_ball_speed, ball_move_dist, ServerParam.i().ballDecay()))
            ball_speed = 0.0
            
            if ball_reach_step > 3:
                ball_speed = calc_first_term_geom_series(ball_move_dist, ServerParam.i().ballDecay(), ball_reach_step)
            else:
                ball_speed = calc_first_term_geom_series_last(1.4, ball_move_dist, ServerParam.i().ballDecay())
                ball_reach_step = math.ceil(calc_length_geom_series(ball_speed, ball_move_dist, ServerParam.i().ballDecay()))

            ball_speed = min(ball_speed, max_ball_speed)

            agent.debugClient().addMessage(f"FreeKick:ForcePass{ball_speed:.3f}")
            agent.debugClient().setTarget(target_point)
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}:  force pass. target=({target_point.x:.1f} {target_point.y:.1f}) speed={ball_speed:.2f} reach_step={ball_reach_step}")

            Body_KickOneStep(target_point, ball_speed).execute(agent)
            agent.setNeckAction(Neck_ScanField())
            return

        # clear
        if abs(wm.ball().angleFromSelf() - wm.myself.body()) > 1.5:
            agent.debugClient().addMessage("FreeKick:Clear:TurnToBall")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}:  clear. turn to ball")

            Body_TurnToBall().execute(agent)
            agent.setNeckAction(Neck_ScanField())
            return

        agent.debugClient().addMessage("FreeKick:Clear")
        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}:  clear")

        Body_ClearBall().execute(agent)
        agent.setNeckAction(Neck_ScanField())



    def doKickWait(agent:IAgent):
        wm = agent.wm

        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait)")

        real_set_play_count = int(wm.time().cycle() - wm.last_set_play_start_time().cycle())

        if real_set_play_count >= ServerParam.i().drop_ball_time() - 5:
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) real set play count = {real_set_play_count} > drop_time-10, force kick mode")
            return False

        face_point = Vector2D(40.0, 0.0)
        face_angle = (face_point - wm.myself.pos()).th()

        if wm.time().stopped() != 0:
            Body_TurnToPoint(face_point).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return True

        if Bhv_SetPlay.is_delaying_tactics_situation(agent):
            agent.debug_client().add_message("FreeKick:Delaying")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) delaying")

            Body_TurnToPoint(face_point).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return True

        if not wm.teammates_from_ball():
            agent.debug_client().add_message("FreeKick:NoTeammate")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) no teammate")

            Body_TurnToPoint(face_point).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return True

        if wm.get_set_play_count() <= 3:
            agent.debug_client().add_message(f"FreeKick:Wait{wm.get_set_play_count()}")

            Body_TurnToPoint(face_point).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return True

        if (wm.get_set_play_count() >= 15 and
                wm.see_time() == wm.time() and
                wm.myself.stamina() > ServerParam.i().stamina_max() * 0.6):
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) set play count = {wm.get_set_play_count()}, force kick mode")
            return False

        if abs(face_angle - wm.myself.body()) > 5.0:
            agent.debug_client().add_message("FreeKick:Turn")

            Body_TurnToPoint(face_point).execute(agent)
            agent.set_neck_action(Neck_ScanField())
            return True

        if (wm.see_time() != wm.time() or
                wm.myself.stamina() < ServerParam.i().stamina_max() * 0.9):
            Body_TurnToBall().execute(agent)
            agent.set_neck_action(Neck_ScanField())

            agent.debug_client().add_message(f"FreeKick:Wait{wm.get_set_play_count()}")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) no see or recover")
            return True

        return False

    def do_move(self, agent:IAgent):
        wm = agent.wm

        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doMove)")

        target_point = Strategy.i().get_home_position(wm, wm.myself.unum())

        if wm.get_set_play_count() > 0 and wm.myself.stamina() > ServerParam.i().stamina_max() * 0.9:
            nearest_opp = agent.world().get_opponent_nearest_to_self(5)

            if nearest_opp and nearest_opp.dist_from_self() < 3.0:
                add_vec = wm.ball().pos() - target_point
                add_vec.set_length(3.0)

                time_val = agent.world().time().cycle() % 60
                if time_val < 20:
                    pass
                elif time_val < 40:
                    target_point += add_vec.rotated_vector(90.0)
                else:
                    target_point += add_vec.rotated_vector(-90.0)

                target_point.x = min(max(-ServerParam.i().pitch_half_length(), target_point.x), ServerParam.i().pitch_half_length())
                target_point.y = min(max(-ServerParam.i().pitch_half_width(), target_point.y), ServerParam.i().pitch_half_width())

        target_point.x = min(target_point.x, agent.world().offside_line_x() - 0.5)

        dash_power = Bhv_SetPlay.get_set_play_dash_power(agent)
        dist_thr = wm.ball().dist_from_self() * 0.07
        if dist_thr < 1.0:
            dist_thr = 1.0

        agent.debug_client().add_message("SetPlayMove")
        agent.debug_client().set_target(target_point)
        agent.debug_client().add_circle(target_point, dist_thr)

        if not Body_GoToPoint(target_point, dist_thr, dash_power).execute(agent):
            Body_TurnToBall().execute(agent)

        if wm.myself.pos().dist(target_point) > max(wm.ball().pos().dist(target_point) * 0.2, dist_thr) + 6.0 or wm.myself.stamina() < ServerParam.i().stamina_max() * 0.7:
            if not wm.myself.stamina_model().capacity_is_empty():
                agent.debug_client().add_message("Sayw")
                agent.add_say_message(WaitRequestMessage())

        agent.set_neck_action(Neck_TurnToBallOrScan(0))


