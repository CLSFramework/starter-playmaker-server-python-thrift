import sys
from typing import List, Dict, Tuple, Union, Any, Optional
from enum import Enum, auto

class ViewWidth(Enum):
    NARROW = auto()
    NORMAL = auto()
    WIDE = auto()

class AgentType(Enum):
    PlayerT = auto()
    CoachT = auto()
    TrainerT = auto()

class RpcVector2D(object):
    def __init__(self, x: float = None, y: float = None, dist: float = None, angle: float = None):
        pass
    x: float
    y: float
    dist: float
    angle: float

class RegisterRequest(object):
    def __init__(self, agent_type: AgentType = None, team_name: str = None, uniform_number: int = None):
        pass
    agent_type: AgentType
    team_name: str
    uniform_number: int

class RegisterResponse(object):
    def __init__(self, client_id: int = None, agent_type: AgentType = None, team_name: str = None, uniform_number: int = None):
        pass
    client_id: int
    agent_type: AgentType
    team_name: str
    uniform_number: int

class Ball(object):
    def __init__(self, position: RpcVector2D = None, relative_position: RpcVector2D = None, seen_position: RpcVector2D = None, heard_position: RpcVector2D = None, velocity: RpcVector2D = None, seen_velocity: RpcVector2D = None, heard_velocity: RpcVector2D = None, pos_count: int = None, seen_pos_count: int = None, heard_pos_count: int = None, vel_count: int = None, seen_vel_count: int = None, heard_vel_count: int = None, lost_count: int = None, ghost_count: int = None, dist_from_self: float = None, angle_from_self: float = None):
        pass
    position: RpcVector2D
    relative_position: RpcVector2D
    seen_position: RpcVector2D
    heard_position: RpcVector2D
    velocity: RpcVector2D
    seen_velocity: RpcVector2D
    heard_velocity: RpcVector2D
    pos_count: int
    seen_pos_count: int
    heard_pos_count: int
    vel_count: int
    seen_vel_count: int
    heard_vel_count: int
    lost_count: int
    ghost_count: int
    dist_from_self: float
    angle_from_self: float

class Side(Enum):
    UNKNOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class LoggerLevel(Enum):
    NoneLevel = auto()
    SYSTEM = auto()
    SENSOR = auto()
    WORLD = auto()
    ACTION = auto()
    INTERCEPT = auto()
    KICK = auto()
    HOLD = auto()
    DRIBBLE = auto()
    PASS = auto()
    CROSS = auto()
    SHOOT = auto()
    CLEAR = auto()
    BLOCK = auto()
    MARK = auto()
    POSITIONING = auto()
    ROLE = auto()
    TEAM = auto()
    COMMUNICATION = auto()
    ANALYZER = auto()
    ACTION_CHAIN = auto()
    PLAN = auto()

class CardType(Enum):
    NO_CARD = auto()
    YELLOW = auto()
    RED = auto()

class Player(object):
    def __init__(self, position: RpcVector2D = None, seen_position: RpcVector2D = None, heard_position: RpcVector2D = None, velocity: RpcVector2D = None, seen_velocity: RpcVector2D = None, pos_count: int = None, seen_pos_count: int = None, heard_pos_count: int = None, vel_count: int = None, seen_vel_count: int = None, ghost_count: int = None, dist_from_self: float = None, angle_from_self: float = None, id: int = None, side: Side = None, uniform_number: int = None, uniform_number_count: int = None, is_goalie: bool = None, body_direction: float = None, body_direction_count: int = None, face_direction: float = None, face_direction_count: int = None, point_to_direction: float = None, point_to_direction_count: int = None, is_kicking: bool = None, dist_from_ball: float = None, angle_from_ball: float = None, ball_reach_steps: int = None, is_tackling: bool = None, type_id: int = None):
        pass
    position: RpcVector2D
    seen_position: RpcVector2D
    heard_position: RpcVector2D
    velocity: RpcVector2D
    seen_velocity: RpcVector2D
    pos_count: int
    seen_pos_count: int
    heard_pos_count: int
    vel_count: int
    seen_vel_count: int
    ghost_count: int
    dist_from_self: float
    angle_from_self: float
    id: int
    side: Side
    uniform_number: int
    uniform_number_count: int
    is_goalie: bool
    body_direction: float
    body_direction_count: int
    face_direction: float
    face_direction_count: int
    point_to_direction: float
    point_to_direction_count: int
    is_kicking: bool
    dist_from_ball: float
    angle_from_ball: float
    ball_reach_steps: int
    is_tackling: bool
    type_id: int

class Self(object):
    def __init__(self, position: RpcVector2D = None, seen_position: RpcVector2D = None, heard_position: RpcVector2D = None, velocity: RpcVector2D = None, seen_velocity: RpcVector2D = None, pos_count: int = None, seen_pos_count: int = None, heard_pos_count: int = None, vel_count: int = None, seen_vel_count: int = None, ghost_count: int = None, id: int = None, side: Side = None, uniform_number: int = None, uniform_number_count: int = None, is_goalie: bool = None, body_direction: float = None, body_direction_count: int = None, face_direction: float = None, face_direction_count: int = None, point_to_direction: float = None, point_to_direction_count: int = None, is_kicking: bool = None, dist_from_ball: float = None, angle_from_ball: float = None, ball_reach_steps: int = None, is_tackling: bool = None, relative_neck_direction: float = None, stamina: float = None, is_kickable: bool = None, catch_probability: float = None, tackle_probability: float = None, foul_probability: float = None, view_width: ViewWidth = None, type_id: int = None, kick_rate: float = None, recovery: float = None, stamina_capacity: float = None, card: CardType = None, catch_time: int = None):
        pass
    position: RpcVector2D
    seen_position: RpcVector2D
    heard_position: RpcVector2D
    velocity: RpcVector2D
    seen_velocity: RpcVector2D
    pos_count: int
    seen_pos_count: int
    heard_pos_count: int
    vel_count: int
    seen_vel_count: int
    ghost_count: int
    id: int
    side: Side
    uniform_number: int
    uniform_number_count: int
    is_goalie: bool
    body_direction: float
    body_direction_count: int
    face_direction: float
    face_direction_count: int
    point_to_direction: float
    point_to_direction_count: int
    is_kicking: bool
    dist_from_ball: float
    angle_from_ball: float
    ball_reach_steps: int
    is_tackling: bool
    relative_neck_direction: float
    stamina: float
    is_kickable: bool
    catch_probability: float
    tackle_probability: float
    foul_probability: float
    view_width: ViewWidth
    type_id: int
    kick_rate: float
    recovery: float
    stamina_capacity: float
    card: CardType
    catch_time: int

class InterceptActionType(Enum):
    UNKNOWN_Intercept_Action_Type = auto()
    OMNI_DASH = auto()
    TURN_FORWARD_DASH = auto()
    TURN_BACKWARD_DASH = auto()

class InterceptInfo(object):
    def __init__(self, action_type: InterceptActionType = None, turn_steps: int = None, turn_angle: float = None, dash_steps: int = None, dash_power: float = None, dash_dir: float = None, final_self_position: RpcVector2D = None, final_ball_dist: float = None, final_stamina: float = None, value: float = None):
        pass
    action_type: InterceptActionType
    turn_steps: int
    turn_angle: float
    dash_steps: int
    dash_power: float
    dash_dir: float
    final_self_position: RpcVector2D
    final_ball_dist: float
    final_stamina: float
    value: float

class InterceptTable(object):
    def __init__(self, self_reach_steps: int = None, first_teammate_reach_steps: int = None, second_teammate_reach_steps: int = None, first_opponent_reach_steps: int = None, second_opponent_reach_steps: int = None, first_teammate_id: int = None, second_teammate_id: int = None, first_opponent_id: int = None, second_opponent_id: int = None, self_intercept_info: List[InterceptInfo] = None):
        pass
    self_reach_steps: int
    first_teammate_reach_steps: int
    second_teammate_reach_steps: int
    first_opponent_reach_steps: int
    second_opponent_reach_steps: int
    first_teammate_id: int
    second_teammate_id: int
    first_opponent_id: int
    second_opponent_id: int
    self_intercept_info: List[InterceptInfo]

class GameModeType(Enum):
    BeforeKickOff = auto()
    TimeOver = auto()
    PlayOn = auto()
    KickOff_ = auto()
    KickIn_ = auto()
    FreeKick_ = auto()
    CornerKick_ = auto()
    GoalKick_ = auto()
    AfterGoal_ = auto()
    OffSide_ = auto()
    PenaltyKick_ = auto()
    FirstHalfOver = auto()
    Pause = auto()
    Human = auto()
    FoulCharge_ = auto()
    FoulPush_ = auto()
    FoulMultipleAttacker_ = auto()
    FoulBallOut_ = auto()
    BackPass_ = auto()
    FreeKickFault_ = auto()
    CatchFault_ = auto()
    IndFreeKick_ = auto()
    PenaltySetup_ = auto()
    PenaltyReady_ = auto()
    PenaltyTaken_ = auto()
    PenaltyMiss_ = auto()
    PenaltyScore_ = auto()
    IllegalDefense_ = auto()
    PenaltyOnfield_ = auto()
    PenaltyFoul_ = auto()
    GoalieCatch_ = auto()
    ExtendHalf = auto()
    MODE_MAX = auto()

class WorldModel(object):
    def __init__(self, intercept_table: InterceptTable = None, our_team_name: str = None, their_team_name: str = None, our_side: Side = None, last_set_play_start_time: int = None, myself: Self = None, ball: Ball = None, teammates: List[Player] = None, opponents: List[Player] = None, unknowns: List[Player] = None, our_players_dict: Dict[int, Player] = None, their_players_dict: Dict[int, Player] = None, our_goalie_uniform_number: int = None, their_goalie_uniform_number: int = None, offside_line_x: float = None, offside_line_x_count: int = None, kickable_teammate_id: int = None, kickable_opponent_id: int = None, last_kick_side: Side = None, last_kicker_uniform_number: int = None, cycle: int = None, game_mode_type: GameModeType = None, left_team_score: int = None, right_team_score: int = None, is_our_set_play: bool = None, is_their_set_play: bool = None, stoped_cycle: int = None, our_team_score: int = None, their_team_score: int = None, is_penalty_kick_mode: bool = None, helios_home_positions: Dict[int, RpcVector2D] = None, our_defense_line_x: float = None, their_defense_line_x: float = None, our_defense_player_line_x: float = None, their_defense_player_line_x: float = None, kickable_teammate_existance: bool = None, kickable_opponent_existance: bool = None):
        pass
    intercept_table: InterceptTable
    our_team_name: str
    their_team_name: str
    our_side: Side
    last_set_play_start_time: int
    myself: Self
    ball: Ball
    teammates: List[Player]
    opponents: List[Player]
    unknowns: List[Player]
    our_players_dict: Dict[int, Player]
    their_players_dict: Dict[int, Player]
    our_goalie_uniform_number: int
    their_goalie_uniform_number: int
    offside_line_x: float
    offside_line_x_count: int
    kickable_teammate_id: int
    kickable_opponent_id: int
    last_kick_side: Side
    last_kicker_uniform_number: int
    cycle: int
    game_mode_type: GameModeType
    left_team_score: int
    right_team_score: int
    is_our_set_play: bool
    is_their_set_play: bool
    stoped_cycle: int
    our_team_score: int
    their_team_score: int
    is_penalty_kick_mode: bool
    helios_home_positions: Dict[int, RpcVector2D]
    our_defense_line_x: float
    their_defense_line_x: float
    our_defense_player_line_x: float
    their_defense_player_line_x: float
    kickable_teammate_existance: bool
    kickable_opponent_existance: bool

class State(object):
    def __init__(self, register_response: RegisterResponse = None, world_model: WorldModel = None, full_world_model: WorldModel = None):
        pass
    register_response: RegisterResponse
    world_model: WorldModel
    full_world_model: WorldModel

class InitMessage(object):
    def __init__(self, register_response: RegisterResponse = None, debug_mode: bool = None):
        pass
    register_response: RegisterResponse
    debug_mode: bool

class Dash(object):
    def __init__(self, power: float = None, relative_direction: float = None):
        pass
    power: float
    relative_direction: float

class Turn(object):
    def __init__(self, relative_direction: float = None):
        pass
    relative_direction: float

class Kick(object):
    def __init__(self, power: float = None, relative_direction: float = None):
        pass
    power: float
    relative_direction: float

class Tackle(object):
    def __init__(self, power_or_dir: float = None, foul: bool = None):
        pass
    power_or_dir: float
    foul: bool

class Catch(object):
    def __init__(self, ):
        pass
    pass

class Move(object):
    def __init__(self, x: float = None, y: float = None):
        pass
    x: float
    y: float

class TurnNeck(object):
    def __init__(self, moment: float = None):
        pass
    moment: float

class ChangeView(object):
    def __init__(self, view_width: ViewWidth = None):
        pass
    view_width: ViewWidth

class BallMessage(object):
    def __init__(self, ball_position: RpcVector2D = None, ball_velocity: RpcVector2D = None):
        pass
    ball_position: RpcVector2D
    ball_velocity: RpcVector2D

class PassMessage(object):
    def __init__(self, receiver_uniform_number: int = None, receiver_point: RpcVector2D = None, ball_position: RpcVector2D = None, ball_velocity: RpcVector2D = None):
        pass
    receiver_uniform_number: int
    receiver_point: RpcVector2D
    ball_position: RpcVector2D
    ball_velocity: RpcVector2D

class InterceptMessage(object):
    def __init__(self, our: bool = None, uniform_number: int = None, cycle: int = None):
        pass
    our: bool
    uniform_number: int
    cycle: int

class GoalieMessage(object):
    def __init__(self, goalie_uniform_number: int = None, goalie_position: RpcVector2D = None, goalie_body_direction: float = None):
        pass
    goalie_uniform_number: int
    goalie_position: RpcVector2D
    goalie_body_direction: float

class GoalieAndPlayerMessage(object):
    def __init__(self, goalie_uniform_number: int = None, goalie_position: RpcVector2D = None, goalie_body_direction: float = None, player_uniform_number: int = None, player_position: RpcVector2D = None):
        pass
    goalie_uniform_number: int
    goalie_position: RpcVector2D
    goalie_body_direction: float
    player_uniform_number: int
    player_position: RpcVector2D

class OffsideLineMessage(object):
    def __init__(self, offside_line_x: float = None):
        pass
    offside_line_x: float

class DefenseLineMessage(object):
    def __init__(self, defense_line_x: float = None):
        pass
    defense_line_x: float

class WaitRequestMessage(object):
    def __init__(self, ):
        pass
    pass

class SetplayMessage(object):
    def __init__(self, wait_step: int = None):
        pass
    wait_step: int

class PassRequestMessage(object):
    def __init__(self, target_point: RpcVector2D = None):
        pass
    target_point: RpcVector2D

class StaminaMessage(object):
    def __init__(self, stamina: float = None):
        pass
    stamina: float

class RecoveryMessage(object):
    def __init__(self, recovery: float = None):
        pass
    recovery: float

class StaminaCapacityMessage(object):
    def __init__(self, stamina_capacity: float = None):
        pass
    stamina_capacity: float

class DribbleMessage(object):
    def __init__(self, target_point: RpcVector2D = None, queue_count: int = None):
        pass
    target_point: RpcVector2D
    queue_count: int

class BallGoalieMessage(object):
    def __init__(self, ball_position: RpcVector2D = None, ball_velocity: RpcVector2D = None, goalie_position: RpcVector2D = None, goalie_body_direction: float = None):
        pass
    ball_position: RpcVector2D
    ball_velocity: RpcVector2D
    goalie_position: RpcVector2D
    goalie_body_direction: float

class OnePlayerMessage(object):
    def __init__(self, uniform_number: int = None, position: RpcVector2D = None):
        pass
    uniform_number: int
    position: RpcVector2D

class TwoPlayerMessage(object):
    def __init__(self, first_uniform_number: int = None, first_position: RpcVector2D = None, second_uniform_number: int = None, second_position: RpcVector2D = None):
        pass
    first_uniform_number: int
    first_position: RpcVector2D
    second_uniform_number: int
    second_position: RpcVector2D

class ThreePlayerMessage(object):
    def __init__(self, first_uniform_number: int = None, first_position: RpcVector2D = None, second_uniform_number: int = None, second_position: RpcVector2D = None, third_uniform_number: int = None, third_position: RpcVector2D = None):
        pass
    first_uniform_number: int
    first_position: RpcVector2D
    second_uniform_number: int
    second_position: RpcVector2D
    third_uniform_number: int
    third_position: RpcVector2D

class SelfMessage(object):
    def __init__(self, self_position: RpcVector2D = None, self_body_direction: float = None, self_stamina: float = None):
        pass
    self_position: RpcVector2D
    self_body_direction: float
    self_stamina: float

class TeammateMessage(object):
    def __init__(self, uniform_number: int = None, position: RpcVector2D = None, body_direction: float = None):
        pass
    uniform_number: int
    position: RpcVector2D
    body_direction: float

class OpponentMessage(object):
    def __init__(self, uniform_number: int = None, position: RpcVector2D = None, body_direction: float = None):
        pass
    uniform_number: int
    position: RpcVector2D
    body_direction: float

class BallPlayerMessage(object):
    def __init__(self, ball_position: RpcVector2D = None, ball_velocity: RpcVector2D = None, uniform_number: int = None, player_position: RpcVector2D = None, body_direction: float = None):
        pass
    ball_position: RpcVector2D
    ball_velocity: RpcVector2D
    uniform_number: int
    player_position: RpcVector2D
    body_direction: float

class Say(object):
    def __init__(self, ball_message: BallMessage = None, pass_message: PassMessage = None, intercept_message: InterceptMessage = None, goalie_message: GoalieMessage = None, goalie_and_player_message: GoalieAndPlayerMessage = None, offside_line_message: OffsideLineMessage = None, defense_line_message: DefenseLineMessage = None, wait_request_message: WaitRequestMessage = None, setplay_message: SetplayMessage = None, pass_request_message: PassRequestMessage = None, stamina_message: StaminaMessage = None, recovery_message: RecoveryMessage = None, stamina_capacity_message: StaminaCapacityMessage = None, dribble_message: DribbleMessage = None, ball_goalie_message: BallGoalieMessage = None, one_player_message: OnePlayerMessage = None, two_player_message: TwoPlayerMessage = None, three_player_message: ThreePlayerMessage = None, self_message: SelfMessage = None, teammate_message: TeammateMessage = None, opponent_message: OpponentMessage = None, ball_player_message: BallPlayerMessage = None):
        pass
    ball_message: BallMessage
    pass_message: PassMessage
    intercept_message: InterceptMessage
    goalie_message: GoalieMessage
    goalie_and_player_message: GoalieAndPlayerMessage
    offside_line_message: OffsideLineMessage
    defense_line_message: DefenseLineMessage
    wait_request_message: WaitRequestMessage
    setplay_message: SetplayMessage
    pass_request_message: PassRequestMessage
    stamina_message: StaminaMessage
    recovery_message: RecoveryMessage
    stamina_capacity_message: StaminaCapacityMessage
    dribble_message: DribbleMessage
    ball_goalie_message: BallGoalieMessage
    one_player_message: OnePlayerMessage
    two_player_message: TwoPlayerMessage
    three_player_message: ThreePlayerMessage
    self_message: SelfMessage
    teammate_message: TeammateMessage
    opponent_message: OpponentMessage
    ball_player_message: BallPlayerMessage

class PointTo(object):
    def __init__(self, x: float = None, y: float = None):
        pass
    x: float
    y: float

class PointToOf(object):
    def __init__(self, ):
        pass
    pass

class AttentionTo(object):
    def __init__(self, side: Side = None, unum: int = None):
        pass
    side: Side
    unum: int

class AttentionToOf(object):
    def __init__(self, ):
        pass
    pass

class AddText(object):
    def __init__(self, level: LoggerLevel = None, message: str = None):
        pass
    level: LoggerLevel
    message: str

class AddPoint(object):
    def __init__(self, level: LoggerLevel = None, point: RpcVector2D = None, color: str = None):
        pass
    level: LoggerLevel
    point: RpcVector2D
    color: str

class AddLine(object):
    def __init__(self, level: LoggerLevel = None, start_point: RpcVector2D = None, end_point: RpcVector2D = None, color: str = None):
        pass
    level: LoggerLevel
    start_point: RpcVector2D
    end_point: RpcVector2D
    color: str

class AddArc(object):
    def __init__(self, level: LoggerLevel = None, center: RpcVector2D = None, radius: float = None, start_angle: float = None, span_angel: float = None, color: str = None):
        pass
    level: LoggerLevel
    center: RpcVector2D
    radius: float
    start_angle: float
    span_angel: float
    color: str

class AddCircle(object):
    def __init__(self, level: LoggerLevel = None, center: RpcVector2D = None, radius: float = None, color: str = None, fill: bool = None):
        pass
    level: LoggerLevel
    center: RpcVector2D
    radius: float
    color: str
    fill: bool

class AddTriangle(object):
    def __init__(self, level: LoggerLevel = None, point1: RpcVector2D = None, point2: RpcVector2D = None, point3: RpcVector2D = None, color: str = None, fill: bool = None):
        pass
    level: LoggerLevel
    point1: RpcVector2D
    point2: RpcVector2D
    point3: RpcVector2D
    color: str
    fill: bool

class AddRectangle(object):
    def __init__(self, level: LoggerLevel = None, left: float = None, top: float = None, length: float = None, width: float = None, color: str = None, fill: bool = None):
        pass
    level: LoggerLevel
    left: float
    top: float
    length: float
    width: float
    color: str
    fill: bool

class AddSector(object):
    def __init__(self, level: LoggerLevel = None, center: RpcVector2D = None, min_radius: float = None, max_radius: float = None, start_angle: float = None, span_angel: float = None, color: str = None, fill: bool = None):
        pass
    level: LoggerLevel
    center: RpcVector2D
    min_radius: float
    max_radius: float
    start_angle: float
    span_angel: float
    color: str
    fill: bool

class AddMessage(object):
    def __init__(self, level: LoggerLevel = None, position: RpcVector2D = None, message: str = None, color: str = None):
        pass
    level: LoggerLevel
    position: RpcVector2D
    message: str
    color: str

class Log(object):
    def __init__(self, add_text: AddText = None, add_point: AddPoint = None, add_line: AddLine = None, add_arc: AddArc = None, add_circle: AddCircle = None, add_triangle: AddTriangle = None, add_rectangle: AddRectangle = None, add_sector: AddSector = None, add_message: AddMessage = None):
        pass
    add_text: AddText
    add_point: AddPoint
    add_line: AddLine
    add_arc: AddArc
    add_circle: AddCircle
    add_triangle: AddTriangle
    add_rectangle: AddRectangle
    add_sector: AddSector
    add_message: AddMessage

class DebugClient(object):
    def __init__(self, message: str = None):
        pass
    message: str

class Body_GoToPoint(object):
    def __init__(self, target_point: RpcVector2D = None, distance_threshold: float = None, max_dash_power: float = None):
        pass
    target_point: RpcVector2D
    distance_threshold: float
    max_dash_power: float

class Body_SmartKick(object):
    def __init__(self, target_point: RpcVector2D = None, first_speed: float = None, first_speed_threshold: float = None, max_steps: int = None):
        pass
    target_point: RpcVector2D
    first_speed: float
    first_speed_threshold: float
    max_steps: int

class Bhv_BeforeKickOff(object):
    def __init__(self, point: RpcVector2D = None):
        pass
    point: RpcVector2D

class Bhv_BodyNeckToBall(object):
    def __init__(self, ):
        pass
    pass

class Bhv_BodyNeckToPoint(object):
    def __init__(self, point: RpcVector2D = None):
        pass
    point: RpcVector2D

class Bhv_Emergency(object):
    def __init__(self, ):
        pass
    pass

class Bhv_GoToPointLookBall(object):
    def __init__(self, target_point: RpcVector2D = None, distance_threshold: float = None, max_dash_power: float = None):
        pass
    target_point: RpcVector2D
    distance_threshold: float
    max_dash_power: float

class Bhv_NeckBodyToBall(object):
    def __init__(self, angle_buf: float = None):
        pass
    angle_buf: float

class Bhv_NeckBodyToPoint(object):
    def __init__(self, point: RpcVector2D = None, angle_buf: float = None):
        pass
    point: RpcVector2D
    angle_buf: float

class Bhv_ScanField(object):
    def __init__(self, ):
        pass
    pass

class Body_AdvanceBall(object):
    def __init__(self, ):
        pass
    pass

class Body_ClearBall(object):
    def __init__(self, ):
        pass
    pass

class Body_Dribble(object):
    def __init__(self, target_point: RpcVector2D = None, distance_threshold: float = None, dash_power: float = None, dash_count: int = None, dodge: bool = None):
        pass
    target_point: RpcVector2D
    distance_threshold: float
    dash_power: float
    dash_count: int
    dodge: bool

class Body_GoToPointDodge(object):
    def __init__(self, target_point: RpcVector2D = None, dash_power: float = None):
        pass
    target_point: RpcVector2D
    dash_power: float

class Body_HoldBall(object):
    def __init__(self, do_turn: bool = None, turn_target_point: RpcVector2D = None, kick_target_point: RpcVector2D = None):
        pass
    do_turn: bool
    turn_target_point: RpcVector2D
    kick_target_point: RpcVector2D

class Body_Intercept(object):
    def __init__(self, save_recovery: bool = None, face_point: RpcVector2D = None):
        pass
    save_recovery: bool
    face_point: RpcVector2D

class Body_KickOneStep(object):
    def __init__(self, target_point: RpcVector2D = None, first_speed: float = None, force_mode: bool = None):
        pass
    target_point: RpcVector2D
    first_speed: float
    force_mode: bool

class Body_StopBall(object):
    def __init__(self, ):
        pass
    pass

class Body_StopDash(object):
    def __init__(self, save_recovery: bool = None):
        pass
    save_recovery: bool

class Body_TackleToPoint(object):
    def __init__(self, target_point: RpcVector2D = None, min_probability: float = None, min_speed: float = None):
        pass
    target_point: RpcVector2D
    min_probability: float
    min_speed: float

class Body_TurnToAngle(object):
    def __init__(self, angle: float = None):
        pass
    angle: float

class Body_TurnToBall(object):
    def __init__(self, cycle: int = None):
        pass
    cycle: int

class Body_TurnToPoint(object):
    def __init__(self, target_point: RpcVector2D = None, cycle: int = None):
        pass
    target_point: RpcVector2D
    cycle: int

class Focus_MoveToPoint(object):
    def __init__(self, target_point: RpcVector2D = None):
        pass
    target_point: RpcVector2D

class Focus_Reset(object):
    def __init__(self, ):
        pass
    pass

class Neck_ScanField(object):
    def __init__(self, ):
        pass
    pass

class Neck_ScanPlayers(object):
    def __init__(self, ):
        pass
    pass

class Neck_TurnToBallAndPlayer(object):
    def __init__(self, side: Side = None, uniform_number: int = None, count_threshold: int = None):
        pass
    side: Side
    uniform_number: int
    count_threshold: int

class Neck_TurnToBallOrScan(object):
    def __init__(self, count_threshold: int = None):
        pass
    count_threshold: int

class Neck_TurnToBall(object):
    def __init__(self, ):
        pass
    pass

class Neck_TurnToGoalieOrScan(object):
    def __init__(self, count_threshold: int = None):
        pass
    count_threshold: int

class Neck_TurnToLowConfTeammate(object):
    def __init__(self, ):
        pass
    pass

class Neck_TurnToPlayerOrScan(object):
    def __init__(self, side: Side = None, uniform_number: int = None, count_threshold: int = None):
        pass
    side: Side
    uniform_number: int
    count_threshold: int

class Neck_TurnToPoint(object):
    def __init__(self, target_point: RpcVector2D = None):
        pass
    target_point: RpcVector2D

class Neck_TurnToRelative(object):
    def __init__(self, angle: float = None):
        pass
    angle: float

class View_ChangeWidth(object):
    def __init__(self, view_width: ViewWidth = None):
        pass
    view_width: ViewWidth

class View_Normal(object):
    def __init__(self, ):
        pass
    pass

class View_Synch(object):
    def __init__(self, ):
        pass
    pass

class View_Wide(object):
    def __init__(self, ):
        pass
    pass

class HeliosGoalie(object):
    def __init__(self, ):
        pass
    pass

class HeliosGoalieMove(object):
    def __init__(self, ):
        pass
    pass

class HeliosGoalieKick(object):
    def __init__(self, ):
        pass
    pass

class HeliosShoot(object):
    def __init__(self, ):
        pass
    pass

class HeliosChainAction(object):
    def __init__(self, direct_pass: bool = None, lead_pass: bool = None, through_pass: bool = None, short_dribble: bool = None, long_dribble: bool = None, cross: bool = None, simple_pass: bool = None, simple_dribble: bool = None, simple_shoot: bool = None):
        pass
    direct_pass: bool
    lead_pass: bool
    through_pass: bool
    short_dribble: bool
    long_dribble: bool
    cross: bool
    simple_pass: bool
    simple_dribble: bool
    simple_shoot: bool

class HeliosBasicOffensive(object):
    def __init__(self, ):
        pass
    pass

class HeliosBasicMove(object):
    def __init__(self, ):
        pass
    pass

class HeliosSetPlay(object):
    def __init__(self, ):
        pass
    pass

class HeliosPenalty(object):
    def __init__(self, ):
        pass
    pass

class HeliosCommunicaion(object):
    def __init__(self, ):
        pass
    pass

class PlayerAction(object):
    def __init__(self, dash: Dash = None, turn: Turn = None, kick: Kick = None, tackle: Tackle = None, catch_action: Catch = None, move: Move = None, turn_neck: TurnNeck = None, change_view: ChangeView = None, say: Say = None, point_to: PointTo = None, point_to_of: PointToOf = None, attention_to: AttentionTo = None, attention_to_of: AttentionToOf = None, log: Log = None, debug_client: DebugClient = None, body_go_to_point: Body_GoToPoint = None, body_smart_kick: Body_SmartKick = None, bhv_before_kick_off: Bhv_BeforeKickOff = None, bhv_body_neck_to_ball: Bhv_BodyNeckToBall = None, bhv_body_neck_to_point: Bhv_BodyNeckToPoint = None, bhv_emergency: Bhv_Emergency = None, bhv_go_to_point_look_ball: Bhv_GoToPointLookBall = None, bhv_neck_body_to_ball: Bhv_NeckBodyToBall = None, bhv_neck_body_to_point: Bhv_NeckBodyToPoint = None, bhv_scan_field: Bhv_ScanField = None, body_advance_ball: Body_AdvanceBall = None, body_clear_ball: Body_ClearBall = None, body_dribble: Body_Dribble = None, body_go_to_point_dodge: Body_GoToPointDodge = None, body_hold_ball: Body_HoldBall = None, body_intercept: Body_Intercept = None, body_kick_one_step: Body_KickOneStep = None, body_stop_ball: Body_StopBall = None, body_stop_dash: Body_StopDash = None, body_tackle_to_point: Body_TackleToPoint = None, body_turn_to_angle: Body_TurnToAngle = None, body_turn_to_ball: Body_TurnToBall = None, body_turn_to_point: Body_TurnToPoint = None, focus_move_to_point: Focus_MoveToPoint = None, focus_reset: Focus_Reset = None, neck_scan_field: Neck_ScanField = None, neck_scan_players: Neck_ScanPlayers = None, neck_turn_to_ball_and_player: Neck_TurnToBallAndPlayer = None, neck_turn_to_ball_or_scan: Neck_TurnToBallOrScan = None, neck_turn_to_ball: Neck_TurnToBall = None, neck_turn_to_goalie_or_scan: Neck_TurnToGoalieOrScan = None, neck_turn_to_low_conf_teammate: Neck_TurnToLowConfTeammate = None, neck_turn_to_player_or_scan: Neck_TurnToPlayerOrScan = None, neck_turn_to_point: Neck_TurnToPoint = None, neck_turn_to_relative: Neck_TurnToRelative = None, view_change_width: View_ChangeWidth = None, view_normal: View_Normal = None, view_synch: View_Synch = None, view_wide: View_Wide = None, helios_goalie: HeliosGoalie = None, helios_goalie_move: HeliosGoalieMove = None, helios_goalie_kick: HeliosGoalieKick = None, helios_shoot: HeliosShoot = None, helios_chain_action: HeliosChainAction = None, helios_basic_offensive: HeliosBasicOffensive = None, helios_basic_move: HeliosBasicMove = None, helios_set_play: HeliosSetPlay = None, helios_penalty: HeliosPenalty = None, helios_communication: HeliosCommunicaion = None):
        pass
    dash: Dash
    turn: Turn
    kick: Kick
    tackle: Tackle
    catch_action: Catch
    move: Move
    turn_neck: TurnNeck
    change_view: ChangeView
    say: Say
    point_to: PointTo
    point_to_of: PointToOf
    attention_to: AttentionTo
    attention_to_of: AttentionToOf
    log: Log
    debug_client: DebugClient
    body_go_to_point: Body_GoToPoint
    body_smart_kick: Body_SmartKick
    bhv_before_kick_off: Bhv_BeforeKickOff
    bhv_body_neck_to_ball: Bhv_BodyNeckToBall
    bhv_body_neck_to_point: Bhv_BodyNeckToPoint
    bhv_emergency: Bhv_Emergency
    bhv_go_to_point_look_ball: Bhv_GoToPointLookBall
    bhv_neck_body_to_ball: Bhv_NeckBodyToBall
    bhv_neck_body_to_point: Bhv_NeckBodyToPoint
    bhv_scan_field: Bhv_ScanField
    body_advance_ball: Body_AdvanceBall
    body_clear_ball: Body_ClearBall
    body_dribble: Body_Dribble
    body_go_to_point_dodge: Body_GoToPointDodge
    body_hold_ball: Body_HoldBall
    body_intercept: Body_Intercept
    body_kick_one_step: Body_KickOneStep
    body_stop_ball: Body_StopBall
    body_stop_dash: Body_StopDash
    body_tackle_to_point: Body_TackleToPoint
    body_turn_to_angle: Body_TurnToAngle
    body_turn_to_ball: Body_TurnToBall
    body_turn_to_point: Body_TurnToPoint
    focus_move_to_point: Focus_MoveToPoint
    focus_reset: Focus_Reset
    neck_scan_field: Neck_ScanField
    neck_scan_players: Neck_ScanPlayers
    neck_turn_to_ball_and_player: Neck_TurnToBallAndPlayer
    neck_turn_to_ball_or_scan: Neck_TurnToBallOrScan
    neck_turn_to_ball: Neck_TurnToBall
    neck_turn_to_goalie_or_scan: Neck_TurnToGoalieOrScan
    neck_turn_to_low_conf_teammate: Neck_TurnToLowConfTeammate
    neck_turn_to_player_or_scan: Neck_TurnToPlayerOrScan
    neck_turn_to_point: Neck_TurnToPoint
    neck_turn_to_relative: Neck_TurnToRelative
    view_change_width: View_ChangeWidth
    view_normal: View_Normal
    view_synch: View_Synch
    view_wide: View_Wide
    helios_goalie: HeliosGoalie
    helios_goalie_move: HeliosGoalieMove
    helios_goalie_kick: HeliosGoalieKick
    helios_shoot: HeliosShoot
    helios_chain_action: HeliosChainAction
    helios_basic_offensive: HeliosBasicOffensive
    helios_basic_move: HeliosBasicMove
    helios_set_play: HeliosSetPlay
    helios_penalty: HeliosPenalty
    helios_communication: HeliosCommunicaion

class PlayerActions(object):
    def __init__(self, actions: List[PlayerAction] = None):
        pass
    actions: List[PlayerAction]

class ChangePlayerType(object):
    def __init__(self, uniform_number: int = None, type: int = None):
        pass
    uniform_number: int
    type: int

class DoHeliosSubstitute(object):
    def __init__(self, ):
        pass
    pass

class DoHeliosSayPlayerTypes(object):
    def __init__(self, ):
        pass
    pass

class CoachAction(object):
    def __init__(self, change_player_types: ChangePlayerType = None, do_helios_substitute: DoHeliosSubstitute = None, do_helios_say_player_types: DoHeliosSayPlayerTypes = None):
        pass
    change_player_types: ChangePlayerType
    do_helios_substitute: DoHeliosSubstitute
    do_helios_say_player_types: DoHeliosSayPlayerTypes

class CoachActions(object):
    def __init__(self, actions: List[CoachAction] = None):
        pass
    actions: List[CoachAction]

class DoKickOff(object):
    def __init__(self, ):
        pass
    pass

class DoMoveBall(object):
    def __init__(self, position: RpcVector2D = None, velocity: RpcVector2D = None):
        pass
    position: RpcVector2D
    velocity: RpcVector2D

class DoMovePlayer(object):
    def __init__(self, our_side: bool = None, uniform_number: int = None, position: RpcVector2D = None, body_direction: float = None):
        pass
    our_side: bool
    uniform_number: int
    position: RpcVector2D
    body_direction: float

class DoRecover(object):
    def __init__(self, ):
        pass
    pass

class DoChangeMode(object):
    def __init__(self, game_mode_type: GameModeType = None, side: Side = None):
        pass
    game_mode_type: GameModeType
    side: Side

class DoChangePlayerType(object):
    def __init__(self, our_side: bool = None, uniform_number: int = None, type: int = None):
        pass
    our_side: bool
    uniform_number: int
    type: int

class TrainerAction(object):
    def __init__(self, do_kick_off: DoKickOff = None, do_move_ball: DoMoveBall = None, do_move_player: DoMovePlayer = None, do_recover: DoRecover = None, do_change_mode: DoChangeMode = None, do_change_player_type: DoChangePlayerType = None):
        pass
    do_kick_off: DoKickOff
    do_move_ball: DoMoveBall
    do_move_player: DoMovePlayer
    do_recover: DoRecover
    do_change_mode: DoChangeMode
    do_change_player_type: DoChangePlayerType

class TrainerActions(object):
    def __init__(self, actions: List[TrainerAction] = None):
        pass
    actions: List[TrainerAction]

class ServerParam(object):
    def __init__(self, register_response: RegisterResponse = None, inertia_moment: float = None, player_size: float = None, player_decay: float = None, player_rand: float = None, player_weight: float = None, player_speed_max: float = None, player_accel_max: float = None, stamina_max: float = None, stamina_inc_max: float = None, recover_init: float = None, recover_dec_thr: float = None, recover_min: float = None, recover_dec: float = None, effort_init: float = None, effort_dec_thr: float = None, effort_min: float = None, effort_dec: float = None, effort_inc_thr: float = None, effort_inc: float = None, kick_rand: float = None, team_actuator_noise: bool = None, player_rand_factor_l: float = None, player_rand_factor_r: float = None, kick_rand_factor_l: float = None, kick_rand_factor_r: float = None, ball_size: float = None, ball_decay: float = None, ball_rand: float = None, ball_weight: float = None, ball_speed_max: float = None, ball_accel_max: float = None, dash_power_rate: float = None, kick_power_rate: float = None, kickable_margin: float = None, control_radius: float = None, control_radius_width: float = None, max_power: float = None, min_power: float = None, max_moment: float = None, min_moment: float = None, max_neck_moment: float = None, min_neck_moment: float = None, max_neck_angle: float = None, min_neck_angle: float = None, visible_angle: float = None, visible_distance: float = None, wind_dir: float = None, wind_force: float = None, wind_angle: float = None, wind_rand: float = None, kickable_area: float = None, catch_area_l: float = None, catch_area_w: float = None, catch_probability: float = None, goalie_max_moves: int = None, corner_kick_margin: float = None, offside_active_area_size: float = None, wind_none: bool = None, use_wind_random: bool = None, coach_say_count_max: int = None, coach_say_msg_size: int = None, clang_win_size: int = None, clang_define_win: int = None, clang_meta_win: int = None, clang_advice_win: int = None, clang_info_win: int = None, clang_mess_delay: int = None, clang_mess_per_cycle: int = None, half_time: int = None, simulator_step: int = None, send_step: int = None, recv_step: int = None, sense_body_step: int = None, lcm_step: int = None, player_say_msg_size: int = None, player_hear_max: int = None, player_hear_inc: int = None, player_hear_decay: int = None, catch_ban_cycle: int = None, slow_down_factor: int = None, use_offside: bool = None, kickoff_offside: bool = None, offside_kick_margin: float = None, audio_cut_dist: float = None, dist_quantize_step: float = None, landmark_dist_quantize_step: float = None, dir_quantize_step: float = None, dist_quantize_step_l: float = None, dist_quantize_step_r: float = None, landmark_dist_quantize_step_l: float = None, landmark_dist_quantize_step_r: float = None, dir_quantize_step_l: float = None, dir_quantize_step_r: float = None, coach_mode: bool = None, coach_with_referee_mode: bool = None, use_old_coach_hear: bool = None, slowness_on_top_for_left_team: float = None, slowness_on_top_for_right_team: float = None, start_goal_l: int = None, start_goal_r: int = None, fullstate_l: bool = None, fullstate_r: bool = None, drop_ball_time: int = None, synch_mode: bool = None, synch_offset: int = None, synch_micro_sleep: int = None, point_to_ban: int = None, point_to_duration: int = None, player_port: int = None, trainer_port: int = None, online_coach_port: int = None, verbose_mode: bool = None, coach_send_vi_step: int = None, replay_file: str = None, landmark_file: str = None, send_comms: bool = None, text_logging: bool = None, game_logging: bool = None, game_log_version: int = None, text_log_dir: str = None, game_log_dir: str = None, text_log_fixed_name: str = None, game_log_fixed_name: str = None, use_text_log_fixed: bool = None, use_game_log_fixed: bool = None, use_text_log_dated: bool = None, use_game_log_dated: bool = None, log_date_format: str = None, log_times: bool = None, record_message: bool = None, text_log_compression: int = None, game_log_compression: int = None, use_profile: bool = None, tackle_dist: float = None, tackle_back_dist: float = None, tackle_width: float = None, tackle_exponent: float = None, tackle_cycles: int = None, tackle_power_rate: float = None, freeform_wait_period: int = None, freeform_send_period: int = None, free_kick_faults: bool = None, back_passes: bool = None, proper_goal_kicks: bool = None, stopped_ball_vel: float = None, max_goal_kicks: int = None, clang_del_win: int = None, clang_rule_win: int = None, auto_mode: bool = None, kick_off_wait: int = None, connect_wait: int = None, game_over_wait: int = None, team_l_start: str = None, team_r_start: str = None, keepaway_mode: bool = None, keepaway_length: float = None, keepaway_width: float = None, keepaway_logging: bool = None, keepaway_log_dir: str = None, keepaway_log_fixed_name: str = None, keepaway_log_fixed: bool = None, keepaway_log_dated: bool = None, keepaway_start: int = None, nr_normal_halfs: int = None, nr_extra_halfs: int = None, penalty_shoot_outs: bool = None, pen_before_setup_wait: int = None, pen_setup_wait: int = None, pen_ready_wait: int = None, pen_taken_wait: int = None, pen_nr_kicks: int = None, pen_max_extra_kicks: int = None, pen_dist_x: float = None, pen_random_winner: bool = None, pen_allow_mult_kicks: bool = None, pen_max_goalie_dist_x: float = None, pen_coach_moves_players: bool = None, module_dir: str = None, ball_stuck_area: float = None, coach_msg_file: str = None, max_tackle_power: float = None, max_back_tackle_power: float = None, player_speed_max_min: float = None, extra_stamina: float = None, synch_see_offset: int = None, extra_half_time: int = None, stamina_capacity: float = None, max_dash_angle: float = None, min_dash_angle: float = None, dash_angle_step: float = None, side_dash_rate: float = None, back_dash_rate: float = None, max_dash_power: float = None, min_dash_power: float = None, tackle_rand_factor: float = None, foul_detect_probability: float = None, foul_exponent: float = None, foul_cycles: int = None, golden_goal: bool = None, red_card_probability: float = None, illegal_defense_duration: int = None, illegal_defense_number: int = None, illegal_defense_dist_x: float = None, illegal_defense_width: float = None, fixed_teamname_l: str = None, fixed_teamname_r: str = None, max_catch_angle: float = None, min_catch_angle: float = None, random_seed: int = None, long_kick_power_factor: float = None, long_kick_delay: int = None, max_monitors: int = None, catchable_area: float = None, real_speed_max: float = None, pitch_half_length: float = None, pitch_half_width: float = None, our_penalty_area_line_x: float = None, their_penalty_area_line_x: float = None, penalty_area_half_width: float = None, penalty_area_length: float = None, goal_width: float = None):
        pass
    register_response: RegisterResponse
    inertia_moment: float
    player_size: float
    player_decay: float
    player_rand: float
    player_weight: float
    player_speed_max: float
    player_accel_max: float
    stamina_max: float
    stamina_inc_max: float
    recover_init: float
    recover_dec_thr: float
    recover_min: float
    recover_dec: float
    effort_init: float
    effort_dec_thr: float
    effort_min: float
    effort_dec: float
    effort_inc_thr: float
    effort_inc: float
    kick_rand: float
    team_actuator_noise: bool
    player_rand_factor_l: float
    player_rand_factor_r: float
    kick_rand_factor_l: float
    kick_rand_factor_r: float
    ball_size: float
    ball_decay: float
    ball_rand: float
    ball_weight: float
    ball_speed_max: float
    ball_accel_max: float
    dash_power_rate: float
    kick_power_rate: float
    kickable_margin: float
    control_radius: float
    control_radius_width: float
    max_power: float
    min_power: float
    max_moment: float
    min_moment: float
    max_neck_moment: float
    min_neck_moment: float
    max_neck_angle: float
    min_neck_angle: float
    visible_angle: float
    visible_distance: float
    wind_dir: float
    wind_force: float
    wind_angle: float
    wind_rand: float
    kickable_area: float
    catch_area_l: float
    catch_area_w: float
    catch_probability: float
    goalie_max_moves: int
    corner_kick_margin: float
    offside_active_area_size: float
    wind_none: bool
    use_wind_random: bool
    coach_say_count_max: int
    coach_say_msg_size: int
    clang_win_size: int
    clang_define_win: int
    clang_meta_win: int
    clang_advice_win: int
    clang_info_win: int
    clang_mess_delay: int
    clang_mess_per_cycle: int
    half_time: int
    simulator_step: int
    send_step: int
    recv_step: int
    sense_body_step: int
    lcm_step: int
    player_say_msg_size: int
    player_hear_max: int
    player_hear_inc: int
    player_hear_decay: int
    catch_ban_cycle: int
    slow_down_factor: int
    use_offside: bool
    kickoff_offside: bool
    offside_kick_margin: float
    audio_cut_dist: float
    dist_quantize_step: float
    landmark_dist_quantize_step: float
    dir_quantize_step: float
    dist_quantize_step_l: float
    dist_quantize_step_r: float
    landmark_dist_quantize_step_l: float
    landmark_dist_quantize_step_r: float
    dir_quantize_step_l: float
    dir_quantize_step_r: float
    coach_mode: bool
    coach_with_referee_mode: bool
    use_old_coach_hear: bool
    slowness_on_top_for_left_team: float
    slowness_on_top_for_right_team: float
    start_goal_l: int
    start_goal_r: int
    fullstate_l: bool
    fullstate_r: bool
    drop_ball_time: int
    synch_mode: bool
    synch_offset: int
    synch_micro_sleep: int
    point_to_ban: int
    point_to_duration: int
    player_port: int
    trainer_port: int
    online_coach_port: int
    verbose_mode: bool
    coach_send_vi_step: int
    replay_file: str
    landmark_file: str
    send_comms: bool
    text_logging: bool
    game_logging: bool
    game_log_version: int
    text_log_dir: str
    game_log_dir: str
    text_log_fixed_name: str
    game_log_fixed_name: str
    use_text_log_fixed: bool
    use_game_log_fixed: bool
    use_text_log_dated: bool
    use_game_log_dated: bool
    log_date_format: str
    log_times: bool
    record_message: bool
    text_log_compression: int
    game_log_compression: int
    use_profile: bool
    tackle_dist: float
    tackle_back_dist: float
    tackle_width: float
    tackle_exponent: float
    tackle_cycles: int
    tackle_power_rate: float
    freeform_wait_period: int
    freeform_send_period: int
    free_kick_faults: bool
    back_passes: bool
    proper_goal_kicks: bool
    stopped_ball_vel: float
    max_goal_kicks: int
    clang_del_win: int
    clang_rule_win: int
    auto_mode: bool
    kick_off_wait: int
    connect_wait: int
    game_over_wait: int
    team_l_start: str
    team_r_start: str
    keepaway_mode: bool
    keepaway_length: float
    keepaway_width: float
    keepaway_logging: bool
    keepaway_log_dir: str
    keepaway_log_fixed_name: str
    keepaway_log_fixed: bool
    keepaway_log_dated: bool
    keepaway_start: int
    nr_normal_halfs: int
    nr_extra_halfs: int
    penalty_shoot_outs: bool
    pen_before_setup_wait: int
    pen_setup_wait: int
    pen_ready_wait: int
    pen_taken_wait: int
    pen_nr_kicks: int
    pen_max_extra_kicks: int
    pen_dist_x: float
    pen_random_winner: bool
    pen_allow_mult_kicks: bool
    pen_max_goalie_dist_x: float
    pen_coach_moves_players: bool
    module_dir: str
    ball_stuck_area: float
    coach_msg_file: str
    max_tackle_power: float
    max_back_tackle_power: float
    player_speed_max_min: float
    extra_stamina: float
    synch_see_offset: int
    extra_half_time: int
    stamina_capacity: float
    max_dash_angle: float
    min_dash_angle: float
    dash_angle_step: float
    side_dash_rate: float
    back_dash_rate: float
    max_dash_power: float
    min_dash_power: float
    tackle_rand_factor: float
    foul_detect_probability: float
    foul_exponent: float
    foul_cycles: int
    golden_goal: bool
    red_card_probability: float
    illegal_defense_duration: int
    illegal_defense_number: int
    illegal_defense_dist_x: float
    illegal_defense_width: float
    fixed_teamname_l: str
    fixed_teamname_r: str
    max_catch_angle: float
    min_catch_angle: float
    random_seed: int
    long_kick_power_factor: float
    long_kick_delay: int
    max_monitors: int
    catchable_area: float
    real_speed_max: float
    pitch_half_length: float
    pitch_half_width: float
    our_penalty_area_line_x: float
    their_penalty_area_line_x: float
    penalty_area_half_width: float
    penalty_area_length: float
    goal_width: float

class PlayerParam(object):
    def __init__(self, register_response: RegisterResponse = None, player_types: int = None, subs_max: int = None, pt_max: int = None, allow_mult_default_type: bool = None, player_speed_max_delta_min: float = None, player_speed_max_delta_max: float = None, stamina_inc_max_delta_factor: float = None, player_decay_delta_min: float = None, player_decay_delta_max: float = None, inertia_moment_delta_factor: float = None, dash_power_rate_delta_min: float = None, dash_power_rate_delta_max: float = None, player_size_delta_factor: float = None, kickable_margin_delta_min: float = None, kickable_margin_delta_max: float = None, kick_rand_delta_factor: float = None, extra_stamina_delta_min: float = None, extra_stamina_delta_max: float = None, effort_max_delta_factor: float = None, effort_min_delta_factor: float = None, random_seed: int = None, new_dash_power_rate_delta_min: float = None, new_dash_power_rate_delta_max: float = None, new_stamina_inc_max_delta_factor: float = None, kick_power_rate_delta_min: float = None, kick_power_rate_delta_max: float = None, foul_detect_probability_delta_factor: float = None, catchable_area_l_stretch_min: float = None, catchable_area_l_stretch_max: float = None):
        pass
    register_response: RegisterResponse
    player_types: int
    subs_max: int
    pt_max: int
    allow_mult_default_type: bool
    player_speed_max_delta_min: float
    player_speed_max_delta_max: float
    stamina_inc_max_delta_factor: float
    player_decay_delta_min: float
    player_decay_delta_max: float
    inertia_moment_delta_factor: float
    dash_power_rate_delta_min: float
    dash_power_rate_delta_max: float
    player_size_delta_factor: float
    kickable_margin_delta_min: float
    kickable_margin_delta_max: float
    kick_rand_delta_factor: float
    extra_stamina_delta_min: float
    extra_stamina_delta_max: float
    effort_max_delta_factor: float
    effort_min_delta_factor: float
    random_seed: int
    new_dash_power_rate_delta_min: float
    new_dash_power_rate_delta_max: float
    new_stamina_inc_max_delta_factor: float
    kick_power_rate_delta_min: float
    kick_power_rate_delta_max: float
    foul_detect_probability_delta_factor: float
    catchable_area_l_stretch_min: float
    catchable_area_l_stretch_max: float

class PlayerType(object):
    def __init__(self, register_response: RegisterResponse = None, id: int = None, stamina_inc_max: float = None, player_decay: float = None, inertia_moment: float = None, dash_power_rate: float = None, player_size: float = None, kickable_margin: float = None, kick_rand: float = None, extra_stamina: float = None, effort_max: float = None, effort_min: float = None, kick_power_rate: float = None, foul_detect_probability: float = None, catchable_area_l_stretch: float = None, unum_far_length: float = None, unum_too_far_length: float = None, team_far_length: float = None, team_too_far_length: float = None, player_max_observation_length: float = None, ball_vel_far_length: float = None, ball_vel_too_far_length: float = None, ball_max_observation_length: float = None, flag_chg_far_length: float = None, flag_chg_too_far_length: float = None, flag_max_observation_length: float = None, kickable_area: float = None, reliable_catchable_dist: float = None, max_catchable_dist: float = None, real_speed_max: float = None, player_speed_max2: float = None, real_speed_max2: float = None, cycles_to_reach_max_speed: int = None, player_speed_max: float = None):
        pass
    register_response: RegisterResponse
    id: int
    stamina_inc_max: float
    player_decay: float
    inertia_moment: float
    dash_power_rate: float
    player_size: float
    kickable_margin: float
    kick_rand: float
    extra_stamina: float
    effort_max: float
    effort_min: float
    kick_power_rate: float
    foul_detect_probability: float
    catchable_area_l_stretch: float
    unum_far_length: float
    unum_too_far_length: float
    team_far_length: float
    team_too_far_length: float
    player_max_observation_length: float
    ball_vel_far_length: float
    ball_vel_too_far_length: float
    ball_max_observation_length: float
    flag_chg_far_length: float
    flag_chg_too_far_length: float
    flag_max_observation_length: float
    kickable_area: float
    reliable_catchable_dist: float
    max_catchable_dist: float
    real_speed_max: float
    player_speed_max2: float
    real_speed_max2: float
    cycles_to_reach_max_speed: int
    player_speed_max: float

class Empty(object):
    def __init__(self, ):
        pass
    pass
