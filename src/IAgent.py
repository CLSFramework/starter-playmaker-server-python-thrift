from typing import Union
from abc import ABC, abstractmethod
from typing import Union
from soccer.ttypes import WorldModel, PlayerActions, ServerParam, PlayerParam, PlayerType, PlayerAction
from soccer.ttypes import AddText, LoggerLevel, Log, AddMessage, AddCircle, CoachAction, TrainerAction
from soccer.ttypes import RpcVector2D


class IAgent(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.wm: Union[WorldModel, None] = None
        self.actions: list[PlayerAction] = []
        self.serverParams: Union[ServerParam, None] = None
        self.playerParams: Union[PlayerParam, None] = None
        self.playerTypes: Union[PlayerType, dict[PlayerType]] = {}
        self.debug_mode: bool = False

    def set_server_param(self, server_param: ServerParam):
        self.serverParams = server_param
    
    def set_player_param(self, player_param: PlayerParam):
        self.playerParams = player_param
        
    def set_player_types(self, player_type: PlayerType):
        self.playerTypes[player_type.id] = player_type
        
    def get_type(self, id: int) -> PlayerType:
        if id < 0:
            id = 0
        return self.playerTypes[id]

    @abstractmethod
    def get_actions(self, wm: WorldModel) -> PlayerActions:
        pass

    # @abstractmethod
    # def get_strategy(self) -> IPositionStrategy:
    #     pass

    def set_debug_mode(self, debug_mode: bool):
        self.debug_mode = debug_mode

    def add_log_text(self, level: LoggerLevel, message: str):
        if not self.debug_mode:
            return
        self.add_action(PlayerAction(
            log=Log(
                add_text=AddText(
                    level=level,
                    message=message
                )
            )
        ))

    def add_log_message(self, level: LoggerLevel, message: str, x, y, color):
        if not self.debug_mode:
            return
        self.add_action(PlayerAction(
            log=Log(
                add_message=AddMessage(
                    level=level,
                    message=message,
                    position=RpcVector2D(x=x, y=y),
                    color=color,
                )
            )
        ))

    def add_log_circle(self, level: LoggerLevel, center_x: float, center_y: float, radius: float, color: str,
                       fill: bool):
        if not self.debug_mode:
            return
        self.add_action(PlayerAction(
            log=Log(
                add_circle=AddCircle(
                    level=level,
                    center=RpcVector2D(x=center_x, y=center_y),
                    radius=radius,
                    color=color,
                    fill=fill
                )
            )
        ))

    def add_action(self, actions: Union[PlayerAction, CoachAction, TrainerAction]):
        self.actions.append(actions)
