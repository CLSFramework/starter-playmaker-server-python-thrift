from src.IAgent import IAgent
from SetPlay.BhvGoToPlacedBall import Bhv_GoToPlacedBall
from SetPlay.BhvSetPlay import BhvSetPlay
from soccer.ttypes import *
from pyrusgeom.vector_2d import Vector2D
from src.Tools import Tools
from src.setplay.BhvGoToPlacedBall import BhvGoToPlacedBall
from src.Strategy import Strategy

class BhvSetPlayKickOff:
    
    def execute(agent: IAgent):
        wm = agent.wm
        teammates = Tools.TeammatesFromBall(agent)

        if not teammates or teammates[0].position.dist_from_self > wm.myself.dist_from_ball:
            return BhvSetPlayKickOff.do_kick(agent)
        else:
            return BhvSetPlayKickOff.do_move(agent)

        return []

    def do_kick(agent: IAgent):
        # Go to the ball position
        actions = []
        actions += Bhv_GoToPlacedBall(0.0).execute(agent)
        
        # Wait
        actions += BhvSetPlayKickOff.do_kick_wait(agent)
            
        
        # Kick
        wm = agent.wm
        max_ball_speed = agent.serverParams.max_power * wm.myself.kick_rate

        target_point = Vector2D()
        ball_speed = max_ball_speed

        # Teammate not found
        if not Tools.TeammatesFromSelf(agent):
            target_point.assign(agent.serverParams.pitch_half_length, (-1 + 2 * (wm.cycle % 2)) * 0.8 * agent.serverParams.goal_width / 2)

        else:
            teammate = Tools.TeammatesFromSelf(agent)[0]
            dist = teammate.dist_from_self

            if dist > 35.0:
                # Too far
                target_point.assign(agent.serverParams.pitch_half_length, (-1 + 2 * (wm.cycle % 2)) * 0.8 * agent.serverParams.goal_width)
            else:
                target_point = teammate.inertia_final_point() #TODO
                ball_speed = min(max_ball_speed,
                                 Tools.calc_first_term_geom_series_last(1.8, dist, agent.serverParams.ball_decay))

        ball_vel = Vector2D.polar2vector(ball_speed, Vector2D(target_point - wm.ball.position).th())
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_next = ball_position + ball_vel
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        while self_position.dist(ball_next) < agent.playerTypes[agent.wm.myself.id].kickable_area + 0.2:
            ball_vel.set_length(ball_speed + 0.1)
            ball_speed += 0.1
            ball_next = ball_position + ball_vel

        ball_speed = min(ball_speed, max_ball_speed)


        # Enforce one step kick
        actions.append(PlayerAction(body_smart_kick=Body_SmartKick(RpcVector2D(target_point.x(), target_point.y()), ball_speed, ball_speed * 0.96, 1)))
        return actions
        
    def do_kick_wait(agent: IAgent) -> bool:
        actions = []
        wm = agent.wm
        real_set_play_count = int(wm.cycle - wm.last_set_play_start_time)

        if real_set_play_count >= agent.serverParams.drop_ball_time - 5:
            return []

        if BhvSetPlay.is_delaying_tactics_situation(agent):
            actions.append(PlayerAction(body_turn_to_angle=Body_TurnToAngle(180)))
            
        if abs(wm.myself.body_direction) < 175.0:
            actions.append(PlayerAction(body_turn_to_angle=Body_TurnToAngle(180)))

        if not Tools.TeammatesFromBall(agent):
            actions.append(PlayerAction(body_turn_to_angle=Body_TurnToAngle(180)))

        if len(Tools.TeammatesFromSelf(agent)) < 9:
            actions.append(PlayerAction(body_turn_to_angle=Body_TurnToAngle(180)))

        if wm.see_time != wm.cycle or wm.myself.stamina < agent.serverParams.stamina_max * 0.9:
            actions.append(PlayerAction(body_turn_to_angle=Body_TurnToAngle(180)))

        actions

    def do_move(agent: IAgent):
        wm = agent.wm
        actions = []
        target = Strategy.get_home_pos(wm, wm.myself.uniform_number)
        target_point = Vector2D(target.x, target.y)
        target_point.x = min(-0.5, target_point.x())

        dash_power = BhvSetPlay.get_set_play_dash_power(agent)
        dist_thr = wm.ball.dist_from_self * 0.07
        if dist_thr < 1.0:
            dist_thr = 1.0
        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(target_point.x(), target_point.y()), dist_thr, dash_power)))
        actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
        
        return actions
