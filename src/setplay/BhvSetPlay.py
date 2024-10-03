from src.IAgent import IAgent
import math
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.segment_2d import Segment2D
from pyrusgeom.circle_2d import Circle2D

class Bhv_SetPlay:
    def __init__(self):
        pass

    def execute(self, agent: IAgent):
        wm = agent.wm
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": Bhv_SetPlay")

        if wm.self().goalie():
            if wm.gameMode().type() != GameMode.BackPass_ and wm.gameMode().type() != GameMode.IndFreeKick_:
                Bhv_GoalieFreeKick().execute(agent)
            else:
                Bhv_SetPlayIndirectFreeKick().execute(agent)
            return True

        if wm.gameMode().type() == GameMode.KickOff_:
            if wm.gameMode().side() == wm.ourSide():
                return Bhv_SetPlayKickOff().execute(agent)
            else:
                self.doBasicTheirSetPlayMove(agent)
                return True

        if wm.gameMode().type() in [GameMode.KickIn_, GameMode.CornerKick_]:
            if wm.gameMode().side() == wm.ourSide():
                return Bhv_SetPlayKickIn().execute(agent)
            else:
                self.doBasicTheirSetPlayMove(agent)
                return True

        if wm.gameMode().type() == GameMode.GoalKick_:
            if wm.gameMode().side() == wm.ourSide():
                return Bhv_SetPlayGoalKick().execute(agent)
            else:
                return Bhv_TheirGoalKickMove().execute(agent)

        if wm.gameMode().type() in [GameMode.BackPass_, GameMode.IndFreeKick_]:
            return Bhv_SetPlayIndirectFreeKick().execute(agent)

        if wm.gameMode().type() in [GameMode.FoulCharge_, GameMode.FoulPush_]:
            if (wm.ball.position.x < ServerParam.i().ourPenaltyAreaLineX() + 1.0 and
                    abs(wm.ball.position.y) < ServerParam.i().penaltyAreaHalfWidth() + 1.0):
                return Bhv_SetPlayIndirectFreeKick().execute(agent)
            elif (wm.ball.position.x > ServerParam.i().theirPenaltyAreaLineX() - 1.0 and
                  abs(wm.ball.position.y) < ServerParam.i().penaltyAreaHalfWidth() + 1.0):
                return Bhv_SetPlayIndirectFreeKick().execute(agent)

        if wm.gameMode().isOurSetPlay(wm.ourSide()):
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": our set play")
            return Bhv_SetPlayFreeKick().execute(agent)
        else:
            self.doBasicTheirSetPlayMove(agent)
            return True

        return False

    def get_set_play_dash_power(self, agent: IAgent):
        wm = agent.wm
        if not wm.gameMode().isOurSetPlay(wm.ourSide()):
            target_point = Strategy.i().getHomePosition(wm, wm.self().unum())
            if target_point.x > wm.self().pos().x:
                if (wm.ball.position.x < -30.0 and
                        target_point.x < wm.ball.position.x):
                    return wm.self().getSafetyDashPower(ServerParam.i().maxDashPower())
                rate = 0.0
                if wm.self().stamina() > ServerParam.i().staminaMax() * 0.8:
                    rate = 1.5 * wm.self().stamina() / ServerParam.i().staminaMax()
                else:
                    rate = 0.9 * (wm.self().stamina() - ServerParam.i().recoverDecThrValue()) / ServerParam.i().staminaMax()
                    rate = max(0.0, rate)
                return (wm.self().playerType().staminaIncMax() *
                        wm.self().recovery() *
                        rate)
        return wm.self().getSafetyDashPower(ServerParam.i().maxDashPower())

    def can_go_to(self, count, wm, ball_circle, target_point):
        move_line = Segment2D(wm.self().pos(), target_point)
        n_intersection = ball_circle.intersection(move_line, None, None)
        agent.add_log_text(LoggerLevel.TEAM, "%d: (can_go_to) check target=(%.2f %.2f) intersection=%d" % (count, target_point.x, target_point.y, n_intersection))
        dlog.addLine(LoggerLevel.TEAM, wm.self().pos(), target_point, "#0000ff")
        num = str(count)
        dlog.addMessage(LoggerLevel.TEAM, target_point, num, "#0000ff")
        if n_intersection == 0:
            agent.add_log_text(LoggerLevel.TEAM, "%d: (can_go_to) ok(1)" % count)
            return True
        if n_intersection == 1:
            angle = (target_point - wm.self().pos()).th()
            agent.add_log_text(LoggerLevel.TEAM, "%d: (can_go_to) intersection=1 angle_diff=%.1f" % (count, (angle - wm.ball().angleFromSelf()).abs()))
            if (angle - wm.ball().angleFromSelf()).abs() > 80.0:
                agent.add_log_text(LoggerLevel.TEAM, "%d: (can_go_to) ok(2)" % count)
                return True
        return False

    def get_avoid_circle_point(self, wm, target_point):
        SP = ServerParam.i()
        avoid_radius = SP.centerCircleR() + wm.self().playerType().playerSize()
        ball_circle = Circle2D(wm.ball.position, avoid_radius)
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (get_avoid_circle_point) first_target=(%.2f %.2f)" % (target_point.x, target_point.y))
        dlog.addCircle(LoggerLevel.TEAM, wm.ball.position, avoid_radius, "#ffffff")
        if self.can_go_to(-1, wm, ball_circle, target_point):
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (get_avoid_circle_point) ok, first point")
            return target_point
        target_angle = (target_point - wm.self().pos()).th()
        ball_target_angle = (target_point - wm.ball.position).th()
        ball_is_left = wm.ball().angleFromSelf().isLeftOf(target_angle)
        ANGLE_DIVS = 6
        subtargets = []
        angle_step = 1 if ball_is_left else -1
        count = 0
        a = angle_step
        for i in range(1, ANGLE_DIVS):
            angle = ball_target_angle + (180.0 / ANGLE_DIVS) * a
            new_target = wm.ball.position + Vector2D.from_polar(avoid_radius + 1.0, angle)
            agent.add_log_text(LoggerLevel.TEAM, "%d: a=%d angle=%.1f (%.2f %.2f)" % (count, a, angle.degree(), new_target.x, new_target.y))
            if abs(new_target.x) > SP.pitchHalfLength() + SP.pitchMargin() - 1.0 or abs(new_target.y) > SP.pitchHalfWidth() + SP.pitchMargin() - 1.0:
                agent.add_log_text(LoggerLevel.TEAM, "%d: out of field" % count)
                break
            if self.can_go_to(count, wm, ball_circle, new_target):
                return new_target
            a += angle_step
            count += 1
        a = -angle_step
        for i in range(1, ANGLE_DIVS * 2):
            angle = ball_target_angle + (180.0 / ANGLE_DIVS) * a
            new_target = wm.ball.position + Vector2D.from_polar(avoid_radius + 1.0, angle)
            agent.add_log_text(LoggerLevel.TEAM, "%d: a=%d angle=%.1f (%.2f %.2f)" % (count, a, angle.degree(), new_target.x, new_target.y))
            if abs(new_target.x) > SP.pitchHalfLength() + SP.pitchMargin() - 1.0 or abs(new_target.y) > SP.pitchHalfWidth() + SP.pitchMargin() - 1.0:
                agent.add_log_text(LoggerLevel.TEAM, "%d: out of field" % count)
                break
            if self.can_go_to(count, wm, ball_circle, new_target):
                return new_target
            a -= angle_step
            count += 1
        return target_point

    def is_kicker(self, agent: IAgent):
        wm = agent.wm
        if wm.gameMode().type() == GameMode.GoalieCatch_ and wm.gameMode().side() == wm.ourSide() and not wm.self().goalie():
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) goalie free kick")
            return False
        kicker_unum = 0
        min_dist2 = float('inf')
        second_kicker_unum = 0
        second_min_dist2 = float('inf')
        for unum in range(1, 12):
            if unum == wm.ourGoalieUnum():
                continue
            home_pos = Strategy.i().getHomePosition(wm, unum)
            if not home_pos.isValid():
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
            kicker = wm.ourPlayer(kicker_unum)
        if second_kicker_unum != 0:
            second_kicker = wm.ourPlayer(second_kicker_unum)
        if not kicker:
            if not wm.teammatesFromBall().empty() and wm.teammatesFromBall()[0].distFromBall() < wm.ball().distFromSelf() * 0.9:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) first kicker")
                return False
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) self(1)")
            return True
        if kicker and second_kicker and (kicker.unum() == wm.self().unum() or second_kicker.unum() == wm.self().unum()):
            if math.sqrt(min_dist2) < math.sqrt(second_min_dist2) * 0.95:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) kicker->unum=%d  (1)" % kicker.unum())
                return kicker.unum() == wm.self().unum()
            elif kicker.distFromBall() < second_kicker.distFromBall() * 0.95:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) kicker->unum=%d  (2)" % kicker.unum())
                return kicker.unum() == wm.self().unum()
            elif second_kicker.distFromBall() < kicker.distFromBall() * 0.95:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) kicker->unum=%d  (3)" % kicker.unum())
                return second_kicker.unum() == wm.self().unum()
            elif not wm.teammatesFromBall().empty() and wm.teammatesFromBall()[0].distFromBall() < wm.self().distFromBall() * 0.95:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) other kicker")
                return False
            else:
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) self(2)")
                return True
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": (is_kicker) kicker->unum=%d" % kicker.unum())
        return kicker.unum() == wm.self().unum()

    def is_delaying_tactics_situation(self, agent: IAgent):
        wm = agent.wm
        real_set_play_count = wm.time().cycle() - wm.lastSetPlayStartTime().cycle()
        wait_buf = 15 if wm.gameMode().type() == GameMode.GoalKick_ else 2
        if real_set_play_count >= ServerParam.i().dropBallTime() - wait_buf:
            return False
        our_score = wm.gameMode().scoreLeft() if wm.ourSide() == LEFT else wm.gameMode().scoreRight()
        opp_score = wm.gameMode().scoreRight() if wm.ourSide() == LEFT else wm.gameMode().scoreLeft()
        if wm.audioMemory().recoveryTime().cycle() >= wm.time().cycle() - 10:
            if our_score > opp_score:
                return True
        cycle_thr = max(0, ServerParam.i().nrNormalHalfs() * (ServerParam.i().halfTime() * 10) - 500)
        if wm.time().cycle() < cycle_thr:
            return False
        if our_score > opp_score and our_score - opp_score <= 1:
            return True
        return False

    def doBasicTheirSetPlayMove(self, agent: IAgent):
        wm = agent.wm
        target_point = Strategy.i().getHomePosition(wm, wm.self().unum())
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": their set play. HomePosition=(%.2f, %.2f)" % (target_point.x, target_point.y))
        dash_power = self.get_set_play_dash_power(agent)
        ball_to_target = target_point - wm.ball.position
        if ball_to_target.r() < 11.0:
            xdiff = math.sqrt(math.pow(11.0, 2) - math.pow(ball_to_target.y, 2))
            target_point.x = wm.ball.position.x - xdiff
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": avoid circle(1). adjust x. x_diff=%.1f newPos=(%.2f %.2f)" % (xdiff, target_point.x, target_point.y))
            if target_point.x < -45.0:
                target_point = wm.ball.position
                target_point += ball_to_target.setLengthVector(11.0)
                agent.add_log_text(LoggerLevel.TEAM, __file__ + ": avoid circle(2). adjust len. new_pos=(%.2f %.2f)" % (target_point.x, target_point.y))
        if wm.gameMode().type() == GameMode.KickOff_ and ServerParam.i().kickoffOffside():
            target_point.x = min(-1.0e-5, target_point.x)
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": avoid kickoff offside. (%.2f %.2f)" % (target_point.x, target_point.y))
        agent.add_log_text(LoggerLevel.TEAM, __file__ + ": find sub target to avoid ball circle")
        adjusted_point = self.get_avoid_circle_point(wm, target_point)
        dist_thr = wm.ball().distFromSelf() * 0.1
        if dist_thr < 0.7:
            dist_thr = 0.7
        if adjusted_point != target_point and wm.ball.position.dist(target_point) > 10.0 and wm.self().inertiaFinalPoint().dist(adjusted_point) < dist_thr:
            agent.add_log_text(LoggerLevel.TEAM, __file__ + ": reverted to the first target point")
            adjusted_point = target_point
        agent.debugClient().setTarget(target_point)
        agent.debugClient().addCircle(target_point, dist_thr)
        if not Body_GoToPoint(adjusted_point, dist_thr, dash_power).execute(agent):
            body_angle = wm.ball().angleFromSelf()
            if body_angle.degree() < 0.0:
                body_angle -= 90.0
            else:
                body_angle += 90.0
            Body_TurnToAngle(body_angle).execute(agent)
        agent.setNeckAction(Neck_TurnToBall())