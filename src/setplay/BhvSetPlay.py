from src.IAgent import IAgent
import math
from soccer.ttypes import *
from setplay.BhvSetPlayKickOff import *
from setplay.BhvTheirGoalKickMove import *
from setplay.BhvSetPlayFreeKick import *
from setplay.BhvSetPlayGoalKick import *
from setplay.BhvSetPlayKickIn import *
from setplay.BhvSetPlayIndirectFreeKick import *
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.segment_2d import Segment2D
from pyrusgeom.circle_2d import Circle2D

class BhvSetPlay:
    def __init__(self):
        pass

    def execute(self, agent: IAgent):
        wm = agent.wm
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": Bhv_SetPlay")

        if wm.myself.is_goalie:
            if wm.game_mode_type != GameModeType.BackPass_ and wm.game_mode_type != GameModeType.IndFreeKick_:
                Bhv_GoalieFreeKick.execute(agent) # TODO
            else:
                Bhv_SetPlayIndirectFreeKick.Decision(self,agent)
            return True

        if wm.game_mode_type == GameModeType.KickOff_:
            if wm.gameMode().side() == wm.our_side:
                return BhvSetPlayKickOff.execute(agent)
            else:
                self.doBasicTheirSetPlayMove(agent)
                return True

        if wm.game_mode_type in [GameModeType.KickIn_, GameModeType.CornerKick_]:
            if wm.gameMode().side() == wm.our_side:
                return BhvSetPlayKickIn.execute(self,agent)
            else:
                self.doBasicTheirSetPlayMove(agent)
                return True

        if wm.game_mode_type == GameModeType.GoalKick_:
            if wm.gameMode().side() == wm.our_side:
                return BhvSetPlayGoalKick.Decision(agent)
            else:
                return BhvTheirGoalKickMove.execute(agent)

        if wm.game_mode_type in [GameModeType.BackPass_, GameModeType.IndFreeKick_]:
            return Bhv_SetPlayIndirectFreeKick.Decision(agent)

        if wm.game_mode_type in [GameModeType.FoulCharge_, GameModeType.FoulPush_]:
            if (wm.ball.position.x < ServerParam.our_penalty_area_line_x + 1.0 and
                    abs(wm.ball.position.y) < ServerParam.penalty_area_half_width + 1.0):
                return Bhv_SetPlayIndirectFreeKick.Decision(agent)
            elif (wm.ball.position.x > ServerParam.their_penalty_area_line_x - 1.0 and
                  abs(wm.ball.position.y) < ServerParam.penalty_area_half_width + 1.0):
                return Bhv_SetPlayIndirectFreeKick.Decision(agent)

        if wm.is_our_set_play:
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": our set play")
            return BhvSetPlayFreeKick.Decision(agent)
        else:
            self.doBasicTheirSetPlayMove(agent)
            return True

        return False

    def get_set_play_dash_power(self, agent: IAgent):
        wm = agent.wm
        if not wm.is_our_set_play:
            target_point = Strategy.get_home_pos(wm, wm.myself.uniform_number)
            if target_point.x > wm.myself.position.x:
                if (wm.ball.position.x < -30.0 and
                        target_point.x < wm.ball.position.x):
                    return wm.myself.getSafetyDashPower(ServerParam.max_dash_power)
                rate = 0.0
                if wm.myself.stamina() > ServerParam.stamina_max * 0.8:
                    rate = 1.5 * wm.myself.stamina / ServerParam.stamina_max
                else:
                    rate = 0.9 * (wm.myself.stamina() - ServerParam.recover_dec_thr) / ServerParam.stamina_max
                    rate = max(0.0, rate)
                return (wm.myself.playerType().staminaIncMax() *
                        wm.myself.recovery() *
                        rate)
        return wm.myself.getSafetyDashPower(ServerParam.max_dash_power)

    def can_go_to(agent:IAgent,self, count, wm, ball_circle: Circle2D, target_point:Vector2D):
        wm = agent.wm
        move_line = Segment2D(wm.myself.position, target_point)
        n_intersection = ball_circle.intersection(move_line, None, None)
        agent.add_log_text(LoggerLevel.TEAM, "%d: (can_go_to) check target=(%.2f %.2f) intersection=%d" % (count, target_point.x, target_point.y, n_intersection))
        dlog.addLine(LoggerLevel.TEAM, wm.myself.position, target_point, "#0000ff")
        num = str(count)
        dlog.addMessage(LoggerLevel.TEAM, target_point, num, "#0000ff")
        if n_intersection == 0:
            agent.add_log_text(LoggerLevel.TEAM, "%d: (can_go_to) ok(1)" % count)
            return True
        if n_intersection == 1:
            angle = Vector2D(target_point - wm.myself.position).th()
            agent.add_log_text(LoggerLevel.TEAM, "%d: (can_go_to) intersection=1 angle_diff=%.1f" % (count, abs(angle - wm.ball.angle_from_self)))
            if abs(angle - wm.ball.angle_from_self) > 80.0:
                agent.add_log_text(LoggerLevel.TEAM, "%d: (can_go_to) ok(2)" % count)
                return True
        return False

    def get_avoid_circle_point(self, wm, target_point,agent:IAgent):
        SP = ServerParam
        wm = agent.wm
        avoid_radius = SP.centerCircleR() + wm.myself.playerType().playerSize()
        ball_circle = Circle2D(wm.ball.position, avoid_radius)
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (get_avoid_circle_point) first_target=(%.2f %.2f)" % (target_point.x, target_point.y))
        dlog.addCircle(LoggerLevel.TEAM, wm.ball.position, avoid_radius, "#ffffff")
        if self.can_go_to(agent,-1, wm, ball_circle, target_point):
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (get_avoid_circle_point) ok, first point")
            return target_point
        target_angle = Vector2D(target_point - wm.myself.position).th()
        ball_target_angle = Vector2D(target_point - wm.ball.position).th()
        ball_is_left = wm.ball.angle_from_self.isLeftOf(target_angle)
        ANGLE_DIVS = 6
        subtargets = []
        angle_step = 1 if ball_is_left else -1
        count = 0
        a = angle_step
        for i in range(1, ANGLE_DIVS):
            wm =agent.wm
            angle = ball_target_angle + (180.0 / ANGLE_DIVS) * a
            new_target = Vector2D(wm.ball.position + Vector2D.from_polar(avoid_radius + 1.0, angle))
            agent.add_log_text(LoggerLevel.TEAM, "%d: a=%d angle=%.1f (%.2f %.2f)" % (count, a, angle, new_target.x, new_target.y))
            if abs(new_target.x) > SP.pitch_half_length + SP.pitchMargin() - 1.0 or abs(new_target.y) > SP.pitch_half_width + SP.pitchMargin() - 1.0:
                agent.add_log_text(LoggerLevel.TEAM, "%d: out of field" % count)
                break
            if self.can_go_to(count, wm, ball_circle, new_target, agent):
                return new_target
            a += angle_step
            count += 1
        a = -angle_step
        for i in range(1, ANGLE_DIVS * 2):
            angle = ball_target_angle + (180.0 / ANGLE_DIVS) * a
            new_target = Vector2D(wm.ball.position + Vector2D.from_polar(avoid_radius + 1.0, angle))
            agent.add_log_text(LoggerLevel.TEAM, "%d: a=%d angle=%.1f (%.2f %.2f)" % (count, a, angle, new_target.x, new_target.y))
            if abs(new_target.x) > SP.pitch_half_length + SP.pitchMargin - 1.0 or abs(new_target.y) > SP.pitch_half_width + SP.pitchMargin() - 1.0:
                agent.add_log_text(LoggerLevel.TEAM, "%d: out of field" % count)
                break
            if self.can_go_to(count, wm, ball_circle, new_target, agent):
                return new_target
            a -= angle_step
            count += 1
        return target_point

    def is_kicker(self, agent: IAgent):
        wm = agent.wm
        if wm.game_mode_type == GameModeType.GoalieCatch_ and wm.gameMode().side() == wm.our_side and not wm.myself.is_goalie:
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) goalie free kick")
            return False
        kicker_unum = 0
        min_dist2 = float('inf')
        second_kicker_unum = 0
        second_min_dist2 = float('inf')
        for unum in range(1, 12):
            if unum == wm.our_goalie_uniform_number:
                continue
            home_pos = Vector2D(Strategy.get_home_pos(wm, unum))
            if not home_pos.is_valid:
                continue
            d2 = home_pos.dist2(wm.ball.position)
            if d2 < second_min_dist2:
                second_kicker_unum = unum
                second_min_dist2 = d2
                if second_min_dist2 < min_dist2:
                    second_kicker_unum, kicker_unum = kicker_unum, second_kicker_unum
                    second_min_dist2, min_dist2 = min_dist2, second_min_dist2
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) kicker_unum=%d second_kicker_unum=%d" % (kicker_unum, second_kicker_unum))
        kicker = None
        second_kicker = None
        if kicker_unum != 0:
            kicker = wm.teammates[kicker_unum]
        if second_kicker_unum != 0:
            second_kicker = wm.teammates[second_kicker_unum]
        if not kicker:
            if not Tools.TeammatesFromBall(agent) == Empty and wm.teammatesFromBall()[0].distFromBall() < wm.ball.dist_from_self * 0.9:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) first kicker")
                return False
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) self(1)")
            return True
        if kicker and second_kicker and (kicker.uniform_number == wm.myself.uniform_number or second_kicker.uniform_number == wm.myself.uniform_number):
            if math.sqrt(min_dist2) < math.sqrt(second_min_dist2) * 0.95:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) kicker->unum=%d  (1)" % kicker.uniform_number)
                return kicker.uniform_number == wm.myself.uniform_number
            elif kicker.dist_from_ball < second_kicker.dist_from_ball * 0.95:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) kicker->unum=%d  (2)" % kicker.uniform_number)
                return kicker.uniform_number == wm.myself.uniform_number
            elif second_kicker.distFromBall() < kicker.distFromBall() * 0.95:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) kicker->unum=%d  (3)" % kicker.uniform_number)
                return second_kicker.uniform_number == wm.myself.uniform_number
            elif not Tools.TeammatesFromBall(agent) == Empty and wm.teammatesFromBall()[0].distFromBall() < wm.myself.distFromBall() * 0.95:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) other kicker")
                return False
            else:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) self(2)")
                return True
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) kicker->unum=%d" % kicker.uniform_number)
        return kicker.uniform_number == wm.myself.uniform_number

    def is_delaying_tactics_situation(self, agent: IAgent):
        wm = agent.wm
        real_set_play_count = wm.cycle - wm.last_set_play_start_time
        wait_buf = 15 if wm.game_mode_type == GameModeType.GoalKick_ else 2
        if real_set_play_count >= ServerParam.drop_ball_time - wait_buf:
            return False
        our_score = wm.left_team_score if wm.our_side == LEFT else wm.right_team_score
        opp_score = wm.right_team_score if wm.our_side == LEFT else wm.left_team_score
        if wm.audioMemory().recoveryTime().cycle >= wm.cycle - 10:
            if our_score > opp_score:
                return True
        cycle_thr = max(0, ServerParam.nr_normal_halfs * (ServerParam.half_time * 10) - 500)
        if wm.cycle < cycle_thr:
            return False
        if our_score > opp_score and our_score - opp_score <= 1:
            return True
        return False

    def doBasicTheirSetPlayMove(self, agent: IAgent):
        wm = agent.wm
        target_point = Strategy.get_home_pos(wm, wm.myself.uniform_number)
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": their set play. HomePosition=(%.2f, %.2f)" % (target_point.x, target_point.y))
        dash_power = self.get_set_play_dash_power(agent)
        ball_to_target = Vector2D(target_point - wm.ball.position)
        if ball_to_target.r() < 11.0:
            xdiff = math.sqrt(math.pow(11.0, 2) - math.pow(ball_to_target.y, 2))
            target_point.x = wm.ball.position.x - xdiff
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": avoid circle(1). adjust x. x_diff=%.1f newPos=(%.2f %.2f)" % (xdiff, target_point.x, target_point.y))
            if target_point.x < -45.0:
                target_point = wm.ball.position
                target_point += ball_to_target.set_length_vector(11.0)
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": avoid circle(2). adjust len. new_pos=(%.2f %.2f)" % (target_point.x, target_point.y))
        if wm.game_mode_type == GameModeType.KickOff_ and ServerParam.kickoff_offside:
            target_point.x = min(-1.0e-5, target_point.x)
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": avoid kickoff offside. (%.2f %.2f)" % (target_point.x, target_point.y))
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": find sub target to avoid ball circle")
        adjusted_point = self.get_avoid_circle_point(wm, target_point,agent)
        dist_thr = wm.ball.dist_from_self * 0.1
        if dist_thr < 0.7:
            dist_thr = 0.7
        if adjusted_point != target_point and wm.ball.position.dist(target_point) > 10.0 and Tools.inertia_final_point(wm.myself,wm.myself.position,wm.myself.velocity).dist(adjusted_point) < dist_thr:
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": reverted to the first target point")
            adjusted_point = target_point
        agent.debugClient().setTarget(target_point)
        agent.debugClient().addCircle(target_point, dist_thr)
        if not Body_GoToPoint(adjusted_point, dist_thr, dash_power).execute(agent):
            body_angle = wm.ball.angle_from_self
            if body_angle < 0.0:
                body_angle -= 90.0
            else:
                body_angle += 90.0
            Body_TurnToAngle(body_angle).execute(agent)
        agent.setNeckAction(Neck_TurnToBall())