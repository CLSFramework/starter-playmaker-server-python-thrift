from src.IAgent import IAgent
from pyrusgeom.vector_2d import Vector2D
from soccer.ttypes import RpcVector2D, PlayerAction, Body_SmartKick



class Shoot:
    def __init__(self):
        pass
    
    def decision(agent: IAgent):
        wm = agent.wm
        ball_pos = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_max_velocity = agent.serverParams.ball_speed_max

        center_goal = Vector2D ( agent.serverParams.pitch_half_length, 0.0 )
        right_goal = Vector2D ( agent.serverParams.pitch_half_length , agent.serverParams.goal_width ) # Lower Pole 
        left_goal = Vector2D ( agent.serverParams.pitch_half_length , -agent.serverParams.goal_width ) # Upper Pole 
        
        if ball_pos.dist(center_goal) <= 25.0:

            if left_goal.dist(ball_pos) < right_goal.dist(ball_pos):
                agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(RpcVector2D(left_goal.x(), left_goal.y()),
                                                                                ball_max_velocity ,
                                                                                    0.1 ,
                                                                                        2)))
            else :
                agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(RpcVector2D(right_goal.x(), right_goal.y()),
                                                                                ball_max_velocity ,
                                                                                    0.1 ,
                                                                                        2)))


        

