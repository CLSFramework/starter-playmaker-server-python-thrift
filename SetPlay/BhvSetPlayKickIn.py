import math
from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D

class BhvSetPlayKickIn:

    def execute(self, agent: IAgent) -> bool:
        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: Bhv_SetPlayKickIn")

        if self.is_kicker(agent):
            self.do_kick(agent)
        else:
            self.do_move(agent)

        return True

    def do_kick(self, agent: IAgent):
        wm = agent.wm

        # Go to the kick position
        ball_place_angle = -90.0 if wm.ball().pos().y > 0.0 else 90.0
        if self.go_to_placed_ball(ball_place_angle).execute(agent):
            return

        # Wait
        if self.do_kick_wait(agent):
            return

        # Kick
        max_ball_speed = wm.self().kickRate() * ServerParam.i().maxPower()

        # Pass
        self.basic_offensive_kick(agent, 1)

        # Kick to the nearest teammate
        receiver = wm.getTeammateNearestToBall(10)
        if receiver and receiver.distFromBall() < 10.0 and \
                abs(receiver.pos().x) < ServerParam.i().pitchHalfLength() and \
                abs(receiver.pos().y) < ServerParam.i().pitchHalfWidth():

            target_point = receiver.inertiaFinalPoint()
            target_point.x += 0.5

            ball_move_dist = wm.ball().pos().dist(target_point)
            ball_reach_step = math.ceil(self.calc_length_geom_series(max_ball_speed, ball_move_dist, ServerParam.i().ballDecay()))
            ball_speed = 0.0

            if ball_reach_step > 3:
                ball_speed = self.calc_first_term_geom_series(ball_move_dist, ServerParam.i().ballDecay(), ball_reach_step)
            else:
                ball_speed = self.calc_first_term_geom_series_last(1.4, ball_move_dist, ServerParam.i().ballDecay())
                ball_reach_step = math.ceil(self.calc_length_geom_series(ball_speed, ball_move_dist, ServerParam.i().ballDecay()))

            ball_speed = min(ball_speed, max_ball_speed)

            agent.debugClient().addMessage(f"KickIn:ForcePass{ball_speed:.3f}")
            agent.debugClient().setTarget(target_point)

            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: kick to nearest teammate ({target_point.x:.1f} {target_point.y:.1f}) speed={ball_speed:.2f}")
            self.body_kick_one_step(target_point, ball_speed).execute(agent)
            agent.setNeckAction(NeckScanField())
            return

        # Clear
        # Turn to ball
        if abs(wm.ball().angleFromSelf() - wm.self().body()) > 1.5:
            agent.debugClient().addMessage("KickIn:Advance:TurnToBall")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: clear. turn to ball")
            self.body_turn_to_ball().execute(agent)
            agent.setNeckAction(NeckScanField())
            return

        # Advance ball
        if wm.self().pos().x < 20.0:
            agent.debugClient().addMessage("KickIn:Advance")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: advance(1)")
            self.body_advance_ball().execute(agent)
            agent.setNeckAction(NeckScanField())
            return

        # Kick to the opponent side corner
        agent.debugClient().addMessage("KickIn:ForceAdvance")
        target_point = Vector2D(ServerParam.i().pitchHalfLength() - 2.0,
                                (ServerParam.i().pitchHalfWidth() - 5.0) * (1.0 - (wm.self().pos().x / ServerParam.i().pitchHalfLength())))

        if wm.self().pos().y < 0.0:
            target_point.y *= -1.0
        
        # Enforce one step kick
        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: advance(2) to ({target_point.x:.1f}, {target_point.y:.1f})")
        self.body_kick_one_step(target_point, ServerParam.i().ballSpeedMax()).execute(agent)
        agent.setNeckAction(NeckScanField())

    def do_kick_wait(self, agent: IAgent) -> bool:
        wm = agent.wm

        real_set_play_count = wm.time().cycle() - wm.lastSetPlayStartTime().cycle()

        if real_set_play_count >= ServerParam.i().dropBallTime() - 5:
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) real set play count = {real_set_play_count} > drop_time-10, force kick mode")
            return False

        if self.is_delaying_tactics_situation(agent):
            agent.debugClient().addMessage("KickIn:Delaying")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) delaying")
            self.body_turn_to_point(Vector2D(0.0, 0.0)).execute(agent)
            agent.setNeckAction(NeckScanField())
            return True

        if wm.teammatesFromBall().empty():
            agent.debugClient().addMessage("KickIn:NoTeammate")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) no teammate")
            self.body_turn_to_point(Vector2D(0.0, 0.0)).execute(agent)
            agent.setNeckAction(NeckScanField())
            return True

        if wm.getSetPlayCount() <= 3:
            agent.debugClient().addMessage(f"KickIn:Wait{wm.getSetPlayCount()}")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) wait teammates")
            self.body_turn_to_ball().execute(agent)
            agent.setNeckAction(NeckScanField())
            return True

        if wm.getSetPlayCount() >= 15 and wm.seeTime() == wm.time() and wm.self().stamina() > ServerParam.i().staminaMax() * 0.6:
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) set play count = {wm.getSetPlayCount()}, force kick mode")
            return False

        if wm.seeTime() != wm.time() or wm.self().stamina() < ServerParam.i().staminaMax() * 0.9:
            self.body_turn_to_ball().execute(agent)
            agent.setNeckAction(NeckScanField())
            agent.debugClient().addMessage(f"KickIn:Wait{wm.getSetPlayCount()}")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) no see or recover")
            return True

        return False

    def do_move(self, agent: IAgent):
        wm = agent.wm

        target_point = Strategy.i().getHomePosition(wm, wm.self().unum())

        avoid_opponent = False
        if wm.self().stamina() > ServerParam.i().staminaMax() * 0.9:
            nearest_opp = wm.getOpponentNearestToSelf(5)
            if nearest_opp and nearest_opp.pos().dist(target_point) < 3.0:
                add_vec = wm.ball().pos() - target_point
                add_vec.setLength(3.0)

                time_val = wm.time().cycle() % 60
                if time_val < 20:
                    pass
                elif time_val < 40:
                    target_point += add_vec.rotatedVector(90.0)
                else:
                    target_point += add_vec.rotatedVector(-90.0)

                target_point.x = min(max(-ServerParam.i().pitchHalfLength(), target_point.x), ServerParam.i().pitchHalfLength())
                target_point.y = min(max(-ServerParam.i().pitchHalfWidth(), target_point.y), ServerParam.i().pitchHalfWidth())
                avoid_opponent = True

        dash_power = self.get_set_play_dash_power(agent)
        dist_thr = wm.ball().distFromSelf() * 0.07
        dist_thr = max(dist_thr, 1.0)

        agent.debugClient().addMessage("KickInMove")
        agent.debugClient().setTarget(target_point)

        kicker_ball_dist = (wm.teammatesFromBall().front().distFromBall() if wm.teammatesFromBall() else 1000.0)

        if not self.body_go_to_point(target_point, dist_thr, dash_power).execute(agent):
            # Already there
            if kicker_ball_dist > 1.0:
                agent.doTurn(120.0)
            else:
                self.body_turn_to_ball().execute(agent)

        my_inertia = wm.self().inertiaFinalPoint()
        wait_dist_buf = (10.0 if avoid_opponent else wm.ball().pos().dist(target_point) * 0.2 + 6.0)

        if my_inertia.dist(target_point) > wait_dist_buf or wm.self().stamina() < ServerParam.i().staminaMax() * 0.7:
            if not wm.self().staminaModel().capacityIsEmpty():
                agent.debugClient().addMessage("Sayw")
                agent.addSayMessage(WaitRequestMessage())

        if kicker_ball_dist > 3.0:
            agent.setViewAction(ViewWide())
            agent.setNeckAction(NeckScanField())
        elif wm.ball().distFromSelf() > 10.0 or kicker_ball_dist > 1.0:
            agent.setNeckAction(NeckTurnToBallOrScan(0))
        else:
            agent.setNeckAction(NeckTurnToBall())
