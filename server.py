from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from soccer import Game
from soccer.ttypes import DoChangeMode, DoMovePlayer, State, Empty, PlayerActions, CoachActions, TrainerActions, PlayerAction, GameModeType
from soccer.ttypes import ServerParam, PlayerParam, PlayerType, InitMessage, RegisterRequest, RegisterResponse, AgentType
from soccer.ttypes import HeliosChainAction, HeliosBasicMove, HeliosGoalie, HeliosSetPlay
from soccer.ttypes import DoMoveBall, RpcVector2D, TrainerAction
from soccer.ttypes import DoHeliosSubstitute, CoachAction
import os
from utils.PFProcessServer import PFProcessServer
from thrift.server.TServer import TThreadedServer
from typing import Union
from threading import Semaphore
from multiprocessing import Manager, Lock
import logging
from pyrusgeom.vector_2d import Vector2D
import argparse
from src.SampleCoachAgent import SampleCoachAgent
from src.SamplePlayerAgent import SamplePlayerAgent
from src.SampleTrainerAgent import SampleTrainerAgent


logging.basicConfig(level=logging.DEBUG)

manager = Manager()
shared_lock = Lock()  # Create a Lock for synchronization
shared_number_of_connections = manager.Value('i', 0)


class GameHandler:
    def __init__(self):
        self.server_params: Union[ServerParam, None] = None
        self.player_params: Union[PlayerParam, None] = None
        self.player_types: dict[int, PlayerType] = {}
        self.debug_mode: bool = False
        self.agent: Union[SampleTrainerAgent, SampleCoachAgent, SamplePlayerAgent] = None

    def GetPlayerActions(self, state: State):
        logging.debug(f"GetPlayerActions unum {state.register_response.uniform_number} at {state.world_model.cycle}")
        actions = self.agent.get_actions(state.world_model)
        return actions

    def GetCoachActions(self, state: State):
        logging.debug(f"GetCoachActions coach at {state.world_model.cycle}")
        actions = self.agent.get_actions(state.world_model)
        return actions

    def GetTrainerActions(self, state: State):
        logging.debug(f"GetTrainerActions trainer at {state.world_model.cycle}")
        actions = self.agent.get_actions(state.world_model)
        return actions

    def SendServerParams(self, serverParams: ServerParam):
        logging.debug(f"Server params received unum {serverParams.register_response.uniform_number}")
        self.agent.set_server_param(serverParams)
        res = Empty()
        return res

    def SendPlayerParams(self, playerParams: PlayerParam):
        logging.debug(f"Player params received unum {playerParams.register_response.uniform_number}")
        self.agent.set_player_param(playerParams)
        res = Empty()
        return res

    def SendPlayerType(self, playerType: PlayerType):
        logging.debug(f"Player type received unum {playerType.register_response.uniform_number}")
        self.agent.set_player_types(playerType)
        res = Empty()
        return res

    def SendInitMessage(self, initMessage: InitMessage):
        logging.debug(f"Init message received unum {initMessage.register_response.uniform_number}")
        self.debug_mode = initMessage.debug_mode
        res = Empty()
        return res

    def Register(self, register_request: RegisterRequest):
        logging.debug(f"received register request from team_name: {register_request.team_name} "
                      f"unum: {register_request.uniform_number} "
                      f"agent_type: {register_request.agent_type}")
        with shared_lock:
            shared_number_of_connections.value += 1
            logging.debug(f"Number of connections {shared_number_of_connections.value}")
            if register_request.agent_type == AgentType.TrainerT:
                self.agent = SampleTrainerAgent()
            elif register_request.agent_type == AgentType.CoachT:
                self.agent = SampleCoachAgent()
            else:
                self.agent = SamplePlayerAgent()
            team_name = register_request.team_name
            uniform_number = register_request.uniform_number
            agent_type = register_request.agent_type
            res = RegisterResponse(client_id=shared_number_of_connections.value,
                                   team_name=team_name,
                                   uniform_number=uniform_number,
                                   agent_type=agent_type)
            return res

    def SendByeCommand(self, register_response: RegisterResponse):
        logging.debug(f"Bye command received unum {register_response.uniform_number}")
        with shared_lock:
            pass
        res = Empty()
        return res

def serve(port):
    handler = GameHandler()
    processor = Game.Processor(handler)
    transport = TSocket.TServerSocket(host='0.0.0.0', port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = PFProcessServer(processor, transport, tfactory, pfactory)
    # server = TThreadedServer(processor, transport, tfactory, pfactory)

    logging.info(f"Starting server on port {port}")
    try:
        server.serve()
    except KeyboardInterrupt:
        server.stop()
        print("Stopping server")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run play maker server')
    parser.add_argument('-p', '--rpc-port', required=False, help='The port of the server', default=50051)
    args = parser.parse_args()
    serve(args.rpc_port)
