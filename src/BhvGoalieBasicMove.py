from src.IAgent import IAgent
from soccer.ttypes import PlayerAction, RpcVector2D, Body_TackleToPoint, Body_Intercept, Body_GoToPoint, Body_TurnToPoint, LoggerLevel
from src.Strategy import Strategy
from src.BhvBasicTackle import BhvBasicTackle
from pyrusgeom.soccer_math import inertia_n_step_point
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.line_2d import Line2D

class BhvGoalieBasicMove:
    def __init__(self):
        pass

    def Decision(agent: IAgent):
        
        wm = agent.wm
        actions = []
        
        self_min = wm.intercept_table.self_reach_steps
        mate_min = wm.intercept_table.first_teammate_reach_steps
        opp_min = wm.intercept_table.first_opponent_reach_steps
    
        
        actions += [tackle] if (tackle := BhvBasicTackle(0.8, 80).Decision(agent)) is not None else []
        
        if self_min < opp_min and self_min < mate_min:
            actions.append(PlayerAction(body_intercept=Body_Intercept()))
            
        move_point = BhvGoalieBasicMove.GetTargetPoint(agent)
        agent.add_log_message(LoggerLevel.TEAM, f": Moving to {move_point}", agent.wm.myself.position.x, agent.wm.myself.position.y - 2, '\033[31m')
        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(move_point.x(), move_point.y()), 1, 100)))
        
        actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(move_point.x(), move_point.y()))))
        
        return actions
    
    def GetTargetPoint(agent: IAgent):
        
        base_move_x = -49.8
        danger_move_x = -51.5
        wm = agent.wm
        
        ball_reach_step = 0
        
        mate_min = wm.intercept_table.first_teammate_reach_steps
        opp_min = wm.intercept_table.first_opponent_reach_steps
        
        if mate_min > 1 and opp_min > 1:
            ball_reach_step = min(mate_min, opp_min)
        
        ball_pos = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_velocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)
        
        base_pos = inertia_n_step_point(ball_pos, ball_velocity, ball_reach_step, agent.serverParams.ball_decay)
        
        if base_pos.y() > agent.serverParams.goal_width / 2 + 3.0:
            right_pole = Vector2D(-agent.serverParams.pitch_half_length, agent.serverParams.goal_width / 2)
            
            angle_to_pole = (right_pole - base_pos).th()
            
            if -140 < angle_to_pole.degree() and angle_to_pole.degree() < -90:
                return Vector2D(danger_move_x, agent.serverParams.goal_width / 2 + 0.001)
        
        elif base_pos.y() < -agent.serverParams.goal_width / 2 - 3:
            left_pole = Vector2D(-agent.serverParams.pitch_half_length, -agent.serverParams.goal_width / 2)
            angle_to_pole = (left_pole - base_pos).th()
            
            if 90 < angle_to_pole.degree() and angle_to_pole.degree() < 140:
                return Vector2D(danger_move_x, -agent.serverParams.goal_width / 2 - 0.001)

        # ball is close to goal line
        
        if base_pos.x() < -agent.serverParams.pitch_half_length + 8 and base_pos.abs_y() > agent.serverParams.goal_width / 2 + 2:
            target_point = Vector2D(base_move_x, agent.serverParams.goal_width / 2 - 1)
            
            if base_pos.y() < 0:
                target_point.set_y(-target_point.y())
            
            return target_point

        x_back = 7.0
        ball_pred_cycle = 5
        y_buf = 0.5
        
        base_point = Vector2D(-agent.serverParams.pitch_half_length - x_back, 0)
        
        if opp_min < 2:
            ball_point = base_pos
        else:
            if opp_min < ball_pred_cycle:
                ball_pred_cycle = opp_min
            
            ball_point = inertia_n_step_point(base_pos, ball_velocity, ball_pred_cycle, agent.serverParams.ball_decay)
        
        if ball_point.x() < base_point.x() + 0.1:
            ball_point.set_x(base_point.x() + 0.1)
        
        ball_line = Line2D(ball_point, base_point)
        move_y = ball_line.get_y(base_move_x)
        
        if move_y > agent.serverParams.goal_width / 2 - y_buf:
            move_y = agent.serverParams.goal_width / 2 - y_buf
        if move_y < -agent.serverParams.goal_width / 2 + y_buf:
            move_y = -agent.serverParams.goal_width / 2 + y_buf
        
        return Vector2D(base_move_x, move_y)

            