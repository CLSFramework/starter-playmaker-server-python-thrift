from src.IAgent import IAgent
from pyrusgeom.vector_2d import Vector2D
from soccer.ttypes import PlayerAction, RpcVector2D, Body_TackleToPoint, Body_Intercept, Body_GoToPoint, Body_TurnToBall
from src.Strategy import Strategy


class BhvBasicMove:
    
    def __init__(self):
        pass
    
    
    def Decision(agent: IAgent):
        # Player action without ball
        
        wm = agent.wm
        
        agent.add_action(PlayerAction(body_tackle_to_point=Body_TackleToPoint(RpcVector2D(0, 0), 0.8, 20)))
        
        self_min = wm.intercept_table.self_reach_steps
        mate_min = wm.intercept_table.first_teammate_reach_steps
        opp_min = wm.intercept_table.first_opponent_reach_steps
        our_min = min(self_min, mate_min)
        
        if mate_min > 1 and (self_min <= 3 or (self_min <= mate_min and self_min < opp_min + 3)):
            agent.add_action(PlayerAction(body_intercept=Body_Intercept()))
            
        if our_min < opp_min:
            pass
            # Do offensive move like unmark or possitioning
        else:
            pass
            # Do defensive move like mark or block
        
        home_pos = Strategy.get_home_pos(agent)
        
        dash_power = Strategy.get_normal_dash_power(agent)
        
        dist_thr = wm.ball.dist_from_self * 0.1
        dist_thr = max(dist_thr, 1.0)
        
        agent.add_action(PlayerAction(body_go_to_point=Body_GoToPoint(home_pos, 0, dash_power)))
        agent.add_action(PlayerAction(body_turn_to_ball=Body_TurnToBall()))