from src.IDecisionMaker import IDecisionMaker
from src.DM_PlayOn import PlayOnDecisionMaker
from src.DM_SetPlay import SetPlayDecisionMaker
from src.IAgent import IAgent
from soccer.ttypes import PlayerAction, HeliosGoalie, HeliosPenalty, HeliosSetPlay, GameModeType, Catch
from src.DM_WithBall import WithBallDecisionMaker 
from src.BhvGoalieBasicMove import BhvGoalieBasicMove
from pyrusgeom.rect_2d import Rect2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.size_2d import Size2D

class DecisionMaker(IDecisionMaker):
    def __init__(self):
        self.playOnDecisionMaker = PlayOnDecisionMaker()
        self.setPlayDecisionMaker = SetPlayDecisionMaker()
    
    def make_decision(self, agent: IAgent):
        if agent.wm.myself.is_goalie:
            if agent.wm.game_mode_type == GameModeType.PlayOn:
                if agent.wm.myself.is_kickable:
                    our_penalty = Rect2D(Vector2D(-agent.serverParams.pitch_half_length, -agent.serverParams.penalty_area_half_width + 1), Size2D(agent.serverParams.penalty_area_length - 1, agent.serverParams.penalty_area_half_width * 2 - 2))
                    if agent.wm.ball.dist_from_self < agent.serverParams.catch_area_l - 0.05 and our_penalty.contains(Vector2D(agent.wm.myself.position.x, agent.wm.myself.position.y)):
                        agent.add_action(PlayerAction(catch_action=Catch()))
                        return
                    WithBallDecisionMaker().make_decision(agent=agent)
                else:
                    action_queue = list(reversed(BhvGoalieBasicMove.Decision(agent)))
                    for i in action_queue:
                        agent.add_action(i)
            else:
                agent.add_action(PlayerAction(helios_goalie=HeliosGoalie()))
        else:
            if agent.wm.game_mode_type == GameModeType.PlayOn:
                self.playOnDecisionMaker.make_decision(agent)
            elif agent.wm.is_penalty_kick_mode:
                agent.add_action(PlayerAction(helios_penalty=HeliosPenalty()))
            else:
                agent.add_action(PlayerAction(helios_set_play=HeliosSetPlay()))