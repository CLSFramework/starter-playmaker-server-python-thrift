from src.IAgent import IAgent
import math
from src.Dribble import Dribble
from soccer.ttypes import *
from src.Tools import Tools
from src.setplay.BhvGoToPlacedBall import BhvGoToPlacedBall
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.soccer_math import inertia_n_step_point
from pyrusgeom.ray_2d import Ray2D
from pyrusgeom.size_2d import Size2D
from pyrusgeom.rect_2d import Rect2D
from pyrusgeom.line_2d import Line2D
from src.ClearBall import ClearBall
class BhvPenaltyKick:
    
    def __init__(self):
        pass

    def Decision(agent: IAgent):
        
        wm = agent.wm
        actions = []
        state = wm.penalty_kick_state
        if wm.game_mode_type == GameModeType.PenaltySetup_:
            if state.current_taker_side == wm.our_side:
                if state.is_kick_taker:
                    print('kicker: ', wm.myself.uniform_number)
                    return BhvPenaltyKick.doKickerSetup(agent)
            else:
                if wm.myself.is_goalie:
                    return BhvPenaltyKick.doGoalieSetup(agent)
        elif wm.game_mode_type == GameModeType.PenaltyReady_:
            if state.current_taker_side == wm.our_side:
                if state.is_kick_taker:
                    return BhvPenaltyKick.doKickerReady(agent)
            else:
                if wm.myself.is_goalie:
                    return BhvPenaltyKick.doGoalieSetup(agent)
        elif wm.game_mode_type == GameModeType.PenaltyTaken_:
            if state.current_taker_side == wm.our_side:
                if state.is_kick_taker:
                    return BhvPenaltyKick.doKicker(agent)
            else:
                if wm.myself.is_goalie:
                    return BhvPenaltyKick.doGoalie(agent)
        elif wm.game_mode_type == GameModeType.PenaltyScore_ or wm.game_mode_type == GameModeType.PenaltyMiss_:
            if state.current_taker_side == wm.our_side: #TODO check
                if wm.myself.is_goalie:
                    return BhvPenaltyKick.doGoalieSetup(agent)
        elif wm.game_mode_type == GameModeType.PenaltyOnfield_ or wm.game_mode_type == GameModeType.PenaltyFoul_:
            pass
        else:
            print("Current playmode is NOT a Penalty Shootout???")
            return actions

        if wm.myself.is_goalie:
            return BhvPenaltyKick.doGoalieWait(agent)
        else:
            return BhvPenaltyKick.doKickerWait(agent)

    def doKickerWait(agent: IAgent):
        wm = agent.wm
        actions = []
        dist_step = (9.0 + 9.0) / 12
        wait_pos = Vector2D(-2.0, -9.8 + dist_step * agent.wm.myself.uniform_number)
        
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        
        if self_position.dist(wait_pos) < 0.7:
            actions.append((PlayerAction(bhv_neck_body_to_ball=Bhv_NeckBodyToBall())))
        else:
            actions.append((PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(wait_pos.x(), wait_pos.y()), 0.3, agent.serverParams.max_dash_power))))
        return actions
            

    def doKickerSetup(agent: IAgent):
        actions = []
        goal_c = Vector2D(agent.serverParams.pitch_half_length, 0.0)
        opps = agent.wm.opponents
        
        opp_goalie = Tools.OpponentGoalie(agent)
        
        place_angle = 0.0
        go_to_placed_ball = BhvGoToPlacedBall(place_angle).Decision(agent)
        if  go_to_placed_ball == []:
            actions.append((PlayerAction(body_turn_to_point= Body_TurnToPoint(RpcVector2D(goal_c.x(), goal_c.y())))))
            if opp_goalie :
                actions.append((PlayerAction(neck_turn_to_point= Neck_TurnToPoint(opp_goalie.position))))
            else : 
                actions.append((PlayerAction(neck_turn_to_point= Neck_TurnToPoint(goal_c))))
        else:
            actions += go_to_placed_ball
        return actions

    def doKickerReady(agent: IAgent):
        wm = agent.wm
        state = wm.penalty_kick_state
        PenaltyKickState
        if wm.myself.stamina < agent.serverParams.stamina_max - 10.0 and (wm.cycle - state.cycle > agent.serverParams.pen_ready_wait - 3):
            return BhvPenaltyKick.doKickerSetup(agent)

        if not wm.myself.is_kickable:
            return BhvPenaltyKick.doKickerSetup(agent)

        return BhvPenaltyKick.doKicker(agent)

    def doKicker(agent: IAgent):
        wm = agent.wm
        actions = []
        if not wm.myself.is_kickable:
            actions.append(PlayerAction(body_intercept=Body_Intercept()))
            actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(wm.ball.position, 0.4, agent.serverParams.max_dash_power)))
            if wm.ball.pos_count > 0 :
                actions.append(PlayerAction(neck_turn_to_ball=Neck_TurnToBall()))
            '''else :
                
                opp_goalie = Player(Tools().OpponentGoalie(agent))
                if opp_goalie :
                    agent.add_action(PlayerAction(neck_turn_to_point=Neck_TurnToPoint(opp_goalie.position)))
                    agent.add_log_text(LoggerLevel.TEAM, "neck to goalie")
                else :
                    agent.add_action(PlayerAction(neck_scan_field=Neck_ScanField()))
                    agent.add_log_text(LoggerLevel.TEAM, "neck scan field")
            return True'''


        actions += BhvPenaltyKick.doShoot(agent)

        actions += BhvPenaltyKick.doDribble(agent)
        
        return actions

    def doOneKickShoot(agent: IAgent):
        wm = agent.wm
        actions = []
        ball_speed = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y).r()
        
        if not agent.serverParams.pen_allow_mult_kicks and ball_speed > 0.3 : 
             return []
        
        # go to the ball side 
        if not wm.myself.is_kickable :
            actions.append((PlayerAction(body_go_to_point=Body_GoToPoint(wm.ball.position,0.4,agent.serverParams.max_dash_power))))
        
        # turn to the ball to get the maximal kick rate
        if abs(wm.ball.angle_from_self - wm.myself.body_direction) > 0.3:
            
            opp_goalie = Tools.OpponentGoalie(agent)
            if opp_goalie :
                actions.append((PlayerAction(neck_turn_to_point=Neck_TurnToPoint(opp_goalie.position))))
            else :
                goal_c = Vector2D(agent.serverParams.pitch_half_length, 0.0)
                actions.append((PlayerAction(neck_turn_to_point=Neck_TurnToPoint(RpcVector2D(goal_c.x(), goal_c.y())))))
                return actions
        
        opp_goalie = Tools.OpponentGoalie(agent)

        shoot_point = Vector2D(agent.serverParams.pitch_half_length, 0.0)
        if opp_goalie :
            shoot_point.set_y((agent.serverParams.goal_width / 2.0 )-1.0)
            if abs(opp_goalie.position.y) > 0.5 : 
                if opp_goalie.position.y > 0.0 :
                    shoot_point.set_y(shoot_point.y() * -1.0)
            elif opp_goalie.body_direction_count < 2.0 :
                if opp_goalie.body_direction > 0.0 :
                    shoot_point.set_y(shoot_point.y() * -1.0) 
        
        actions.append((PlayerAction(body_kick_one_step=Body_KickOneStep(RpcVector2D(shoot_point.x(), shoot_point.y()),agent.serverParams.ball_speed_max))))


        return actions

    def doShoot(agent: IAgent):
        wm = agent.wm
        actions = []
        time = wm.cycle
        state = wm.penalty_kick_state
        elapsed_time = time - state.cycle
        time_thr = agent.serverParams.pen_taken_wait - 25.0
        if ( wm.cycle - state.cycle ) > agent.serverParams.pen_taken_wait - 25.0 : 
            return BhvPenaltyKick.doOneKickShoot(agent)
        
        shot_point = Vector2D(0,0)
        shot_speed = 0.0

        if BhvPenaltyKick.getShootPos(agent,shot_point,shot_speed) :
            actions.append((PlayerAction(body_smart_kick=Body_SmartKick(RpcVector2D(shot_point.x(), shot_point.y()),shot_speed,shot_speed*0.96,2))))
        
        return actions

    def doDribble(agent: IAgent):
        actions = []
        CONTINUAL_COUNT = 20
        S_target_continual_count = CONTINUAL_COUNT

        SP = agent.serverParams
        wm = agent.wm
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_velocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)
        goal_c = Vector2D(SP.pitch_half_length, 0.0)

        penalty_abs_x = SP.their_penalty_area_line_x

        
        opp_goalie = Tools.OpponentGoalie(agent)
        
        goalie_max_speed = 1.0

        my_abs_x = abs(wm.myself.position.x)
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        self_velocity = Vector2D(wm.myself.velocity.x, wm.myself.velocity.y)
        opp_goalie_position = Vector2D(opp_goalie.position.x, opp_goalie.position.y)
        goalie_dist = (opp_goalie_position.dist(self_position) 
                       - goalie_max_speed * min(5, opp_goalie.pos_count) 
                       if opp_goalie else 200.0)
        goalie_abs_x = (abs(opp_goalie.position.x) if opp_goalie else 200.0)

        base_target_abs_y = (SP.goal_width / 0.2 )+ 4.0
        drib_target = goal_c
        drib_dashes = 6

        if my_abs_x < penalty_abs_x - 3.0 and goalie_dist > 10.0:
            pass
        else:
            if goalie_abs_x > my_abs_x:
                if goalie_dist < 4.0:
                    if S_target_continual_count == 1:
                        S_target_continual_count = -CONTINUAL_COUNT
                    elif S_target_continual_count == -1:
                        S_target_continual_count = +CONTINUAL_COUNT
                    elif S_target_continual_count > 0:
                        S_target_continual_count -= 1
                    else:
                        S_target_continual_count += 1

                if S_target_continual_count > 0:
                    if wm.myself.position.y < -base_target_abs_y + 2.0:
                        drib_target.set_y(base_target_abs_y)
                    else:
                        drib_target.set_y(-base_target_abs_y)

                else:
                    if wm.myself.position.y > base_target_abs_y - 2.0:
                        drib_target.set_y(-base_target_abs_y)

                    else:
                        drib_target.set_y(base_target_abs_y)

                drib_target.set_x(goalie_abs_x + 1.0)
                drib_target.set_x(min(max(penalty_abs_x - 2.0, drib_target.x()), 
                                    SP.pitch_half_length - 4.0))

                dashes = (self_position.dist(drib_target) * 0.8 
                      / SP.player_speed_max)
                drib_dashes = int(dashes // 1)
                drib_dashes = min(max(1, drib_dashes), 6)

        if opp_goalie and goalie_dist < 5.0:
            drib_angle = Vector2D(drib_target - self_position).th()
            goalie_angle = Vector2D(opp_goalie_position - self_position).th()
            drib_dashes = 6
            if abs(drib_angle - goalie_angle) < 80.0:
                drib_target = wm.myself.position
                drib_target += Vector2D.polar2vector(10.0, goalie_angle + (self_position.y > 0 and -1.0 or +1.0) * 55.0)

        target_rel = Vector2D(drib_target - self_position)
        buf = 2.0
        if abs(drib_target.x()) < penalty_abs_x:
            buf += 2.0

        if abs(target_rel.x()) < 5.0 and (not opp_goalie 
                                        or opp_goalie_position.dist(drib_target) > target_rel.r() - buf):
            if abs(target_rel.th() - wm.myself.body_direction) < 5.0:
                first_speed = BhvPenaltyKick.calc_first_term_geom_series_last(0.5, 
                                                           target_rel.r(), 
                                                           SP.ball_decay)
                first_speed = min(first_speed, SP.ball_speed_max)
                actions.append( PlayerAction(body_smart_kick=Body_SmartKick(RpcVector2D(drib_target.x(), drib_target.y()), first_speed, first_speed * 0.96, 3)))
            
            elif Vector2D(ball_position + ball_velocity - self_velocity).r() < agent.serverParams.kickable_area - 0.2:
                actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(drib_target.x(), drib_target.y()))))
            else:
                actions.append(PlayerAction(body_stop_ball=Body_StopBall()))
        else:
            actions.append(Dribble.Decision(agent))

        if opp_goalie:
            actions.append(PlayerAction(neck_turn_to_point=Neck_TurnToPoint(opp_goalie.position)))
        else:
            actions.append(PlayerAction(neck_scan_field=Neck_ScanField()))

        return actions            

    def doGoalieWait(agent: IAgent):
        actions = []
        actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
        actions.append(PlayerAction(neck_turn_to_ball=Neck_TurnToBall()))

        return actions

    def doGoalieSetup(agent: IAgent):
        
        wm = agent.wm
        move_point = Vector2D(-agent.serverParams.pitch_half_length + agent.serverParams.pen_max_goalie_dist_x - 0.1,0.0)
        actions = []
        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(move_point,0.5,agent.serverParams.max_dash_power)))

        if abs(wm.myself.body_direction) > 2.0 : 
            
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(0, 0))))
        
        #actions.append(PlayerAction(neck_turn_to_ball=Neck_TurnToBall()))

        return actions
    
    def doGoalie(agent: IAgent):
        SP = agent.serverParams
        wm = agent.wm
        actions = []
        # check if catchable
        our_penalty = Rect2D(Vector2D(-SP.pitch_half_length, -SP.penalty_area_half_width + 1.0),
                             Size2D(SP.penalty_area_length - 1.0, (SP.penalty_area_half_width*2.0) - 2.0))
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_velocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)
        if wm.ball.dist_from_self < SP.catchable_area - 0.05 and our_penalty.contains(ball_position):
            return [PlayerAction(catch_action = Catch())]

        if agent.wm.myself.is_kickable:
            actions += ClearBall.Decision(agent)
            actions.append(PlayerAction(body_turn_to_ball=Body_TurnToBall()))
            return actions

        # if taker can only one kick, goalie should stay the front of goal.
        if not SP.pen_allow_mult_kicks:
            # kick has not been taken.
            if ball_velocity.r2() < 0.01 and abs(wm.ball.position.x) < SP.pitch_half_length - SP.pen_dist_x - 1.0:
                return BhvPenaltyKick.doGoalieSetup(agent)

            if ball_velocity.r2() > 0.01:
                return BhvPenaltyKick.doGoalieSlideChase(agent)

        return BhvPenaltyKick.doGoalieBasicMove(agent)

    def doGoalieBasicMove(agent: IAgent):
        SP = agent.serverParams
        wm = agent.wm
        actions = []
        our_penalty = Rect2D(Vector2D(-SP.pitch_half_length, -SP.penalty_area_half_width + 1.0),
                             Size2D(SP.penalty_area_length - 1.0, (SP.penalty_area_half_width*2.0) - 2.0))


        # get active interception catch point
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_velocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)
        self_min = wm.intercept_table.self_reach_steps
        move_pos = Tools.inertia_point(ball_position, ball_velocity, self_min, agent.serverParams.ball_decay)

        if our_penalty.contains(move_pos):
            # ExistIntPoint
            if wm.intercept_table.first_opponent_reach_steps < wm.intercept_table.self_reach_steps or wm.intercept_table.self_reach_steps <= 4:
                actions.append(PlayerAction(body_intercept=Body_Intercept(False)))
                return actions

        my_pos = Vector2D(wm.myself.position.x, wm.myself.position.y)
        ball_pos: Vector2D
        if wm.intercept_table.first_opponent_reach_steps < wm.intercept_table.self_reach_steps:
            opp = Tools.OpponentsFromBall(agent)
            opp_pos = opp[0]
            ball_pos = Vector2D(opp_pos.x, opp_pos.y)
            ball_pos += Vector2D(opp.velocity.x, opp.velocity.y)
        else:
            ball_pos = inertia_n_step_point(ball_pos, ball_velocity, 3, SP.ball_decay)

        move_pos = BhvPenaltyKick.getGoalieMovePos(agent, ball_pos, my_pos)


        actions.append(PlayerAction(body_go_to_point=Body_GoToPoint(RpcVector2D(move_pos.x(), move_pos.y()), 0.5, SP.max_dash_power)))

        # already there
        face_angle = wm.ball.angle_from_self
        if wm.ball.angle_from_self > wm.myself.body_direction:
            face_angle += 90.0
        else:
            face_angle -= 90.0

        actions.append(PlayerAction(body_turn_to_angle=Body_TurnToAngle(face_angle)))

        return actions

    def getGoalieMovePos(agent : IAgent, ball_pos: Vector2D, my_pos: Vector2D):
        SP = agent.serverParams
        min_x = -SP.pitch_half_length + SP.catch_area_l * 0.9

        if ball_pos.x < -49.0:
            if abs(ball_pos.y) < (SP.goal_width / 2.0 ):
                return Vector2D(min_x, ball_pos.y())
            else:
                return Vector2D(min_x, math.copysign((SP.goal_width / 2.0), ball_pos.y()))

        goal_l = Vector2D(-SP.pitch_half_length, -(SP.goal_width / 2.0))
        goal_r = Vector2D(-SP.pitch_half_length, (SP.goal_width / 2.0))

        ball2post_angle_l = Vector2D(goal_l - ball_pos).th()
        ball2post_angle_r = Vector2D(goal_r - ball_pos).th()

        # NOTE: post_angle_r < post_angle_l
        line_dir = AngleDeg.bisect(ball2post_angle_r, ball2post_angle_l)

        line_mid = Line2D(ball_pos, line_dir)
        goal_line = Line2D(goal_l, goal_r)

        intersection = Vector2D(goal_line.intersection(line_mid))
        if intersection.is_valid():
            line_l = Line2D(ball_pos, goal_l)
            line_r = Line2D(ball_pos, goal_r)

            alpha = math.degrees(math.atan2((SP.goal_width / 2.0), SP.penalty_area_length - 2.5))
            dist_from_goal = ((line_l.dist(intersection) + line_r.dist(intersection)) * 0.5) / math.sin(math.radians(alpha))

            if dist_from_goal <= (SP.goal_width / 2.0):
                dist_from_goal = (SP.goal_width / 2.0)

            if (ball_pos - intersection).r() + 1.5 < dist_from_goal:
                dist_from_goal = (ball_pos - intersection).r() + 1.5

            position_error = line_dir - Vector2D(intersection - my_pos).th()

            danger_angle = 21.0

            if position_error.abs() > danger_angle:
                dist_from_goal *= ((1.0 - ((position_error.abs() - danger_angle) / (180.0 - danger_angle))) * 0.5)

            result = intersection
            add_vec = ball_pos - intersection
            add_vec.set_length(dist_from_goal)

            result += add_vec
            if result.set_x < min_x:
                result.set_x(min_x)
            return result
        else:
            if ball_pos.x() > 0.0:
                return Vector2D(min_x, goal_l.y())
            elif ball_pos.x() < 0.0:
                return Vector2D(min_x, goal_r.y())
            else:
                return Vector2D(min_x, 0.0)

    def doGoalieSlideChase(agent:IAgent):
        wm = agent.wm
        actions = []
        if math.fabs(90.0 - abs(wm.myself.body_direction)) > 2.0:
            face_point = Vector2D(wm.myself.position.x, 100.0)
            if wm.myself.body_direction < 0.0:
                face_point.set_y(-100.0)
            
            actions.append(PlayerAction(body_turn_to_point=Body_TurnToPoint(RpcVector2D(face_point.x(), face_point.y()))))
            #actions.append(PlayerAction(neck_turn_to_ball=Neck_TurnToBall()))
            return actions
        self_position = Vector2D(wm.myself.position.x, wm.myself.position.y)
        
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        ball_veclocity = Vector2D(wm.ball.velocity.x, wm.ball.velocity.y)
        ball_ray = Ray2D(ball_position, ball_veclocity.th())
        ball_line = Line2D(ball_ray.origin(), ball_ray.dir())
        my_line = Line2D(self_position, wm.myself.body_direction)

        intersection = Vector2D(my_line.intersection(ball_line))
        if not intersection.is_valid() or not ball_ray.dir() < (intersection):
            actions.append(PlayerAction(body_intercept=Body_Intercept()))
            # goalie mode
            actions.append(PlayerAction(neck_turn_to_ball=Neck_TurnToBall()))
            return actions

        if wm.myself.position.dist(intersection) < agent.serverParams.catch_area_l * 0.7:
            actions.append(PlayerAction(body_stop_dash=Body_StopDash()))
            # not save recovery
            actions.append(PlayerAction(neck_turn_to_ball=Neck_TurnToBall()))
            return actions

        angle = Vector2D(intersection - self_position).th()
        dash_power = agent.serverParams.max_dash_power

        if abs(angle.degree() - wm.myself.body_direction) > 90.0:
            dash_power = agent.serverParams.min_dash_power
        actions.append(PlayerAction(dash=Dash(dash_power)))
        actions.append(PlayerAction(neck_turn_to_ball=Neck_TurnToBall()))
        return actions

    def getShootPos(agent: IAgent, point, first_speed):
        # using listing method to pass the reference
        wm = agent.wm
        SP = agent.serverParams
        ball_position = Vector2D(wm.ball.position.x, wm.ball.position.y)
        if Vector2D(SP.pitch_half_length,0.0).dist2(ball_position) > 35.0 ** 2:
            # too far
            return False
        
        opp_goalie = Tools.OpponentGoalie(agent)
        
        if not opp_goalie:
            shot_c = Vector2D(SP.pitch_half_length,0.0)
            if point is not None:
                point[0] = shot_c 
            if first_speed is not None:
                first_speed[0] = SP.ball_speed_max 

            # no goalie
            return True

        best_l_or_r = 0
        best_speed = SP.ball_speed_max + 1.0

        post_buf = 1.0 + min(2.0, (SP.pitch_half_length - abs(wm.myself.position.x)) * 0.1)

        shot_l = Vector2D(SP.pitch_half_length, (-SP.goal_width / 2.0) + post_buf)
        shot_r = Vector2D(SP.pitch_half_length, (+SP.goal_width /0.2) - post_buf)

        angle_l = (shot_l - ball_position).th()
        angle_r = (shot_r - ball_position).th()

        goalie_max_speed = 1.0
        goalie_dist_buf = goalie_max_speed * min(5, opp_goalie.pos_count) + SP.catch_area_l + 0.2
        opp_goalie_position = Vector2D(opp_goalie.position.x, opp_goalie.position.y)
        opp_goalie_velocity = Vector2D(opp_goalie.velocity.x, opp_goalie.velocity.y)
        goalie_next_pos = Vector2D(opp_goalie_position + opp_goalie_velocity)

        for i in range(2):
            target = shot_l if i == 0 else shot_r
            angle = angle_l if i == 0 else angle_r

            dist2goal = ball_position(target)

            tmp_first_speed = (dist2goal + 5.0) * (1.0 - SP.ball_decay)
            tmp_first_speed = max(1.2, tmp_first_speed)

            over_max = False
            while not over_max:
                if tmp_first_speed > SP.ball_speed_max:
                    over_max = True
                    tmp_first_speed = SP.ball_speed_max

                ball_pos = Vector2D(wm.ball.position)
                ball_vel = Vector2D.polar2vector(tmp_first_speed, angle)
                ball_pos += ball_vel
                ball_vel *= SP.ball_decay

                goalie_can_reach = False

                cycle = 0
                while abs(ball_pos.x) < SP.pitch_half_length:
                    if goalie_next_pos.dist(ball_pos) < goalie_max_speed * cycle + goalie_dist_buf:
                        goalie_can_reach = True
                        break

                    ball_pos += ball_vel
                    ball_vel *= SP.ball_decay
                    cycle += 1

                    if not goalie_can_reach:
                        if tmp_first_speed < best_speed:
                            best_l_or_r = i
                            best_speed = tmp_first_speed
                        break
                    tmp_first_speed += 0.4

        if best_speed <= SP.ball_speed_max:
            if point is not None:
                point[0] = shot_l if best_l_or_r == 0 else shot_r
            if first_speed is not None:
                first_speed[0] = best_speed

            return True

        return False


    def calc_first_term_geom_series_last(last_term, sum, r):
        if abs(last_term) < 0.001:
            return sum * (1.0 - r)

        inverse = 1.0 / r
        tmp = 1.0 + sum * (inverse - 1.0) / last_term
        if tmp < 0.001:
            return last_term

        return last_term * math.pow(inverse, math.log(tmp) / math.log(inverse))