from src.IAgent import IAgent
import math
from soccer.ttypes import *
from src.setplay.BhvSetPlayKickOff import *
from src.setplay.BhvTheirGoalKickMove import *
from src.setplay.BhvSetPlayFreeKick import *
from src.setplay.BhvSetPlayGoalKick import *
from src.setplay.BhvSetPlayKickIn import *
from src.setplay.BhvSetPlayIndirectFreeKick import *
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.segment_2d import Segment2D
from pyrusgeom.circle_2d import Circle2D

class BhvSetPlay:
    def __init__(self):
        pass

    def Decision(agent: IAgent):
        wm = agent.wm

        if wm.myself.is_goalie:
            if wm.game_mode_type != GameModeType.BackPass_ and wm.game_mode_type != GameModeType.IndFreeKick_:
                return BhvSetPlayGoalKick.Decision(agent)
            else:
                return BhvSetPlayIndirectFreeKick.Decision(agent)
            return []

        if wm.game_mode_type == GameModeType.KickOff_:
            if wm.game_mode_side == wm.our_side:
                return BhvSetPlayKickOff.Decision(agent)
            else:
                return BhvSetPlay.doBasicTheirSetPlayMove(agent)


        if wm.game_mode_type in [GameModeType.KickIn_, GameModeType.CornerKick_]:
            if wm.game_mode_side == wm.our_side:
                return BhvSetPlayKickIn.Decision(agent)
            else:
                return BhvSetPlay.doBasicTheirSetPlayMove(agent)

        if wm.game_mode_type == GameModeType.GoalKick_:
            if wm.game_mode_side == wm.our_side:
                return BhvSetPlayGoalKick.Decision(agent)
            else:
                return BhvTheirGoalKickMove.Decision(agent)

        if wm.game_mode_type in [GameModeType.BackPass_, GameModeType.IndFreeKick_]:
            return BhvSetPlayIndirectFreeKick.Decision(agent)

        if wm.game_mode_type in [GameModeType.FoulCharge_, GameModeType.FoulPush_]:
            if (wm.ball.position.x < agent.serverParams.our_penalty_area_line_x + 1.0 and abs(wm.ball.position.y) < agent.serverParams.penalty_area_half_width + 1.0):
                return BhvSetPlayIndirectFreeKick.Decision(agent)
            elif (wm.ball.position.x > agent.serverParams.their_penalty_area_line_x - 1.0 and
                  abs(wm.ball.position.y) < agent.serverParams.penalty_area_half_width + 1.0):
                return BhvSetPlayIndirectFreeKick.Decision(agent)

        if wm.is_our_set_play:
            return BhvSetPlayFreeKick.Decision(agent)
        else:
            BhvSetPlay.doBasicTheirSetPlayMove(agent)

        return []

    def get_set_play_dash_power(agent: IAgent):
        wm = agent.wm
        if not wm.is_our_set_play:
            target_point = Strategy.get_home_pos(agent, wm.myself.uniform_number)
            if target_point.x > wm.myself.position.x:
                if (wm.ball.position.x < -30.0 and
                        target_point.x < wm.ball.position.x):
                    return wm.myself.get_safety_dash_power
                rate = 0.0
                if wm.myself.stamina > agent.serverParams.stamina_max * 0.8:
                    rate = 1.5 * wm.myself.stamina / agent.serverParams.stamina_max
                else:
                    rate = 0.9 * (wm.myself.stamina -  agent.serverParams.recover_dec_thr) /  agent.serverParams.stamina_max
                    rate = max(0.0, rate)
                return (agent.playerTypes[wm.myself.id].stamina_inc_max * wm.myself.recovery * rate)
        return wm.myself.get_safety_dash_power

    def can_go_to(agent:IAgent, count, wm, ball_circle: Circle2D, target_point:Vector2D) -> bool:
        wm = agent.wm
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        move_line = Segment2D(self_position, target_point)
        n_intersection = ball_circle.intersection(move_line, None, None)

        num = str(count)

        if n_intersection == 0:
            return True
        
        if n_intersection == 1:
            angle = Vector2D(target_point - self_position).th()
            if abs(angle - wm.ball.angle_from_self) > 80.0:
                return True
        return False

    def get_avoid_circle_point(wm, target_point,agent:IAgent):
        SP = ServerParam
        wm = agent.wm
        avoid_radius = SP.center_circle_r + agent.playerTypes[wm.myself.id].player_size
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_circle = Circle2D(ball_position, avoid_radius)
        if BhvSetPlay.can_go_to(agent,-1, wm, ball_circle, target_point):
            return target_point
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        target_angle = Vector2D(target_point - self_position).th()
        ball_target_angle = Vector2D(target_point - wm.ball.position).th()
        ball_ang = AngleDeg(wm.ball.angle_from_self)
        ball_is_left = ball_ang.is_left_of(target_angle)
        ANGLE_DIVS = 6
        subtargets = []
        angle_step = 1 if ball_is_left else -1
        count = 0
        a = angle_step
        for i in range(1, ANGLE_DIVS):
            angle = ball_target_angle + (180.0 / ANGLE_DIVS) * a
            new_target = Vector2D(wm.ball.position + Vector2D.from_polar(avoid_radius + 1.0, angle))

            if abs(new_target.x()) > SP.pitch_half_length + SP.pith_margin - 1.0 or abs(new_target.y) > SP.pitch_half_width + SP.pitchMargin() - 1.0: #TODO pith_margin
                break
            if BhvSetPlay.can_go_to(count, wm, ball_circle, new_target, agent):
                return new_target
            a += angle_step
            count += 1
        a = -angle_step
        for i in range(1, ANGLE_DIVS * 2):
            angle = ball_target_angle + (180.0 / ANGLE_DIVS) * a
            new_target = Vector2D(ball_position + Vector2D.from_polar(avoid_radius + 1.0, angle))

            if abs(new_target.x()) > SP.pitch_half_length + SP.pitchMargin - 1.0 or abs(new_target.y()) > SP.pitch_half_width + SP.pitchMargin() - 1.0: #TODO
                break
            if BhvSetPlay.can_go_to(count, wm, ball_circle, new_target, agent):
                return new_target
            a -= angle_step
            count += 1
        return target_point

    def is_kicker(agent: IAgent):
        wm = agent.wm
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        if wm.game_mode_type == GameModeType.GoalieCatch_ and wm.game_mode_side == wm.our_side and not wm.myself.is_goalie:
            return False
        kicker_unum = 0
        min_dist2 = float('inf')
        second_kicker_unum = 0
        second_min_dist2 = float('inf')
        for unum in range(1, 12):
            if unum == wm.our_goalie_uniform_number:
                continue
            home_pos = Vector2D(Strategy.get_home_pos(agent, unum).x, Strategy.get_home_pos(agent, unum).y)
            if not home_pos.is_valid:
                continue
            d2 = home_pos.dist2(ball_position)
            if d2 < second_min_dist2:
                second_kicker_unum = unum
                second_min_dist2 = d2
                if second_min_dist2 < min_dist2:
                    second_kicker_unum, kicker_unum = kicker_unum, second_kicker_unum
                    second_min_dist2, min_dist2 = min_dist2, second_min_dist2

        kicker = None
        second_kicker = None
        if kicker_unum != 0:
            kicker = wm.teammates[kicker_unum]
        if second_kicker_unum != 0:
            second_kicker = wm.teammates[second_kicker_unum]
        if not kicker:
            if Tools.TeammatesFromBall(agent) and Tools.TeammatesFromBall(agent)[0].dist_from_ball < wm.ball.dist_from_self * 0.9:
                return False

            return True
        if kicker and second_kicker and (kicker.uniform_number == wm.myself.uniform_number or second_kicker.uniform_number == wm.myself.uniform_number):
            teammates_from_ball = Tools.TeammatesFromBall(agent)
            if math.sqrt(min_dist2) < math.sqrt(second_min_dist2) * 0.95:
                return kicker.uniform_number == wm.myself.uniform_number
            elif kicker.dist_from_ball < second_kicker.dist_from_ball * 0.95:
                return kicker.uniform_number == wm.myself.uniform_number
            elif second_kicker.dist_from_ball < kicker.dist_from_ball * 0.95:
                return second_kicker.uniform_number == wm.myself.uniform_number
            
            elif teammates_from_ball and teammates_from_ball[0].dist_from_ball < wm.myself.dist_from_ball * 0.95:
                return False
            else:
                return True
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