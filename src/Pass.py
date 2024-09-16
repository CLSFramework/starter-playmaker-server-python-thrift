from src.IAgent import IAgent
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
from src.Tools import Tools
from soccer.ttypes import *


class Pass:

    def __init__(self):
        pass

    def Decision(agent: IAgent):
        
        wm = agent.wm
        target = []
        ball_pos = Vector2D(wm.ball.position.x, wm.ball.position.y)
        self_pos = Vector2D(wm.myself.position.x, wm.myself.position.y)
        print('len: ', len(wm.teammates))
        for i in wm.teammates :
            if i == None or i.uniform_number == wm.myself.uniform_number or i.uniform_number < 0:
                continue
            tm_pos = Vector2D(i.position.x, i.position.y)
            if tm_pos.dist(ball_pos) > 30.0 :
                continue
            if self_pos.dist(tm_pos) < 2.0:
                continue
            check_root = Sector2D(ball_pos, 1.0, tm_pos.dist(ball_pos) + 3.0, (tm_pos - ball_pos).th().degree() - 15.0, (tm_pos - ball_pos).th().degree() + 15.0)
            if not Tools.ExistOpponentIn(agent, check_root):
                target.append(i)
                
        if not target == []:
            best_target = target[0]
            for i in target:
                if i.position.x > best_target.position.x:
                    best_target = i
            if not wm.game_mode_type == GameModeType.PlayOn:
                agent.add_log_message(LoggerLevel.PASS, f": Passing to {best_target.uniform_number}", agent.wm.myself.position.x, agent.wm.myself.position.y - 2, '\033[31m')
                return PlayerAction(body_smart_kick=Body_SmartKick(best_target.position, 2.7, 2.5, 1))
            else :
                agent.add_log_message(LoggerLevel.PASS, f": Passing to {best_target.uniform_number}", agent.wm.myself.position.x, agent.wm.myself.position.y - 2, '\033[31m')
                return PlayerAction(body_smart_kick=Body_SmartKick(best_target.position, 2.5, 2.5, 1))
        
        return 
                