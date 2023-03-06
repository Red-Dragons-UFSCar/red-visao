from numpy import cos, sin, arctan2, sqrt, sign, pi, delete, append, array, deg2rad

from .behaviours import Univector
from .corners import target_in_corner


# % Function to approximate phi_v
def approx(robot, target, avoid_obst=True, obst=None, n=8, d=2, field_is_hiperbolic=True):
    navigate = Univector()  # ? Defines the navigation algorithm
    dl = 0.000001  # ? Constant to approximate phi_v

    x = robot.xPos  # ? Saving (x,y) coordinates to calculate phi_v
    y = robot.yPos
    robot.xPos = robot.xPos + dl * cos(robot.theta)  # ? Incrementing robot (x,y) position
    robot.yPos = robot.yPos + dl * sin(robot.theta)

    if avoid_obst:
        if field_is_hiperbolic:
            stp_theta = navigate.univec_field_h(robot, target, obst)  # ? Computing a step Theta to determine phi_v
        else:
            stp_theta = navigate.univec_field_n(robot, target, obst, n, d)  # ?Computing a step Theta to determine phi_v
    else:
        if field_is_hiperbolic:
            stp_theta = navigate.hip_vec_field(robot, target)  # ? Computing a step Theta to determine phi_v
        else:
            # ? Computing a step Theta to determine phi_v
            stp_theta = navigate.n_vec_field(robot, target, n, d, have_face=False)

    robot.xPos = x  # ? Returning original (x,y) coordinates
    robot.yPos = y

    return stp_theta


# % Function to control the robot with or without collision avoidance
def univec_controller(robot, target, avoid_obst=True, obst=None, n=8, d=2, stop_when_arrive=False, double_face=False,
                      field_is_hiperbolic=True):
    flagCorner, corner = target_in_corner(target, robot)
    # if flagCorner:
    # robotLockedCorner(target, robot)
    navigate = Univector()  # ? Defines the navigation algorithm
    dl = 0.000001  # ? Constant to approximate phi_v
    k_w = robot.kw #1.5  # ? Feedback constant (k_w=1 means no gain)
    k_p = 1  # ? Feedback constant (k_p=1 means no gain)

    # % Correção de ângulo caso o robô esteja jogando com a face de trás
    #if robot.face == -1:
        #robot.theta = arctan2(sin(robot.theta - pi), cos(robot.theta - pi))

    target.theta = target.theta*pi/180


    # % Navigation: Go-to-Goal + Avoid Obstacle Vector Field
    if avoid_obst:
        if field_is_hiperbolic:
            des_theta = navigate.univec_field_h(robot, target, obst)  # ? Desired angle w/ gtg and ao vector field
        else:
            des_theta = navigate.univec_field_n(robot, target, obst, n, d)  # ? Desired angle w/ gtg and ao vector field

    # % Navigation: Go-to-Goal Vector Field
    else:
        if field_is_hiperbolic:
            des_theta = navigate.hip_vec_field(robot, target)  # ? Desired angle w/ gtg
        else:
            des_theta = navigate.n_vec_field(robot, target, n, d, have_face=False)  # ? Desired angle w/ gtg


    #'''
    #des_theta = robot.target.theta

    stp_theta = approx(robot, target, avoid_obst, obst, n, d, field_is_hiperbolic)
    #stp_theta=des_theta
    phi_v = arctan2(sin(stp_theta - des_theta),
                    cos(stp_theta - des_theta)) / dl  # ? Trick to mantain phi_v between [-pi,pi]
    theta_e = which_face(robot, target, des_theta, double_face)
    v1 = (2 * robot.vMax - robot.LSimulador * k_w * sqrt(abs(theta_e))) / (2 + robot.LSimulador * abs(phi_v))
    v2 = (sqrt(k_w ** 2 + 4 * robot.rMax * abs(phi_v)) - k_w * sqrt(abs(theta_e))) / (2 * abs(phi_v) + dl)

    if stop_when_arrive:
        v3 = k_p * robot.dist(target)
    else:
        v3 = robot.vMax

    if stop_when_arrive and robot.arrive():
        v = 0
        w = 0
    else:
        v = min(abs(v1), abs(v2), abs(v3))
        w = v * phi_v + k_w * sign(theta_e) * sqrt(abs(theta_e))

    print("Velocidade: " + str(v))
    print("Angular: " + str(w))
    print("theta_e: ", theta_e)
    # % Some code to store the past position, orientation and velocity
    # robot.v=v
    robot.pastPose = delete(robot.pastPose, 0, 1)  # ? Deleting the first column
    robot.pastPose = append(robot.pastPose, array(
        [[round(robot.xPos)], [round(robot.yPos)], [round(float(robot.theta))], [round(float(v))]]), 1)
    '''

    ang_erro = which_face(robot, target, des_theta, double_face)
    #ang_erro = des_theta-robot.theta*pi/180
    ang_erro = arctan2(sin(ang_erro),cos(ang_erro))

    derivativo = 0

    if robot.lastError == None:
        derivativo = 0
    else:
        ang_derivativo = ang_erro-robot.lastError
        ang_derivativo = arctan2(sin(ang_derivativo),cos(ang_derivativo))
        derivativo = sin(ang_derivativo)/0.02
        print("derivativo = " + str(derivativo))

    print("ang erro: " + str(ang_erro*180/pi))
    #print("a = " + str(robot.theta))
    #v = 15
    #Kp = 1.5
    #Kd = 0.1
    #Ki = 0.005
    v = 25
    Kp = 4#2
    Kd = 0.5#0.2
    Ki = 0.005
    robot.somaErro += sin(ang_erro)
    #robot.somaErro = arctan2(sin(robot.somaErro),cos(robot.somaErro))
    w = Kp*sin(ang_erro) + Ki*robot.somaErro
    print(w)
    #if w > 5:
        #w = 5
    robot.lastError = ang_erro
    #'''

    return v, w


# TODO #3 Verificar a necessidade de flagTrocaFace - travar a troca de face nos obstaculos
def which_face(robot, target, des_theta, double_face):
    theta_e = arctan2(sin(des_theta - deg2rad(robot.theta)), cos(des_theta - deg2rad(robot.theta)))  # Calculo do erro com a face atual

    if (abs(theta_e) > pi / 2 + pi / 12) and (
            not robot.flagTrocaFace) and double_face:  # Se o ângulo for propício pra trocar a face
        print("Oi")
        #robot.face = robot.face * (-1)  # Inverte a face
        robot.theta = arctan2(sin(robot.theta + pi), cos(robot.theta + pi))  # Recalcula o angulo
        theta_e = arctan2(sin(des_theta - robot.theta), cos(des_theta - robot.theta))  # Recalcula o erro

    return theta_e

# def which_face(robot, target, des_theta, double_face):
#     des_theta = deg2rad(des_theta)
#     theta = deg2rad(robot.theta)
#     theta_e = arctan2(sin(des_theta - theta), cos(des_theta - theta))  # Calculo do erro com a face atual
#     #robot.face = robot.face * (-1)  # Inverte a face
#     #robot.theta = arctan2(sin(robot.theta + pi), cos(robot.theta + pi))  # Recalcula o angulo
#     #theta_e = arctan2(sin(des_theta - robot.theta), cos(des_theta - robot.theta))  # Recalcula o erro
#
#     return theta_e
