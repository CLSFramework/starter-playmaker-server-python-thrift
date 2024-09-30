# from pyparsing import col
from src.IDecisionMaker import IDecisionMaker
from src.IAgent import IAgent
from soccer.ttypes import PlayerAction, Catch
from src.DM_WithBall import WithBallDecisionMaker
from src.BhvGoalieBasicMove import BhvGoalieBasicMove
from pyrusgeom.rect_2d import Rect2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.size_2d import Size2D

class GoalieDecisionMaker(IDecisionMaker):
    def __init__(self):
        pass
    
    def make_decision(self, agent: IAgent):
        
        def DoKick(agent: IAgent):
            WithBallDecisionMaker.make_decision(agent)
        
        def DoMove(agent: IAgent):
            action_queue = list(reversed(BhvGoalieBasicMove.Decision(agent)))
            for i in action_queue:
                agent.add_action(i)
            
        our_penalty = Rect2D(Vector2D(-agent.serverParams.pitch_half_length, -agent.serverParams.penalty_area_half_width + 1), Size2D(agent.serverParams.penalty_area_length - 1, agent.serverParams.penalty_area_half_width * 2 - 2))
        if agent.wm.ball.dist_from_self < agent.serverParams.catch_area_l - 0.05 and our_penalty.contains(Vector2D(agent.wm.myself.position.x, agent.wm.myself.position.y)):
            agent.add_action(PlayerAction(catch_action=Catch()))
            return
        if agent.wm.myself.is_kickable:
            DoKick(agent)
        else:
            DoMove(agent)
        return
    
    
        
        