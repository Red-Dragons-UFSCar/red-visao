from numpy import arctan2, sqrt, pi, deg2rad


# Estas funções são utilizadas para alterar a execução das estratégias do jogador nos cantos
# Afim de impedir que ele fique travado

def target_in_corner(target, robot):
    corner = 0
    flag_corner = False
    if not robot.teamYellow:
        if target.xPos < 20:

            flag_corner = True
            corner = 1
            if target.xPos < 5:
                target.update(target.xPos + 3, target.yPos, target.theta)
            else:
                target.update(target.xPos + 1.5, target.yPos, target.theta)
        elif target.xPos > 150:

            flag_corner = True
            corner = 3
            if target.xPos > 155:
                target.update(target.xPos - 3, target.yPos, target.theta)
            else:
                target.update(target.xPos - 1.5, target.yPos, target.theta)
        if target.yPos < 10:

            flag_corner = True
            corner = 2
            if target.yPos < 5:
                target.update(target.xPos, target.yPos + 3, target.theta)
            else:
                target.update(target.xPos, target.yPos + 1.5, target.theta)
        elif target.yPos > 120:

            flag_corner = True
            corner = 4
            if target.yPos > 125:
                target.update(target.xPos, target.yPos - 3, target.theta)
            else:
                target.update(target.xPos, target.yPos - 1.5, target.theta)
    else:
        if target.xPos < 20:

            flag_corner = True
            corner = 1
            if target.xPos < 15:
                target.update(target.xPos + 3, target.yPos, target.theta)
            else:
                target.update(target.xPos + 1.5, target.yPos, target.theta)
        elif target.xPos > 150:

            flag_corner = True
            corner = 3
            if target.xPos > 155:
                target.update(target.xPos - 3, target.yPos, target.theta)
            else:
                target.update(target.xPos - 1.5, target.yPos, target.theta)
        if target.yPos < 10:

            flag_corner = True
            corner = 2
            if target.yPos < 5:
                target.update(target.xPos, target.yPos + 3, target.theta)
            else:
                target.update(target.xPos, target.yPos + 1.5, target.theta)
        elif target.yPos > 120:

            flag_corner = True
            corner = 4
            if target.yPos > 125:
                target.update(target.xPos, target.yPos - 3, target.theta)
            else:
                target.update(target.xPos, target.yPos - 1.5, target.theta)

    robot.spin = False
    if flag_corner:
        robot.spin = True
        change_target_theta(robot, target, corner)

    return flag_corner, corner


def change_target_theta(robot, target, corner):
    dist = sqrt((robot.xPos - target.xPos) ** 2 + (robot.yPos - target.yPos) ** 2)

    if not robot.teamYellow:
        if corner == 2 or corner == 4:
            if dist < 6:
                if robot.yPos < 75:
                    theta_gol = arctan2(75, 160 - robot.xPos)

                else:
                    theta_gol = arctan2(-75, 160 - robot.xPos)
                target.update(target.xPos, target.yPos, theta_gol)
            else:
                target.update(target.xPos, target.yPos, 0)

        elif robot.yPos > 110:
            if corner == 1:
                target.update(target.xPos, target.yPos, pi / 2)
            elif corner == 3:
                target.update(target.xPos, target.yPos, -pi / 2)
        elif robot.yPos < 40:
            if corner == 1:
                target.update(target.xPos, target.yPos, -pi / 2)
            elif corner == 3:
                target.update(target.xPos, target.yPos, pi / 2)
    else:
        if corner == 2 or corner == 4:
            if dist < 6:
                if robot.yPos < 75:
                    theta_gol = arctan2(75, 10 - robot.xPos)

                else:
                    theta_gol = arctan2(-75, 10 - robot.xPos)
                target.update(target.xPos, target.yPos, theta_gol)
            else:
                if target.yPos > 65:
                    target.update(target.xPos, target.yPos, -pi + deg2rad(10))
                else:
                    target.update(target.xPos, target.yPos, pi - deg2rad(10))

        elif robot.yPos > 110:
            if corner == 1:
                target.update(target.xPos, target.yPos, -pi / 2)
            elif corner == 3:
                target.update(target.xPos, target.yPos, pi / 2)
        elif robot.yPos < 40:
            if corner == 1:
                target.update(target.xPos, target.yPos, pi / 2)
            elif corner == 3:
                target.update(target.xPos, target.yPos, -pi / 2)

    return None


def robot_locked_corner(target, robot):
    corner = 0
    flag_locked = False
    if robot.xPos < 3 and (robot.yPos > 110 or robot.yPos < 40):
        if abs(robot.theta) < 0.35 or abs(robot.theta - pi) < 0.35:
            flag_locked = True
            corner = 1
    elif robot.xPos > 147 and (robot.yPos > 110 or robot.yPos < 40):
        if abs(robot.theta) < 0.35 or abs(robot.theta - pi) < 0.35:
            flag_locked = True
            corner = 3
    if robot.yPos < 5:
        if (abs(robot.theta) < ((pi / 2) + 0.35)) and (abs(robot.theta) > ((pi / 2) - 0.35)):
            flag_locked = True
            corner = 2
    elif robot.yPos > 125:
        if (abs(robot.theta) < ((pi / 2) + 0.35)) and (abs(robot.theta) < ((pi / 2) - 0.35)):
            flag_locked = True
            corner = 4

    if flag_locked:
        change_target_pos(robot, target, corner)

    return flag_locked, corner


def change_target_pos(robot, target, corner):
    if corner == 1:
        target.update(robot.xPos + 100, robot.yPos, 0)
    if corner == 2:
        target.update(robot.xPos, robot.yPos + 100, pi / 2)
    if corner == 3:
        target.update(robot.xPos - 100, robot.yPos, 0)
    if corner == 4:
        target.update(robot.xPos, robot.yPos - 100, -pi / 2)
    return None
