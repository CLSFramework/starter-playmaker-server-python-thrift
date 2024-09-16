from src.IAgent import IAgent
from soccer.ttypes import PlayerAction, CardType, Tackle
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.soccer_math import inertia_n_step_point
from pyrusgeom.ray_2d import Ray2D
from pyrusgeom.line_2d import Line2D

class BhvBasicTackle:
    
    def __init__(self, min_prob: float, body_thr: float):
        self.min_prob = min_prob
        self.body_thr = body_thr

    def Decision(self, agent: IAgent):
        
        action = []
        wm = agent.wm
        use_foul = False
        tackle_prob = wm.myself.tackle_probability
        if wm.myself.card == CardType.NO_CARD and (wm.ball.position.x > agent.serverParams.our_penalty_area_line_x + 0.5 or abs(wm.ball.position.y) > agent.serverParams.penalty_area_half_width + 0.5) and tackle_prob < wm.myself.foul_probability:
            tackle_prob = wm.myself.foul_probability
            use_foul = True
            
        if tackle_prob < self.min_prob:
            return action
        
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
            return action

        return BhvBasicTackle.ExecuteOldVersion(self, agent, use_foul)

    
    def ExecuteOldVersion(self, agent: IAgent, use_foul: bool):
        
        wm = agent.wm
        actions = []
        tackle_power = agent.serverParams.max_tackle_power
        
        if abs(wm.myself.body_direction) < self.body_thr:
            actions.append(PlayerAction(tackle=Tackle(tackle_power, use_foul)))
            
        tackle_power = -agent.serverParams.max_back_tackle_power
        
        if tackle_power < 0.0 and abs(wm.myself.body_direction) > 180 - self.body_thr:
            actions.append(PlayerAction(tackle=Tackle(tackle_power)))
        
        return actions
        

        
        
        