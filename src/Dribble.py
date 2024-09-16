from src.IAgent import IAgent
from src.Tools import Tools
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.sector_2d import Sector2D
from soccer.ttypes import RpcVector2D, PlayerAction, Body_SmartKick, LoggerLevel


class Dribble:

    def __init__(self):
        pass

    def Decision(agent: IAgent):
        wm = agent.wm
        ball_pos = Vector2D(wm.ball.position.x, wm.ball.position.y)
        dribble_angle = (Vector2D(52.5, 0) - ball_pos).th().degree()
        dribble_speed = 0.8
        dribble_threshold = 0.7
        dribble_sector = Sector2D(ball_pos, 0, 3, dribble_angle - 15, dribble_angle + 15)
        
        if not Tools.ExistOpponentIn(agent , dribble_sector):
            Target = Vector2D.polar2vector(3, dribble_angle) + ball_pos
            agent.add_log_message(LoggerLevel.DRIBBLE, f": Dribbling to {Target}", agent.wm.myself.position.x, agent.wm.myself.position.y - 2, '\033[31m') 
            return PlayerAction(body_smart_kick=Body_SmartKick(RpcVector2D(Target.x(), Target.y()),
                                                                dribble_speed,
                                                                    dribble_threshold,
                                                                        2))
        return


    


