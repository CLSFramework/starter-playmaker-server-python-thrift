from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
from src.Tools import *
from pyrusgeom import vector_2d
from soccer.ttypes import *
import numpy as np 


class Pass:

    def __init__(self):
        pass

    def Decision(agent: IAgent):
        Targets = agent.wm.teammates
        BallPosition = agent.wm.ball.position
        AgentPosition = agent.wm.myself.position
        for i in Targets :
            if i == None or i.uniform_number == agent.wm.myself.uniform_number or i.uniform_number < 0.0:
                continue
            if i.position.dist(BallPosition) > 30.0 :
                continue
            if AgentPosition.dist(i.position) < 2.0:
                continue
            Possibility = Sector2D(BallPosition,
                                    1.0,
                                        i.position.dist(BallPosition) + 3.0,
                                            Vector2D(i.position - BallPosition).th() - 15.0,
                                                Vector2D(i.position - BallPosition).th() + 15.0)
            if ExistOpponentIn(agent, Possibility):
                Targets.remove(i)
        if not Targets == []:
            BestTarget = Targets[0]
            for i in Targets:
                if i.position.x > BestTarget.position.x :
                    BestTarget = i.position
            if not agent.wm.game_mode_type == GameModeType(2):
                agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(BestTarget,
                    2.7,
                        2.5,
                            1)))
            else :
                agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(BestTarget,
                    2.7,
                        2.5,
                            1)))  
                
def ExistOpponentIn(agent: IAgent, region: Region2D):
        for i in agent.wm.opponents:
            if region.contains(i.position):
               return True 