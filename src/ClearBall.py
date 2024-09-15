from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
from src.Tools import *
from pyrusgeom import vector_2d
from soccer.ttypes import *

class ClearBall :

    def __init__(self):
        pass
    

    def Decision(agent: IAgent):
        wm = agent.wm
        ball_pos = Vector2D(wm.ball.position.x, wm.ball.position.y)
        target = Vector2D(agent.serverParams.pitch_half_length, 0.0)
        if ball_pos.x() > -25.0 :
            if ball_pos.dist(Vector2D(0.0, -agent.serverParams.pitch_half_width)) < ball_pos.dist(Vector2D(0.0, agent.serverParams.pitch_half_width)) :
                target = Vector2D(0.0,-34.0)
            else :
                target = Vector2D(0.0,34.0)
        else :
            if abs(ball_pos.y()) < 10 and ball_pos.x() < -10.0 :
                if ball_pos.y() > 0.0 :
                    target = Vector2D(-agent.serverParams.pitch_half_length, 20.0)
                else :
                    target = Vector2D(-agent.serverParams.pitch_half_length, -20.0)
            else:
                if ball_pos.y() > 0.0 :
                    target = Vector2D(ball_pos.x(), 34.0)
                else : 
                    target = Vector2D(ball_pos.x(), -34.0)
        agent.add_log_message(LoggerLevel.CLEAR, f": Clearing Ball to {target}", agent.wm.myself.position.x, agent.wm.myself.position.y - 2, '\033[31m')
        return PlayerAction(body_smart_kick=Body_SmartKick(RpcVector2D(target.x(), target.y()),
                                                                        2.7,
                                                                            2.7,
                                                                                2))
        