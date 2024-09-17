from src.IAgent import IAgent
from soccer.ttypes import PlayerAction, CardType, Tackle, LoggerLevel,Neck_TurnToBallOrScan
from src.Tools import Tools
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.soccer_math import inertia_n_step_point
from pyrusgeom.ray_2d import Ray2D
from pyrusgeom.line_2d import Line2D

class BhvBasicTackle:
    
    def __init__(self, min_prob: float, body_thr: float):
        self.min_prob = min_prob
        self.body_thr = body_thr

    def Decision(self, agent: IAgent):
        
        wm = agent.wm
        use_foul = False
        tackle_prob = wm.myself.tackle_probability
        if wm.myself.card == CardType.NO_CARD and (wm.ball.position.x > agent.serverParams.our_penalty_area_line_x + 0.5 or abs(wm.ball.position.y) > agent.serverParams.penalty_area_half_width + 0.5) and tackle_prob < wm.myself.foul_probability:
            tackle_prob = wm.myself.foul_probability
            use_foul = True
            
        if tackle_prob < self.min_prob:
            return
        
        self_min = wm.intercept_table.self_reach_steps
        mate_min = wm.intercept_table.first_teammate_reach_steps
        opp_min = wm.intercept_table.first_opponent_reach_steps
        
        self_pos = Vector2D(wm.myself.position.x, wm.myself.position.y)
        ball_pos = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_velocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)
        
        self_reach_point = inertia_n_step_point(ball_pos, ball_velocity, self_min, agent.serverParams.ball_decay)
        
        ball_will_be_in_our_goal = False
        
        if self_reach_point.x() < -agent.serverParams.pitch_half_length:
            
            ball_ray = Ray2D(ball_pos, ball_velocity.th())
            goal_line = Line2D(Vector2D(-agent.serverParams.pitch_half_length, 10.0), Vector2D(-agent.serverParams.pitch_half_length, -10.0))
            
            intersect = ball_ray.intersection(goal_line)
            
            if intersect.is_valid() and intersect.abs_y() < (agent.serverParams.goal_width / 2) + 1:
                ball_will_be_in_our_goal = True
                
        if opp_min < 2 or ball_will_be_in_our_goal or (opp_min < self_min - 3 and opp_min < mate_min - 3) or (self_min >= 5 and ball_pos.dist2(Vector2D(agent.serverParams.pitch_half_length, 0)) < 100) and ((Vector2D(agent.serverParams.pitch_half_length, 0) - self_pos).th() - wm.myself.body_direction).abs() < 45:
            # Try tackle
            pass
        else:
            return

        return BhvBasicTackle.ExecuteOldVersion(self, agent, use_foul)

    
    def ExecuteOldVersion(self, agent: IAgent, use_foul: bool):
        
        wm = agent.wm
        tackle_power = agent.serverParams.max_tackle_power
        
        if abs(wm.myself.body_direction) < self.body_thr:
            return PlayerAction(tackle=Tackle(tackle_power, use_foul))
            
        tackle_power = -agent.serverParams.max_back_tackle_power
        
        if tackle_power < 0.0 and abs(wm.myself.body_direction) > 180 - self.body_thr:
            return PlayerAction(tackle=Tackle(tackle_power))
        
        return
        
    def ExecuteV12(self, agent: IAgent, use_foul: bool):

        s_last_execute_time =  agent.wm.cycle
        s_result = False
        s_best_angle = AngleDeg(0,0)

        wm = agent.wm

        if s_last_execute_time == wm.time():
            agent.add_log_text(LoggerLevel.TEAM, f": called several times")
            if s_result:
                agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: executeV12() tackle angle={s_best_angle.degree()}")
                agent.add_log_message(LoggerLevel.TEAM,f"BasicTackle{s_best_angle.degree()}", agent.wm.myself.position.x, agent.wm.myself.position.y - 2, '\033[31m')

                tackle_dir = (s_best_angle - wm.myself.body_direction).degree()
                return PlayerAction(tackle=Tackle(tackle_dir, use_foul))
                #actions.append(PlayerAction(neck_turn_to_ball_or_scan=Neck_TurnToBallOrScan(0)))

        s_last_execute_time = wm.time()
        s_result = False

        SP = agent.serverParams

        opp_goal = Vector2D(SP.pitch_half_length, 0.0)
        our_goal = Vector2D(-SP.pitch_half_length, 0.0)
        kickable_opponent = True
        if wm.intercept_table.first_opponent_reach_steps > 1:
            kickable_opponent = False
        virtual_accel = (kickable_opponent and Vector2D(our_goal - wm.ball.position).set_length(0.5) or Vector2D(0.0, 0.0))
        shoot_chance = (wm.ball.position.dist(opp_goal) < 20.0)

        ball_rel_angle = wm.ball.angleFromSelf() - wm.myself.body_direction
        tackle_rate = SP.tackle_power_rate * (1.0 - 0.5 * abs(ball_rel_angle) / 180.0)

        best_angle = AngleDeg(0.0)
        max_speed = -1.0

        for a in range(-180.0, 180.0, 10.0):
            rel_angle = AngleDeg(a - wm.myself.body_direction)

            eff_power = SP.max_tackle_power + ((SP.max_tackle_power - SP.max_back_tackle_power) * (1.0 - rel_angle.abs() / 180.0))
            eff_power *= tackle_rate

            vel = Vector2D(wm.ball.velocity + Vector2D.polar2vector(eff_power, AngleDeg(a)))
            vel += virtual_accel

            speed = vel.r()
            if speed > SP.ball_speed_max:
                vel *= (SP.ball_speed_max / speed)
                speed = SP.ball_speed_max

            if abs(vel.th()) > 90.0:
                continue

            ball_next = wm.ball.position + vel

            maybe_opponent_get_ball = False

            for o in wm.opponents:
                if o.pos_count > 10:
                    continue
                if o.ghost_count > 0:
                    continue
                if o.is_tackling:
                    continue
                if o.dist_from_ball > 6.0:
                    break

                opp_pos = Vector2D(o.position + o.velocity)
                if opp_pos.dist(ball_next) < SP.kickable_area + 0.1:
                    maybe_opponent_get_ball = True
                    break

            if maybe_opponent_get_ball:
                continue

            if shoot_chance:
                ball_ray = Ray2D(wm.ball.position, vel.th())
                goal_line = Line2D(Vector2D(SP.pitch_half_length, 10.0), Vector2D(SP.pitch_half_length, -10.0))
                intersect = Vector2D(ball_ray.intersection(goal_line))
                if intersect._is_valid and intersect.abs_y() < (SP.goal_width/2.0) - 3.0:
                    speed += 10.0

            if speed > max_speed:
                max_speed = speed
                best_angle = AngleDeg(a)

        if max_speed < 0.0:
            s_result = False
            agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: failed executeV12. max_speed={max_speed}")
            return False

        s_result = True
        s_best_angle = best_angle

        agent.add_log_text(LoggerLevel.TEAM, f"{__file__}: executeV12() angle={best_angle.degree()}")
        agent.add_log_message(LoggerLevel.TEAM,f"BasicTackle{best_angle.degree()}", agent.wm.myself.position.x, agent.wm.myself.position.y - 2, '\033[31m')

        tackle_dir = (best_angle - wm.myself.body_direction).degree()
        return PlayerAction(tackle=Tackle(tackle_dir, use_foul))
        #actions.append(PlayerAction(neck_turn_to_ball_or_scan=Neck_TurnToBallOrScan(0)))

        
        
        