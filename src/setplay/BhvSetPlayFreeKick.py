import math
from src.IAgent import IAgent
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D
from src.setplay.BhvSetPlay import BhvSetPlay
from src.setplay.BhvGoToPlacedBall import BhvGoToPlacedBall
from pyrusgeom.soccer_math import calc_length_geom_series
from pyrusgeom.soccer_math import calc_first_term_geom_series
from src.Pass import Pass
from src.Tools import Tools
import math
from src.ClearBall import ClearBall
from pyrusgeom.angle_deg import AngleDeg
from src.Strategy import *
class BhvSetPlayFreeKick:
    def __init__(self):
        pass
    
    def Decision(self, agent: IAgent):
        
        if BhvSetPlay.is_kicker(agent):
            return self.doKick(agent)
        else:
            return self.doMove(agent)

    def doKick(self, agent:IAgent):
        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: (doKick)")
        actions = []
        # go to the ball position
        actions += BhvGoToPlacedBall(0.0).Decision(agent)


        actions += self.doKickWait(agent)

        # kick
        wm = agent.wm
        max_ball_speed = wm.myself.kick_rate * agent.serverParams.max_power

        # pass
        actions += Pass.Decision(agent)

        # kick to the nearest teammate

        nearest_teammate: Player = Tools.GetTeammateNearestToSelf(False)
        if nearest_teammate and nearest_teammate.dist_from_self < 20.0 and (
            nearest_teammate.position.x > -30.0 or nearest_teammate.dist_from_self < 10.0):
            nearest_teammate_pos = Vector2D(nearest_teammate.position.x, nearest_teammate.position.y)
            nearest_teammate_vel = Vector2D(nearest_teammate.velocity.x, nearest_teammate.velocity.y)
            target_point = Tools.inertia_final_point(nearest_teammate, nearest_teammate_pos, nearest_teammate_vel)
            target_point.x += 0.5
            ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
            ball_move_dist = ball_position.dist(target_point)
            ball_reach_step = math.ceil(calc_length_geom_series(max_ball_speed, ball_move_dist, agent.serverParams.ball_decay))
            ball_speed = 0.0
            if ball_reach_step > 3:
                ball_speed = calc_first_term_geom_series(ball_move_dist, ServerParam.i().ballDecay(), ball_reach_step)
            else:
                ball_speed = Tools.calc_first_term_geom_series_last(1.4, ball_move_dist, agent.serverParams.ball_decay)
                ball_reach_step = math.ceil(calc_length_geom_series(ball_speed, ball_move_dist, agent.serverParams.ball_decay))

            ball_speed = min(ball_speed, max_ball_speed)
            actions.append(PlayerAction(body_kick_one_step=Body_KickOneStep(target_point, ball_speed)))

        # clear
        if abs(wm.ball.angle_from_self - wm.myself.body()) > 1.5:
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))

        actions.append(ClearBall.Decision(agent))
        return actions


    def doKickWait(agent:IAgent):
        wm = agent.wm
        actions = []
        real_set_play_count = wm.cycle - wm.last_set_play_start_time

        if real_set_play_count >= agent.serverParams.drop_ball_time - 5:
            return []

        face_point = Vector2D(40.0, 0.0)
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        face_angle = Vector2D(face_point - self_position).th()

        if wm.stoped_cycle != 0:
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(face_point)))

        if BhvSetPlay.is_delaying_tactics_situation(agent):
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(face_point)))

        if not Tools.TeammatesFromBall(agent):
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(face_point)))

        if wm.set_play_count <= 3:
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(face_point)))

        if wm.set_play_count >= 15 and wm.see_time == wm.cycle and wm.myself.stamina > agent.serverParams.stamina_max * 0.6:
            return []
        
        if abs(face_angle - wm.myself.body_direction) > 5.0:
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(face_point)))

        if (wm.see_time != wm.cycle or
                wm.myself.stamina < agent.serverParams.stamina_max * 0.9):
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall().execute(agent)))

        return actions

    def do_move(agent:IAgent):
        wm = agent.wm
        actions = []
        target_point_rpc = Strategy.get_home_pos(wm, wm.myself.uniform_number)
        target_point = Vector2D(target_point_rpc.x, target_point_rpc.y)
        ball_positions = Vector2D(wm.ball.position.x, wm.ball.position.y)
        self_positions = Vector2D(wm.myself.position.x, wm.myself.position.y)
        if wm.set_play_count > 0 and wm.myself.stamina > agent.serverParams.stamina_max * 0.9:
            nearest_opp = Tools.OpponentsFromSelf(agent)[0]

            if nearest_opp and nearest_opp.dist_from_self < 3.0:
                add_vec = ball_positions - target_point
                add_vec.set_length(3.0)

                time_val = wm.cycle % 60
                if time_val < 20:
                    pass
                elif time_val < 40:
                    target_point += add_vec.rotated_vector(90.0)
                else:
                    target_point += add_vec.rotated_vector(-90.0)

                target_point.x = min(max(-agent.serverParams.pitch_half_length, target_point.x), agent.serverParams.pitch_half_length)
                target_point.y = min(max(-agent.serverParams.pitch_half_width, target_point.y), agent.serverParams.pitch_half_width)

        target_point.x = min(target_point.x, wm.offside_line_x - 0.5)

        dash_power = BhvSetPlay().get_set_play_dash_power(agent)
        dist_thr = wm.ball.dist_from_self * 0.07
        if dist_thr < 1.0:
            dist_thr = 1.0

        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(target_point, dist_thr, dash_power)))
        actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))

        if self_positions.dist(target_point) > max(ball_positions.dist(target_point) * 0.2, dist_thr) + 6.0 or wm.myself.stamina < agent.serverParams.stamina_max * 0.7:
            if not wm.myself.stamina_capacity == 0: #TODO stamina model
                actions.append(PlayerAction(WaitRequestMessage()))

        return actions


