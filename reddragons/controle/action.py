from numpy import pi, cos, sin, tan, arctan2, sqrt, deg2rad

from .execution import univec_controller


# % Basic Actions
def stop(robot):
    robot.sim_set_vel(0, 0)


def sweep_ball(robot, left_side=True):
    if left_side:
        w = -0.5 * robot.vMax * robot.R / robot.L
    else:
        w = 0.5 * robot.vMax * robot.R / robot.L

    if robot.yPos > 65:
        robot.sim_set_vel(0, w)
    else:
        robot.sim_set_vel(0, -w)


def position_to_sweep(robot, ball, left_side=True, friend1=None, friend2=None):
    if left_side:
        robot.target.update(ball.xPos, ball.yPos, 0)
    else:
        robot.target.update(ball.xPos, ball.yPos, pi)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False)
    else:  # ? Both friends to avoid
        robot.obst.update(robot, friend1, friend2)
        v, w = univec_controller(robot, robot.target, True, robot.obst)

    robot.sim_set_vel(v, w)


def avoid_bound(robot, friend1=None, friend2=None):
    # % Verify if the dot product between the robot and the point (135,65) is positive
    # % It means the angle resides in ]-pi/2,pi/2[
    dot_prod = (cos(robot.theta)) * (135 - robot.xPos) + (sin(robot.theta)) * (65 - robot.yPos)

    if dot_prod >= 0:
        arrival_theta = arctan2(65 - robot.yPos, 135 - robot.xPos)
        robot.target.update(135, 65, arrival_theta)
    else:
        arrival_theta = arctan2(65 - robot.yPos, 15 - robot.xPos)
        robot.target.update(15, 65, arrival_theta)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False)
    else:  # ? Both friends to avoid
        robot.obst.update(robot, friend1, friend2)
        v, w = univec_controller(robot, robot.target, True, robot.obst)

    robot.sim_set_vel(v, w)


def hold_position(robot, xg, yg, des_theta, friend1=None, friend2=None):
    robot.target.update(xg, yg, des_theta)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, stop_when_arrive=True)
    else:  # ? Both friends to avoid
        robot.obst.update(robot, friend1, friend2)
        v, w = univec_controller(robot, robot.target, True, robot.obst, stop_when_arrive=True)

    robot.sim_set_vel(v, w)


# % Attacker Actions
def shoot(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    if left_side:
        arrival_theta = arctan2(65 - ball.yPos, 160 - ball.xPos)  # ? Angle between the ball and point (150,65)
    else:
        arrival_theta = arctan2(65 - ball.yPos, 10 - ball.xPos)  # ? Angle between the ball and point (0,65)
    # robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # ? Both friends to avoid
        # robot.obst.update(robot,friend1,friend2,enemy1,enemy2,enemy3)
        robot.obst.update2(robot, ball, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    robot.sim_set_vel(v, w)


def shoot2(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    if left_side:
        if (ball.yPos > 45) and (ball.yPos < 85):
            arrival_theta = 0
        elif ball.yPos <= 45:
            y = 45 + (45 - ball.yPos) / (45 - 0) * 20
            arrival_theta = arctan2(y - 45, 160 - ball.xPos)
        else:
            y = 85 - (ball.yPos - 85) / (130 - 85) * 20
            arrival_theta = arctan2(y - 85, 160 - ball.xPos)
    else:
        if (ball.yPos > 45) and (ball.yPos < 85):
            arrival_theta = pi
        elif ball.yPos <= 45:
            y = 45 + (45 - ball.yPos) / (45 - 0) * 20
            arrival_theta = arctan2(y - 45, 10 - ball.xPos)
        else:
            y = 85 - (ball.yPos - 85) / (130 - 85) * 20
            arrival_theta = arctan2(y - 85, 10 - ball.xPos)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)
    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # ? Both friends to avoid
        robot.obst.update2(robot, ball, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    robot.sim_set_vel(v, w)


# % Defender Actions
def defender_spin(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    if left_side:
        arrival_theta = arctan2(65 - ball.yPos, 160 - ball.xPos)  # ? Angle between the ball and point (150,65)
    else:
        arrival_theta = arctan2(65 - ball.yPos, 10 - ball.xPos)  # ? Angle between the ball and point (0,65)
    # robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # ? Both friends to avoid
        # robot.obst.update(robot,friend1,friend2,enemy1,enemy2,enemy3)
        robot.obst.update2(robot, ball, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    d = robot.dist(ball)
    if robot.spin and d < 10:
        if not robot.teamYellow:
            if robot.yPos > 65:
                v = 0
                w = -30
            else:
                v = 0
                w = 30
        else:
            if robot.yPos > 65:
                v = 0
                w = 30
            else:
                v = 0
                w = -30

    robot.sim_set_vel(v, w)


def push_ball(robot, ball, friend1=None, friend2=None):
    d_sup = sqrt((75 - ball.xPos) ** 2 + (130 - ball.yPos) ** 2)  # ? Distance between the ball and point (75,130)
    d_inf = sqrt((75 - ball.xPos) ** 2 + (0 - ball.yPos) ** 2)  # ? Distance between the ball and point (75,0)

    if d_sup <= d_inf:
        arrival_theta = arctan2(130 - ball.yPos, 75 - ball.xPos)  # ? Angle between the ball and point (75,130)
    else:
        arrival_theta = arctan2(-ball.yPos, 75 - ball.xPos)  # ? Angle between the ball and point (75,0)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False)
    else:  # ? Both friends to avoid
        robot.obst.update(robot, friend1, friend2)
        v, w = univec_controller(robot, robot.target, True, robot.obst)

    robot.sim_set_vel(v, w)


# TODO #2 Need more speed to reach the ball faster than our enemy
def screen_out_ball(robot, ball, static_point, left_side=True, upper_lim=200, lower_lim=0, friend1=None, friend2=None):
    # Check if ball is inside the limits
    if ball.yPos >= upper_lim:
        y_point = upper_lim

    elif ball.yPos <= lower_lim:
        y_point = lower_lim

    else:
        y_point = ball.yPos
    # Check the field side
    if left_side:
        if robot.yPos <= ball.yPos:
            arrival_theta = pi / 2
        else:
            arrival_theta = -pi / 2
        robot.target.update(static_point, y_point, arrival_theta)
    else:
        if robot.yPos <= ball.yPos:
            arrival_theta = pi / 2
        else:
            arrival_theta = -pi / 2
        robot.target.update(170 - static_point, y_point, arrival_theta)

    if robot.contStopped > 60:
        if robot.teamYellow:
            if abs(robot.theta) < 10:
                v = -30
                w = 5
            else:
                v = 30
                w = -5
        else:
            if abs(robot.theta) < 10:
                v = -30
                w = 0
            else:
                v = 30
                w = 0
    else:
        if friend1 is None and friend2 is None:  # ? No friends to avoid
            v, w = univec_controller(robot, robot.target, avoid_obst=False, stop_when_arrive=True)
        else:  # ? Both friends to avoid
            robot.obst.update(robot, friend1, friend2)
            v, w = univec_controller(robot, robot.target, True, robot.obst, stop_when_arrive=True)

    robot.sim_set_vel(v, w)


# % Goalkeeper Actions
def goal_keeper_defender(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None,
                         enemy3=None):
    if left_side:
        arrival_theta = arctan2(ball.yPos - 65, ball.xPos - 10)  # ? Angle between the ball and point (150,65)
    else:
        arrival_theta = arctan2(ball.yPos - 65, ball.xPos - 160)  # ? Angle between the ball and point (0,65)
    # robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # ? Both friends to avoid
        robot.obst.update(robot, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    if robot.dist(ball) < 10:
        if not robot.teamYellow:
            if robot.yPos > 65:
                v = 0
                w = -30
            else:
                v = 0
                w = 30
        else:
            if robot.yPos > 65:
                v = 0
                w = 30
            else:
                v = 0
                w = -30

    robot.sim_set_vel(v, w)


# TODO #1 More effective way to predict the ball position
def blobk_ball(robot, ball, left_side=True):
    ball_vec = (ball.pastPose[:, 1] - ball.pastPose[:, 0]).reshape(2, 1)
    # ? Building a vector between current and past position of the ball
    if left_side:
        alpha = (9 - ball.xPos) / (ball_vec[0] + 0.000000001)
        des_y = ball.yPos + alpha * ball_vec[1]
        if 82 >= des_y >= 48:
            # ? If the projection of the ball is inside of our goal, we manage the goalkeeper to the
            if robot.yPos <= des_y:  # ? point (9,y_projected)
                arrival_theta = pi / 2
            else:
                arrival_theta = -pi / 2
            robot.target.update(9, float(des_y), arrival_theta)
        else:  # ? Else we manage the goalkeeper to the center of the goal, at point (9,65)
            if robot.yPos <= 65:
                arrival_theta = pi / 2
            else:
                arrival_theta = -pi / 2
            robot.target.update(9, 65, arrival_theta)
        v, w = univec_controller(robot, robot.target, None, False, stop_when_arrive=True)
        robot.sim_set_vel(v, w)
    else:
        alpha = (141 - ball.xPos) / (ball_vec[0] + 0.000000001)
        des_y = ball.yPos + alpha * ball_vec[1]
        if 82 >= des_y >= 48:  # ? If the projection of the ball is inside of our goal, we manage the goalkeeper to the
            if robot.yPos <= des_y:  # ? point (141,y_projected)
                arrival_theta = pi / 2
            else:
                arrival_theta = -pi / 2
            robot.target.update(141, float(des_y), arrival_theta)
        else:  # ? Else we manage the goalkeeper to the center of the goal, at point (141,65)
            if robot.yPos <= 65:
                arrival_theta = pi / 2
            else:
                arrival_theta = -pi / 2
            robot.target.update(141, 65, arrival_theta)
        v, w = univec_controller(robot, robot.target, None, False, stop_when_arrive=True)
        robot.sim_set_vel(v, w)


def protect_goal(robot, ball, r, left_side=True, friend1=None, friend2=None):
    if left_side:
        theta = arctan2((ball.yPos - 65), (ball.xPos - 15))

        if pi / 2 >= theta >= (-pi / 2):

            proj_x = r * cos(theta) + 15
            proj_y = r * sin(theta) + 65

        else:

            proj_x = -r * cos(theta) + 15
            proj_y = r * sin(theta) + 65

        if robot.yPos > 100:
            if robot.xPos < ball.xPos:
                arrival_theta = -(pi / 2 - theta)

            if robot.xPos >= ball.xPos:
                arrival_theta = (pi / 2 + theta)

        if 100 >= robot.yPos > 65:
            if robot.yPos < ball.yPos:
                arrival_theta = (pi / 2 + theta)
            if robot.yPos >= ball.yPos:
                arrival_theta = -(pi / 2 - theta)

        if 65 >= robot.yPos > 30:
            if robot.yPos < ball.yPos:
                arrival_theta = pi / 2 + theta
            if robot.yPos >= ball.yPos:
                arrival_theta = -(pi / 2 - theta)

        if robot.yPos <= 30:
            if robot.xPos < ball.xPos:
                arrival_theta = pi / 2 + theta

            if robot.xPos >= ball.xPos:
                arrival_theta = -(pi / 2 - theta)

    arrival_theta = arctan2(sin(arrival_theta), cos(arrival_theta))
    robot.target.update(proj_x, proj_y, arrival_theta)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, stop_when_arrive=True)
    else:  # ? Both friends to avoid
        robot.obst.update(robot, friend1, friend2)
        v, w = univec_controller(robot, robot.target, True, robot.obst, stop_when_arrive=True)

    robot.sim_set_vel(v, w)


# %Crossing functions
def direct_goal(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    if robot.flagDirectGoal:
        if robot.dist(ball) < 10:
            robot.target.update(150, 65, 0)
        else:
            robot.flagDirectGoal = False
    else:
        arrival_theta = arctan2(65 - ball.yPos, 150 - ball.xPos)
        robot.target.update(ball.xPos, ball.yPos, arrival_theta)
        if (robot.dist(ball) < 10 and (
                robot.theta < (arrival_theta + pi / 18) and (robot.theta > arrival_theta - pi / 18))):
            robot.flagDirectGoal = True

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False)
    else:  # ? Both friends to avoid
        robot.obst.update(robot, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst)
    robot.sim_set_vel(v, w)


def ball_crossing(robot_attacker, ball, array_side_crossing, left_side=True, robot_defender=None, robot_goalkeeper=None):
    if array_side_crossing[0] or (robot_attacker.flagCruzamento and robot_attacker.yPos < 65):  # For left-down side
        arrival_theta = arctan2(115 - ball.yPos, 75 - ball.xPos)
        robot_attacker.target.update(ball.xPos, ball.yPos, arrival_theta)
        robot_defender.target.update(85, 85, arrival_theta - pi)
        robot_attacker.flagCruzamento = True
    elif array_side_crossing[1] or (robot_attacker.flagCruzamento and robot_attacker.yPos > 65):  # For left-up side
        arrival_theta = -pi + arctan2(ball.yPos - 25, ball.xPos - 75)
        robot_attacker.target.update(ball.xPos, ball.yPos, arrival_theta)
        robot_defender.target.update(85, 45, arrival_theta + pi)
        robot_attacker.flagCruzamento = True

    if robot_goalkeeper is None:  # Setting velocity for robots
        va, wa = univec_controller(robot_attacker, robot_attacker.target, avoid_obst=False)
        vd, wd = univec_controller(robot_defender, robot_defender.target, avoid_obst=False)
    else:  # ? Both friends to avoid
        robot_attacker.obst.update(robot_attacker, robot_defender, robot_goalkeeper)
        va, wa = univec_controller(robot_attacker, robot_attacker.target, True, robot_attacker.obst)
        robot_attacker.obst.update(robot_defender, robot_attacker, robot_goalkeeper)
        if robot_defender.dist(robot_defender.target) < 5:  # Code for stop robot when he arrive in the target
            stop(robot_defender)
        else:
            vd, wd = univec_controller(robot_defender, robot_defender.target, True, robot_defender.obst)
            robot_defender.sim_set_vel(vd, wd)
    robot_attacker.sim_set_vel(va, wa)


def verify_crossing(robot_attacker, ball, left_side=True, robot_defender=None, robot_goalkeeper=None):
    x_t = (150 - 40 / tan(pi / 6))
    array_side_crossing = [False, False]  # [Left-Down, Left-Up]
    flag_crossing = False
    # Ball in corners - Triangular Area
    if (robot_attacker.xPos > (150 - x_t) and (
            robot_attacker.yPos < (robot_attacker.xPos - x_t) * tan(pi / 6))):  # For left-down side
        array_side_crossing[0] = True
        flag_crossing = True
    elif (robot_attacker.xPos > (150 - x_t) and (
            robot_attacker.yPos > 130 - (robot_attacker.xPos - x_t) * tan(pi / 6))):  # For left-up side
        array_side_crossing[1] = True
        flag_crossing = True
    elif robot_attacker.flagCruzamento:
        flag_crossing = True
    return array_side_crossing, flag_crossing


def position_change(array_functions, ball, array_side_crossing, left_side=True):
    if array_functions[2].flagCruzamento and (not array_side_crossing[0]) and (not array_side_crossing[1]):
        if (30 < ball.yPos < 100) and (92.5 < ball.xPos < 132.5):
            array_functions[1], array_functions[2] = array_functions[2], array_functions[1]  # Switching positions
            array_functions[2].flagCruzamento = False
        elif array_functions[2].dist(ball) > 30:
            array_functions[2].flagCruzamento = False
        elif (45 < ball.yPos < 85) and (132.5 < ball.xPos < 150):
            array_functions[2].flagCruzamento = False
        elif (ball.yPos > 105) and (75 < ball.xPos < 112.5):
            array_functions[2].flagCruzamento = False
        elif (ball.yPos < 25) and (75 < ball.xPos < 112.5):
            array_functions[2].flagCruzamento = False
    return array_functions


def girar(robot, v1, v2):
    robot.sim_set_vel2(v1, v2)


def defender_penalty(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    if left_side:
        arrival_theta = arctan2(ball.yPos - 65, ball.xPos - 10)  # ? Angle between the ball and point (150,65)
    else:
        arrival_theta = arctan2(ball.yPos - 65, ball.xPos - 160)  # ? Angle between the ball and point (0,65)
    # robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # ? Both friends to avoid
        robot.obst.update(robot, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    robot.sim_set_vel(v, w)


def attack_penalty(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    if left_side:
        if robot.yPos > 65:
            arrival_theta = -deg2rad(15)
        else:
            arrival_theta = deg2rad(15)
    else:
        if robot.yPos > 65:
            arrival_theta = -deg2rad(165)
        else:
            arrival_theta = deg2rad(165)

    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # ? No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # ? Both friends to avoid
        robot.obst.update(robot, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    robot.sim_set_vel(v, w)


def slave(robot_slave, robot_master, robot0=None, robot_enemy_0=None, robot_enemy_1=None, robot_enemy_2=None):
    if robot_master.yPos > 65:
        if robot_master.xPos > 75:
            proj_x = robot_master.xPos - 15
            proj_y = robot_master.yPos - 30
        else:
            proj_x = robot_master.xPos + 15
            proj_y = robot_master.yPos - 30  #
    else:
        if robot_master.xPos > 75:
            proj_x = robot_master.xPos - 15
            proj_y = robot_master.yPos + 30
        else:
            proj_x = robot_master.xPos + 15
            proj_y = robot_master.yPos + 30  #

    dist = sqrt((robot_slave.xPos - proj_x) ** 2 + (robot_slave.yPos - proj_y) ** 2)
    robot_slave.target.update(proj_x, proj_y, 0)

    if dist < 10:
        stop(robot_slave)
    else:
        # ? No friends to avoid
        if robot0 is None and robot_enemy_0 is None and robot_enemy_1 is None and robot_enemy_2 is None:
            v, w = univec_controller(robot_slave, robot_slave.target, avoid_obst=False, n=16, d=2)
        else:  # ? Both friends to avoid
            robot_slave.obst.update(robot_slave, robot0, robot_master, robot_enemy_0, robot_enemy_1, robot_enemy_2)
            v, w = univec_controller(robot_slave, robot_slave.target, True, robot_slave.obst, n=4, d=4)

        robot_slave.sim_set_vel(v, w)


def master_slave(robot0, robot1, robot2, ball, robot_enemy_0, robot_enemy_1, robot_enemy_2):
    dist1 = sqrt((robot1.xPos - ball.xPos) ** 2 + (robot1.yPos - ball.yPos) ** 2)
    ang1 = 0  # = arctan2(ball.yPos - robot1.yPos,ball.xPos - robot1.xPos)

    dist2 = sqrt((robot2.xPos - ball.xPos) ** 2 + (robot2.yPos - ball.yPos) ** 2)
    ang2 = 0  # = arctan2(ball.yPos - robot2.yPos,ball.xPos - robot2.xPos )

    # w1 = 0.20*(1-cos(ang1 - robot1.theta)) + 0.80*dist1/(dist1+dist2)
    # w2 = 0.20*(1-cos(ang2 - robot2.theta)) + 0.80*dist2/(dist1+dist2)

    if dist1 > dist2:
        # linhas 352 e 353 condicionais para não entrar no gol, o mesmo para 365 e 366
        if not robot1.teamYellow:
            if ball.xPos < 30 and (110 > ball.yPos > 30):
                if robot1.xPos < 30:
                    screen_out_ball(robot2, robot2, 55, left_side=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screen_out_ball(robot2, ball, 55, left_side=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                slave(robot1, robot2, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

            else:
                defender_spin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                if robot1.dist(ball) < 20:
                    if robot2.xPos > 140 and (100 > robot2.yPos > 40):
                        slave(robot1, robot2, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
                    else:
                        defender_spin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot2,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                else:
                    slave(robot1, robot2, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
        else:
            if ball.xPos > 130 and (110 > ball.yPos > 30):
                if robot1.xPos > 130:
                    screen_out_ball(robot2, robot2, 55, left_side=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screen_out_ball(robot2, ball, 55, left_side=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                slave(robot1, robot2, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

            else:
                defender_spin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                if robot1.dist(ball) < 20:
                    if robot2.xPos < 35 and (100 > robot2.yPos > 40):
                        slave(robot1, robot2, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
                    else:
                        defender_spin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot2,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                else:
                    slave(robot1, robot2, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

    else:
        if not robot1.teamYellow:
            if ball.xPos < 35 and (110 > ball.yPos > 30):
                if robot1.xPos < 35:
                    screen_out_ball(robot1, robot1, 55, left_side=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screen_out_ball(robot1, ball, 55, left_side=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                slave(robot2, robot1, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

            else:
                defender_spin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                if robot2.dist(ball) < 20:
                    if robot1.xPos > 140 and (100 > robot1.yPos > 40):
                        slave(robot2, robot1, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
                    else:
                        defender_spin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot1,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                else:
                    slave(robot2, robot1, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
        else:
            if ball.xPos > 130 and (110 > ball.yPos > 30):
                if robot1.xPos > 130:
                    screen_out_ball(robot1, robot1, 55, left_side=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screen_out_ball(robot1, ball, 55, left_side=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                slave(robot2, robot1, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

            else:
                defender_spin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                if robot2.dist(ball) < 20:
                    if robot1.xPos < 35 and (100 > robot1.yPos > 40):
                        slave(robot2, robot1, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
                    else:
                        defender_spin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot1,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                else:
                    slave(robot2, robot1, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
