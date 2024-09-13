from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
from src.Tools import *
from pyrusgeom import vector_2d
from soccer.ttypes import *

class ClearBall :

    def Decision(agent: IAgent):
        BallPosition = agent.wm.ball.position
        Target = Vector2D(agent.serverParams.pitch_half_length,0.0)
        if BallPosition.x > -25.0 :
            if BallPosition.dist(Vector2D(0.0,-34.0)) < BallPosition.dist(Vector2D(0.0,34.0)) :
                Target = Vector2D(0.0,-34.0)
            else :
                Target = Vector2D(0.0,34.0)
        else :
            if abs(BallPosition.y) < 10 and BallPosition.x < -10.0 :
                if BallPosition.y > 0.0 :
                    Target = Vector2D(-agent.serverParams.pitch_half_length,20.0)
                else :
                    Target = Vector2D(-agent.serverParams.pitch_half_length,-20.0)
            else :
                if BallPosition.y > 0.0 :
                    Target = Vector2D(BallPosition.x,34.0)
                else : 
                    Target = Vector2D(BallPosition.x,-34.0)
        agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(Target,
                                                                        2.7,
                                                                            2.7,
                                                                                2)))
        