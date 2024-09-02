from abc import ABC
from src.IAgent import IAgent
from soccer.ttypes import WorldModel
from soccer.ttypes import CoachAction
from soccer.ttypes import ChangePlayerType, DoHeliosSubstitute, CoachActions


class SampleCoachAgent(IAgent, ABC):
    def __init__(self):
        super().__init__()
        self.wm: WorldModel = None
        self.first_substitution = True
    
    def get_actions(self, wm:WorldModel) -> CoachActions:
        self.wm = wm
        
        actions = CoachActions()
        actions.actions = []
        # if (wm.cycle == 0
        #     and self.first_substitution
        #     and self.playerParams is not None
        #     and len(self.playerTypes.keys()) == self.playerParams.player_types):
            
        #     self.first_substitution = False
        #     for i in range(11):
        #         actions.actions.append(
        #             CoachAction(
        #                 change_player_types=ChangePlayerType(
        #                 uniform_number=i+1,
        #                 type=i
        #                 )
        #             )
        #         )

        # actions.append(
        #     CoachAction(
        #         do_helios_substitute=DoHeliosSubstitute()
        #     )
        # )
        actions.actions.append(
            CoachAction(
                do_helios_substitute=DoHeliosSubstitute()
            )
        )
        return actions