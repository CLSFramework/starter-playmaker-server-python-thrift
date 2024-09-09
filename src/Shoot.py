from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
import time
import logging
import math
from soccer.ttypes import *



class Shoot:
    def __init__(self):
        pass
    
    def decision(self, agent: IAgent):

        BallPosition = agent.wm.ball.position
        BallMaxVelocity = agent.serverParams.ball_speed_max

        CenterGoal = RpcVector2D ( agent.serverParams.pitch_half_length, 0.0 )
        RightGoal = RpcVector2D ( agent.serverParams.pitch_half_length , agent.serverParams.goal_width ) # Lower Pole 
        LeftGoal = RpcVector2D ( agent.serverParams.pitch_half_length , -agent.serverParams.goal_width ) # Upper Pole 
        
        if BallPosition.dist(CenterGoal) <= 25:

            if LeftGoal.dist(BallPosition) < RightGoal.dist(BallPosition):
                agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(LeftGoal,
                                                                                BallMaxVelocity ,
                                                                                    0.1 ,
                                                                                        2)))
            else :
                agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(RightGoal,
                                                                                BallMaxVelocity ,
                                                                                    0.1 ,
                                                                                        2)))


        

