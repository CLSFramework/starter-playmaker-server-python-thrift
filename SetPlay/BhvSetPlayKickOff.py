from src.IAgent import IAgent
from SetPlay.BhvGoToPlacedBall import Bhv_GoToPlacedBall
from SetPlay.BhvSetPlay import Bhv_SetPlay
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D

class BhvSetPlayKickOff:
    
    def execute(agent: IAgent) -> bool:
        wm = agent.wm
        teammates = wm.teammates_from_ball()

        if not teammates or teammates[0].position.dist_from_self > wm.myself.dist_from_ball:
            BhvSetPlayKickOff.do_kick(agent)
        else:
            BhvSetPlayKickOff.do_move(agent)

        return True

    def do_kick(agent: IAgent):
        # Go to the ball position
        if Bhv_GoToPlacedBall(0.0).execute(agent):
            return
        
        # Wait
        if BhvSetPlayKickOff.do_kick_wait(agent):
            return
        
        # Kick
        wm = agent.wm
        max_ball_speed = ServerParam.i().max_power() * wm.myself.kick_rate

        target_point = Vector2D()
        ball_speed = max_ball_speed

        # Teammate not found
        if not wm.teammates_from_self():
            target_point.assign(ServerParam.i().pitch_half_length(),
                                (-1 + 2 * (wm.time().cycle() % 2)) * 0.8 * ServerParam.i().goal_half_width())
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: no teammate. target=({target_point.x:.1f} {target_point.y:.1f})")
        else:
            teammate = wm.teammates_from_self()[0]
            dist = teammate.dist_from_self()

            if dist > 35.0:
                # Too far
                target_point.assign(ServerParam.i().pitch_half_length(),
                                    (-1 + 2 * (wm.time().cycle() % 2)) * 0.8 * ServerParam.i().goal_half_width())
                agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: nearest teammate is too far. target=({target_point.x:.1f} {target_point.y:.1f})")
            else:
                target_point = teammate.inertia_final_point()
                ball_speed = min(max_ball_speed,
                                 calc_first_term_geom_series_last(1.8, dist, ServerParam.i().ball_decay()))
                agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: nearest teammate {teammate.unum()} target=({target_point.x:.1f} {target_point.y:.1f}) speed={ball_speed:.3f}")

        ball_vel = Vector2D.polar2vector(ball_speed, Vector2D(target_point - wm.ball.position).th())
        ball_next = wm.ball.position + ball_vel

        while wm.myself.pos().dist(ball_next) < wm.myself.player_type().kickable_area() + 0.2:
            ball_vel.set_length(ball_speed + 0.1)
            ball_speed += 0.1
            ball_next = wm.ball.position + ball_vel

            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: kickable in next cycle. adjust ball speed to {ball_speed:.3f}")

        ball_speed = min(ball_speed, max_ball_speed)

        agent.debug_client().set_target(target_point)

        # Enforce one step kick
        BodySmartKick(target_point, ball_speed, ball_speed * 0.96, 1).execute(agent)
        agent.set_neck_action(NeckScanField())

    def do_kick_wait(agent: IAgent) -> bool:
        wm = agent.wm
        real_set_play_count = int(wm.time().cycle() - wm.last_set_play_start_time().cycle())

        if real_set_play_count >= ServerParam.i().drop_ball_time() - 5:
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) real set play count = {real_set_play_count} > drop_time-10, force kick mode")
            return False

        if Bhv_SetPlay.is_delaying_tactics_situation(agent):
            agent.debug_client().add_message("KickOff:Delaying")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) delaying")

            BodyTurnToAngle(180.0).execute(agent)
            agent.set_neck_action(NeckScanField())
            return True

        if abs(wm.myself.body().abs()) < 175.0:
            agent.debug_client().add_message("KickOff:Turn")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) turn")

            BodyTurnToAngle(180.0).execute(agent)
            agent.set_neck_action(NeckScanField())
            return True

        if not wm.teammates_from_ball():
            agent.debug_client().add_message("KickOff:NoTeammate")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) no teammate")

            BodyTurnToAngle(180.0).execute(agent)
            agent.set_neck_action(NeckScanField())
            return True

        if len(wm.teammates_from_self()) < 9:
            agent.debug_client().add_message(f"FreeKick:Wait{real_set_play_count}")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) wait...")

            BodyTurnToAngle(180.0).execute(agent)
            agent.set_neck_action(NeckScanField())
            return True

        if wm.see_time() != wm.time() or wm.myself.stamina() < ServerParam.i().stamina_max() * 0.9:
            agent.debug_client().add_message("KickOff:WaitX")
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKickWait) no see or recover")

            BodyTurnToAngle(180.0).execute(agent)
            agent.set_neck_action(NeckScanField())
            return True

        return False

    def do_move(agent: IAgent):
        wm = agent.wm
        target_point = Strategy.i().get_home_position(wm, wm.myself.unum())
        target_point.x = min(-0.5, target_point.x)

        dash_power = Bhv_SetPlay.get_set_play_dash_power(agent)
        dist_thr = wm.ball.dist_from_self * 0.07
        if dist_thr < 1.0:
            dist_thr = 1.0

        if not BodyGoToPoint(target_point, dist_thr, dash_power).execute(agent):
            BodyTurnToBall().execute(agent)
        
        agent.set_neck_action(NeckScanField())
        agent.debug_client().set_target(target_point)
