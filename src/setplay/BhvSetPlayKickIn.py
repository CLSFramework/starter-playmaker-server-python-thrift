import math
from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D
from src.setplay.BhvGoToPlacedBall import BhvGoToPlacedBall
from src.Pass import Pass
from src.Tools import Tools
import math
from pyrusgeom.soccer_math import *
from src.setplay.BhvSetPlay import BhvSetPlay
from src.Strategy import Strategy
class BhvSetPlayKickIn:

    def Decision(agent: IAgent) -> bool:
        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: Bhv_SetPlayKickIn")

        if BhvSetPlayKickIn.is_kicker(agent):
            return BhvSetPlayKickIn.do_kick(agent)
        else:
            return BhvSetPlayKickIn.do_move(agent)

        return []

    def do_kick(agent: IAgent):
        wm = agent.wm
        actions = []
        # Go to the kick position
        ball_place_angle = -90.0 if wm.ball.position.y > 0.0 else 90.0
        actions += BhvGoToPlacedBall.Decision(ball_place_angle)

        # Wait
        if BhvSetPlayKickIn.do_kick_wait(agent):
            return []

        # Kick
        max_ball_speed = wm.myself.kick_rate * agent.serverParams.max_power

        # Pass
        actions += Pass.Decision(agent)

        # Kick to the nearest teammate
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        receiver: Player = Tools.GetTeammateNearestTo(ball_position)
        if receiver and receiver.dist_from_ball < 10.0 and abs(receiver.position.x) < agent.serverParams.pitch_half_length and abs(receiver.position.y) < agent.serverParams.pitch_half_width:

            target_point = Vector2D(receiver.inertia_final_point.x, receiver.inertia_final_point.y)
            target_point.set_x(target_point.x() + 0.5)
            ball_move_dist = ball_position.dist(target_point)
            ball_reach_step = math.ceil(calc_length_geom_series(max_ball_speed, ball_move_dist, agent.serverParams.ball_decay))
            ball_speed = 0.0

            if ball_reach_step > 3:
                ball_speed = calc_first_term_geom_series(ball_move_dist, agent.serverParams.ball_decay, ball_reach_step)
            else:
                ball_speed = Tools.calc_first_term_geom_series_last(1.4, ball_move_dist, agent.serverParams.ball_decay)
                ball_reach_step = math.ceil(calc_length_geom_series(ball_speed, ball_move_dist, agent.serverParams.ball_decay))

            ball_speed = min(ball_speed, max_ball_speed)
            actions.append(PlayerAction(body_kick_one_step=Body_KickOneStep(RpcVector2D(target_point.x(), target_point.y()), ball_speed)))
            return actions

        # Clear
        # Turn to ball
        if abs(wm.ball.angle_from_self - wm.myself.body_direction) > 1.5:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
            return actions

        # Advance ball
        if wm.myself.position.x < 20.0:
            actions.append(PlayerAction(body_advance_ball=Body_AdvanceBall()))
            return actions

        # Kick to the opponent side corner

        target_point = Vector2D(agent.serverParams.pitch_half_length - 2.0,
                                (agent.serverParams.pitch_half_width - 5.0) * (1.0 - (wm.myself.position.x / agent.serverParams.pitch_half_length)))

        if wm.myself.position.y < 0.0:
            target_point.set_y(target_point.y() * -1.0)
        
        # Enforce one step kick
        actions.append(PlayerAction(body_kick_one_step=Body_KickOneStep(RpcVector2D(target_point.x(), target_point.y()), agent.serverParams.ball_speed_max)))
        return actions
    

    def do_kick_wait(agent: IAgent) -> bool:
        wm = agent.wm

        real_set_play_count = wm.cycle - wm.last_set_play_start_time
        actions = []
        if real_set_play_count >= agent.serverParams.drop_ball_time - 5:
            return []

        if BhvSetPlay.is_delaying_tactics_situation(agent):
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(0, 0))))
            return actions

        if not Tools.TeammatesFromBall(agent):
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(0, 0))))
            return actions

        if wm.set_play_count <= 3:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
            return actions

        if wm.set_play_count >= 15 and wm.see_time == wm.cycle and wm.myself.stamina > agent.serverParams.stamina_max * 0.6:
            return []

        if wm.see_time != wm.cycle or wm.myself.stamina < agent.serverParams.stamina_max * 0.9:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
            return actions

        return actions

    def do_move(self, agent: IAgent):
        wm = agent.wm
        actions = []
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        target = Strategy.get_home_pos(agent, wm.myself.uniform_number)
        target_point = Vector2D(target.x, target.y)
        avoid_opponent = False
        
        if wm.myself.stamina > agent.serverParams.stamina_max * 0.9:
            nearest_opp = Tools.GetOpponentNearestToSelf(agent)
            nearest_opp_pos = Vector2D(nearest_opp.position.x, nearest_opp.position.y)
            
            if nearest_opp and nearest_opp_pos.dist(target_point) < 3.0:
                add_vec = ball_position - target_point
                add_vec.set_length(3.0)

                time_val = wm.cycle % 60
                if time_val < 20:
                    pass
                elif time_val < 40:
                    target_point += add_vec.rotated_vector(90.0)
                else:
                    target_point += add_vec.rotated_vector(-90.0)

                target_point.set_x(min(max(-agent.serverParams.pitch_half_length, target_point.x()), agent.serverParams.pitch_half_length()))
                target_point.set_y (min(max(-agent.serverParams.pitch_half_width, target_point.y), agent.serverParams.pitch_half_width))
                avoid_opponent = True

        dash_power = BhvSetPlay.get_set_play_dash_power(agent)
        dist_thr = wm.ball.dist_from_self * 0.07
        dist_thr = max(dist_thr, 1.0)
        tm = Tools.TeammatesFromBall(agent)
        if tm:
            kicker_ball_dist = tm[0].dist_from_ball
        else:
            1000
        
        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(target_point.x(), target_point.y()), dist_thr, dash_power)))
            # Already there
        if kicker_ball_dist > 1.0:
            actions.append(PlayerAction(turn=Turn(120)))
        else:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        self_velocity = Vector2D(wm.myself.velocity.x, wm.myself.velocity.y)
        my_inertia = Tools.inertia_final_point(agent.PlayerTypes[wm.myself.id], self_position, self_velocity)
        wait_dist_buf = (10.0 if avoid_opponent else ball_position.dist(target_point) * 0.2 + 6.0)

        if my_inertia.dist(target_point) > wait_dist_buf or wm.myself.stamina < agent.serverParams.stamina_max * 0.7:
            if not wm.myself.stamina_capacity == 0:
                actions.append(PlayerAction(say=WaitRequestMessage()))

        ''''if kicker_ball_dist > 3.0:
            agent.setViewAction(ViewWide())
            agent.setNeckAction(NeckScanField())
        elif wm.ball().distFromSelf() > 10.0 or kicker_ball_dist > 1.0:
            agent.setNeckAction(NeckTurnToBallOrScan(0))
        else:
            agent.setNeckAction(NeckTurnToBall())''' #TODO
            
        return actions