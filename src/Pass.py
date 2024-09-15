from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
from src.Tools import Tools
from pyrusgeom import vector_2d
from soccer.ttypes import *
import numpy as np 


class Pass:

    def __init__(self):
        pass

    def Decision(agent: IAgent):
        wm = agent.wm
        target = wm.teammates
        ball_pos = Vector2D(wm.ball.position.x, wm.ball.position.y)
        self_pos = wm.myself.position
        for i in target :
            if i == None or i.uniform_number == wm.myself.uniform_number or i.uniform_number < 0:
                continue
            if i.position.dist(ball_pos) > 30.0 :
                continue
            if self_pos.dist(i.position) < 2.0:
                continue
            Possibility = Sector2D(ball_pos, 1.0, Vector2D(i.position.x, i.position.y).dist(ball_pos) + 3.0, Vector2D(Vector2D(i.position.x, i.position.y) - ball_pos).th().degree() - 15.0, Vector2D(Vector2D(i.position.x, i.position.y) - ball_pos).th().degree() + 15.0)
            if Tools.ExistOpponentIn(agent, Possibility):
                target.remove(i)
        if not target == []:
            best_target = target[0]
            for i in target:
                if i.position.x > best_target.position.x :
                    best_target = i.position
            if not wm.game_mode_type == GameModeType.PlayOn:
                agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(best_target,
                    2.7,
                        2.5,
                            1)))
            else :
                agent.add_action(PlayerAction(body_smart_kick=Body_SmartKick(best_target,
                    2.7,
                        2.5,
                            1)))  
                