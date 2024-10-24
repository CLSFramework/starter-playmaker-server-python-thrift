from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D
from src.setplay.BhvSetPlay import BhvSetPlay
from src.ClearBall import ClearBall
from src.Tools import Tools
from src.BhvBasicOffensiveKick import BhvBasicOffensiveKick
from src.Pass import Pass
from src.Strategy import Strategy
from src.ClearBall import ClearBall

class BhvSetPlayGoalKick:
    def __init__():
        pass
    
    def Decision(agent:IAgent):
        
        if BhvSetPlay.is_kicker(agent):
            return BhvSetPlayGoalKick.do_kick(agent)
        else:
            return BhvSetPlayGoalKick.do_move(agent)

    def do_kick(agent: IAgent):
        actions = []
        if BhvSetPlayGoalKick.do_second_kick(agent):
            return
        
        if BhvSetPlayGoalKick.go_to_placed_ball(agent):
            print(f"{__file__}: (doKick) go to ball")
            return
        
        if BhvSetPlayGoalKick.do_kick_wait(agent):
            return
        
        if BhvSetPlayGoalKick.do_pass(agent):
            return
        
        if BhvSetPlayGoalKick.do_kick_to_far_side(agent):
            return
        wm = agent.wm
        real_set_play_count = wm.cycle - agent.wm.last_set_play_start_time
        if real_set_play_count <= agent.serverParams.drop_ball_time - 10:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
            return actions
        actions += ClearBall.Decision(agent)
        print(f"{__file__}: clear ball")
        return actions

    def do_second_kick(agent:IAgent):
        wm = agent.wm
        actions = []
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_velocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)
        if wm.ball.position.x < -agent.serverParams.pitch_half_length + agent.serverParams.goal_area_length + 1.0 and abs(wm.ball.position.y) < agent.serverParams.goal_width * 0.5 + 1.0:
            return []
        
        if wm.myself.is_kickable:
            actions += BhvSetPlayGoalKick.do_pass(agent)
            actions += ClearBall.Decision(agent)
        
        actions += BhvSetPlayGoalKick.do_intercept(agent)
        
        ball_final = Tools.BallInertiaFinalPoint(ball_position, ball_velocity, agent.serverParams.ball_decay)
        
        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(ball_final.x(), ball_final.y(), 2.0, agent.serverParams.max_dash_power))))
        
        actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(0, 0))))
        
        return actions

    def do_kick_wait(self, agent:IAgent):
        wm = agent.wm
        actions = []
        real_set_play_count = wm.cycle - wm.last_set_play_start_time

        if real_set_play_count >= agent.serverParams.drop_ball_time - 10:
            return []

        if BhvSetPlay.is_delaying_tactics_situation(agent):
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
        
        if abs(wm.ball.angle_from_self - wm.myself.body_direction) > 3.0:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
        
        if wm.set_play_count <= 6:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))

        if wm.set_play_count <= 30 and Tools.TeammatesFromSelf(agent).length() == 0:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
        
        if wm.set_play_count >= 15 and wm.see_time == wm.cycle and wm.myself.stamina > agent.serverParams.stamina_max:
            return []
        
        if wm.set_play_count <= 3 or wm.see_time != wm.cycle or wm.myself.stamina < agent.serverParams.stamina_max * 0.9:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
            
        return actions

    def do_pass(agent:IAgent):
        return Pass.Decision(agent)

    def do_intercept(self, agent:IAgent):
        wm = agent.wm
        actions = []
        
        if wm.ball.position.x < -agent.serverParams.pitch_half_length + agent.serverParams.goal_area_length + 1.0 and abs(wm.ball.position.y) < agent.serverParams.goal_area_width * 0.5 + 1.0:
            return []
        
        if wm.myself.is_kickable:
            return []

        self_min = wm.intercept_table.self_reach_steps
        mate_min = wm.intercept_table.first_teammate_reach_steps
        if self_min > mate_min:
            return []
        
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_velocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)
        trap_pos = Tools.inertia_point(ball_position, ball_velocity, self_min, agent.serverParams.ball_decay)
        if (trap_pos.x() > agent.serverParams.our_penalty_area_line_x - 8.0 and abs(trap_pos.y()) > agent.serverParams.penalty_area_half_width - 5.0) or ball_velocity.r2() < 0.25:
            actions.append(PlayerAction(body_intercept=Body_Intercept()))
        
        return actions

    def do_move(agent:IAgent):
        actions = []
        actions += BhvSetPlayGoalKick.do_intercept(agent)
        
        wm = agent.wm
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        dash_power = BhvSetPlay.get_set_play_dash_power(agent)
        dist_thr = max(wm.ball.dist_from_self * 0.07, 1.0)

        target_rpc = Strategy.get_home_pos(wm, wm.myself.uniform_number)
        target_point = Vector2D(target_rpc.x, target_rpc.y)
        target_point.y() += wm.ball.position.y * 0.5

        if abs(target_point.y()) > agent.serverParams.pitch_half_width - 1.0:
            target_point.y() = (target_point.y() / abs(target_point.y())) * (agent.serverParams.pitch_half_width - 1.0)

        if wm.myself.stamina > agent.serverParams.stamina_max * 0.9:
            
            nearest_opp = Tools.GetOpponentNearestToSelf(agent)
            if nearest_opp and nearest_opp.dist_from_self < 3.0:
                add_vec: Vector2D = ball_position - target_point()
                add_vec.set_length(3.0)

                time_val = wm.cycle % 60
                if time_val < 20:
                    pass
                elif time_val < 40:
                    target_point += add_vec.rotated_vector(90.0)
                else:
                    target_point += add_vec.rotated_vector(-90.0)

                target_point.x() = min(max(-agent.serverParams.pitch_half_length, target_point.x()), agent.serverParams.pitch_half_length)
                target_point.y() = min(max(-agent.serverParams.pitch_half_width, target_point.y()), agent.serverParams.pitch_half_width)

        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(target_point.x(), target_point.y()), dist_thr, dash_power)))
        actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
        
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        if (self_position.dist(target_point) > ball_position.dist(target_point) * 0.2 + 6.0 or wm.myself.stamina < agent.serverParams.stamina_max * 0.7):
            if not wm.myself.stamina_capacity == 0: #TODO
                pass

        return actions

    def do_kick_to_far_side(agent:IAgent):
        wm = agent.wm
        actions = []
        target_point = Vector2D(agent.serverParams.our_penalty_area_line_x - 5.0, agent.serverParams.penalty_area_half_width)
        if wm.ball.position.y > 0.0:
            target_point.y *= -1.0
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_move_dist = ball_position.dist(target_point)
        ball_first_speed = Tools.calc_first_term_geom_series_last(0.7, ball_move_dist, agent.serverParams.ball_decay)
        ball_first_speed = min(agent.serverParams.ball_speed_max, ball_first_speed)
        ball_first_speed = min(wm.myself.kick_rate * agent.serverParams.max_power, ball_first_speed)

        accel = target_point - ball_position
        accel.set_length(ball_first_speed)

        kick_power = min(agent.serverParams.max_power, accel.r() / wm.myself.kick_rate)
        kick_angle = accel.th()
        actions.append(PlayerAction(kick=Kick(kick_power, kick_angle.degree() - wm.myself.body_direction)))
        return actions
