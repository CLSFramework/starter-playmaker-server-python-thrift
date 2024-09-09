from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
import time
import logging
import math
from src.Tools import *
from pyrusgeom import vector_2d
from soccer.ttypes import *


class Dribble:

    def __init__(self):
        pass

    def Decision(self,agent: IAgent):

        BallPosition = agent.wm.ball.position
        DribbleAngle = Vector2D(RpcVector2D(52.5,0) - BallPosition).th()
        DribbleSpeed = 0.8, DribbleThreshold = 0.7
        DribbleSector = Sector2D(BallPosition,
                                    0,
                                        3,
                                            DribbleAngle - 15,
                                                DribbleAngle + 15)
        
        if not ExistOpponentIn(agent , DribbleSector):
            Target = Vector2D(3 * DribbleAngle.cos(),
                                3 * DribbleAngle.sin()) + BallPosition 
            agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(Target,
                                                                            DribbleSpeed,
                                                                                DribbleThreshold,
                                                                                    2)))


def ExistOpponentIn(agent: IAgent, region: Region2D):
        for i in agent.wm.opponents:
            if region.contains(i.position):
                return True
    


