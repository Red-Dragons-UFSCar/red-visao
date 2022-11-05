from numpy import sqrt, array, amin, where, zeros, delete, append, int32, argmin


# from scipy.spatial import distance -> Descomentar quando atividade do Grid voltar

# ! Units: cm, rad, s

# % Class to set the targets of each robot in game
class Target:
    def __init__(self):
        self.xPos = 0  # ? Desired x position
        self.yPos = 0  # ? Desired y position
        self.theta = 0  # ? Orientation at the desired point (x,y)

    # % Setter
    def update(self, x, y, theta):
        self.xPos = x
        self.yPos = y
        self.theta = theta

    # % This method print a little log on console
    def show_info(self):
        print('xPos: {:.2f} | yPos: {:.2f} | theta: {:.2f}'.format(self.xPos, self.yPos, float(self.theta)))


# % Class to set the obstacle of each robot
class Obstacle:
    def __init__(self):
        self.xPos = 0  # ? Obstacle x position
        self.yPos = 0  # ? Obstacle y position
        self.v = 0  # ? Obstacle velocity (cm/s)
        self.theta = 0  # ? Obstacle orientation

    # % Setter
    def set_obst(self, x, y, v, theta):
        self.xPos = x
        self.yPos = y
        self.v = v
        self.theta = theta

    # % This method verify which is the closest obstacle and sets it as the current obstacle to avoid
    def update(self, robot, friend1, friend2, enemy1=None, enemy2=None, enemy3=None):
        if (enemy1 is None) and (enemy2 is None) and (enemy3 is None):
            d = array([[robot.dist(friend1)],
                       [robot.dist(friend2)]])
        elif (enemy2 is None) and (enemy3 is None):
            d = array([[robot.dist(friend1)],
                       [robot.dist(friend2)],
                       [robot.dist(enemy1)]])
        elif enemy3 is None:
            d = array([[robot.dist(friend1)],
                       [robot.dist(friend2)],
                       [robot.dist(enemy1)],
                       [robot.dist(enemy2)]])
        else:
            d = array([[robot.dist(friend1)],
                       [robot.dist(friend2)],
                       [robot.dist(enemy1)],
                       [robot.dist(enemy2)],
                       [robot.dist(enemy3)]])

        index = where(d == amin(d))
        if index[0][0] == 0:
            self.set_obst(friend1.xPos, friend1.yPos, friend1.v, friend1.theta)
        elif index[0][0] == 1:
            self.set_obst(friend2.xPos, friend2.yPos, friend2.v, friend2.theta)
        elif index[0][0] == 2:
            self.set_obst(enemy1.xPos, enemy1.yPos, 0, 0)
        elif index[0][0] == 3:
            self.set_obst(enemy2.xPos, enemy2.yPos, 0, 0)
        else:
            self.set_obst(enemy3.xPos, enemy3.yPos, 0, 0)

    def update2(self, robot, ball, friend1, friend2, enemy1, enemy2, enemy3):
        enemys = array([enemy1, enemy2, enemy3])
        d_ball = array([[enemy1.dist(ball)],
                        [enemy2.dist(ball)],
                        [enemy3.dist(ball)]])
        index = argmin(d_ball)
        if d_ball[index] < 15:
            enemys = delete(enemys, [index])

        if not robot.teamYellow:
            x_gol = 160
            y_gol = 65
        else:
            x_gol = 10
            y_gol = 65

        if len(enemys) == 3:
            d1 = sqrt((x_gol - enemy1.xPos) ** 2 + (y_gol - enemy1.yPos) ** 2)
            d2 = sqrt((x_gol - enemy2.xPos) ** 2 + (y_gol - enemy2.yPos) ** 2)
            d3 = sqrt((x_gol - enemy3.xPos) ** 2 + (y_gol - enemy3.yPos) ** 2)
            d_gol = array([[d1],
                           [d2],
                           [d3]])
            index = argmin(d_gol)
            dballgol = sqrt((x_gol - ball.xPos) ** 2 + (y_gol - ball.yPos) ** 2)
            if d_gol[index] < 20 and dballgol < 20:
                enemys = delete(enemys, index)
        else:
            d1 = sqrt((x_gol - enemys[0].xPos) ** 2 + (y_gol - enemys[0].yPos) ** 2)
            d2 = sqrt((x_gol - enemys[1].xPos) ** 2 + (y_gol - enemys[1].yPos) ** 2)
            d_gol = array([[d1],
                           [d2]])
            index = argmin(d_gol)
            if d_gol[index] < 20:
                enemys = delete(enemys, index)

        # for i in range(len(enemys)):
        #     print("Index: ", enemys[i].index)

        enemys = append(enemys, friend1)
        enemys = append(enemys, friend2)
        d_robot = zeros(len(enemys))
        # for i in range(len(enemys)):
        #     print("Index: ", enemys[i].index)
        for i in range(len(enemys)):
            d_robot[i] = robot.dist(enemys[i])

        index = argmin(d_robot)
        self.set_obst(enemys[index].xPos, enemys[index].yPos, 0, 0)
        # if enemys[index].teamYellow:
        #     print("Obstaculo: Amarelo " + str(enemys[index].index))
        # else:
        #     print("Obstaculo: Azul " + str(enemys[index].index))
        self.set_obst(enemys[index].xPos, enemys[index].yPos, 0, 0)

    # % This method print a little log on console
    def show_info(self):
        print('xPos: {:.2f} | yPos: {:.2f} | theta: {:.2f} | velocity: {:.2f}'.format(self.xPos, self.yPos,
                                                                                      float(self.theta), self.v))


# % Class to create the ball in game
class Ball:
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.vx = 0
        self.vy = 0
        self.pastPose = zeros(4).reshape(2, 2)  # ? Stores the last 3 positions (x,y) => updated on self.simGetPose()

    # % This method gets position of the ball in FIRASim
    def sim_get_pose(self, data_ball):
        self.xPos = data_ball.x #+ data_ball.vx * 100 * 12 / 60
        self.yPos = data_ball.y #+ data_ball.vy * 100 * 12 / 60

        # check if prev is out of field, in this case reflect ball moviment to reproduce the collision
        if self.xPos > 160:
            self.xPos = 160 - (self.yPos - 160)
        elif self.xPos < 10:
            self.xPos = 10 - (self.yPos - 10)

        if self.yPos > 130:
            self.yPos = 130 - (self.yPos - 130)
        elif self.yPos < 0:
            self.yPos = - self.yPos

        self.vx = data_ball.vx
        self.vy = data_ball.vy

    # % This method print a little log on console
    def show_info(self):
        print('xPos: {:.2f} | yPos: {:.2f}'.format(self.xPos, self.yPos))


# % Class to create the robots in game
class Robot:
    def __init__(self, index, actuator, mray):
        self.flagDirectGoal = False
        self.flagCruzamento = False
        self.flagTrocaFace = False
        self.teamYellow = mray
        self.spin = False
        self.contStopped = 0
        self.index = int32(index)
        self.actuator = actuator
        self.face = 1  # ? Defines the current face of the robot
        self.xPos = 0  # ? X position
        self.yPos = 0  # ? Y position
        self.theta = 0  # ? Orientation
        self.rightMotor = 0  # ? Right motor handle
        self.leftMotor = 0  # ? Left motor handle
        self.v = 0  # ? Velocity (cm/s) => updated on execution.py
        self.vx = 0
        self.vy = 0
        self.vTheta = 0
        self.vL = 0  # ? Left wheel velocity (cm/s) => updated on simClasses.py -> simSetVel()
        self.vR = 0  # ? Right wheel velocity (cm/s) =>  updated on simClasses.py -> simSetVel()
        self.vMax = 20   # ! Robot max velocity (cm/s)
        self.rMax = 6 * self.vMax  # ! Robot max rotation velocity (rad*cm/s)
        self.L = 7.5  # ? Base length of the robot (cm)
        self.LSimulador = 6.11  # ? Base length of the robot on coppelia (cm)
        self.R = 3.4  # ? Wheel radius (cm)
        self.obst = Obstacle()  # ? Defines the robot obstacle
        self.target = Target()  # ? Defines the robot target
        # ? Stores the last 3 positions (x,y) and orientation => updated on execution.py
        self.pastPose = zeros(12).reshape(4,
                                          3)
        self.dir_R = 0b00001100
        self.dir_L = 0b00000011
        self.lastError = None
        self.somaErro = 0
        self.lastTheta = None

        if self.index == 1:
            self.kw = 1.4#1.5
        else:
            self.kw = 1.15#1.5

    # % This method calculates the distance between the robot and an object
    def dist(self, obj):
        return sqrt((self.xPos - obj.xPos) ** 2 + (self.yPos - obj.yPos) ** 2)

    # % This method returns True if the distance between the target and the robot is less than 5cm - False otherwise
    def arrive(self):
        if self.dist(self.target) <= 7:
            return True
        else:
            return False

    # % This method gets both position and orientation of the robot in FIRASim
    def sim_get_pose(self, data_robot):
        self.xPos = data_robot.x
        self.yPos = data_robot.y
        self.vx = data_robot.vx
        self.vy = data_robot.vy
        self.theta = data_robot.a
        self.vTheta = data_robot.va
        self.v = sqrt(self.vx ** 2 + self.vy ** 2)

    def sim_set_vel(self, v, w):
        if self.face == 1:
            self.vR = v + 0.5 * self.L * w
            self.vL = v - 0.5 * self.L * w
        else:
            self.vL = -v - 0.5 * self.L * w
            self.vR = -v + 0.5 * self.L * w
        #self.actuator.send(self.index, self.vL, self.vR)
        self.setVel()

    def setVel(self):

        if self.index == 1:
            self.dir_R = 0b00001000
            self.dir_L = 0b00000010
            if self.vR > 0:
                self.dir_R = 0b00001000
            else:
                self.dir_R = 0b00000100
            if self.vL > 0:
                self.dir_L = 0b00000010
            else:
                self.dir_L = 0b00000001
        if self.index == 0:
            self.dir_R = 0b10000000
            self.dir_L = 0b00100000
            if self.vR > 0:
                self.dir_R = 0b10000000#0b01000000
            else:
                self.dir_R = 0b01000000
            if self.vL > 0:
                self.dir_L = 0b00100000
            else:
                self.dir_L = 0b00010000

            if self.vR == 0:
                self.dir_R = 0b00000000
            if self.vL == 0:
                self.dir_L = 0b00000000
            
        if self.index == 2:
            self.dir_R = 0b10000000
            self.dir_L = 0b00100000
            if self.vR > 0:
                self.dir_R = 0b10000000#0b01000000
            else:
                self.dir_R = 0b01000000
            if self.vL > 0:
                self.dir_L = 0b00100000
            else:
                self.dir_L = 0b00010000
        self.vR = int(abs(self.vR))
        self.vL = int(abs(self.vL))

    def sim_set_vel2(self, v1, v2):
        self.actuator.send(self.index, v1, v2)

    # % This method print a little log on console
    def show_info(self):
        print('xPos: {:.2f} | yPos: {:.2f} | theta: {:.2f} | velocity: {:.2f}'.format(self.xPos, self.yPos,
                                                                                      float(self.theta), float(self.v)))


'''
-------------------Descomentar quando atividade do Grid voltar
class Grid:
    def __init__(self):

        # criando um grid 5x6
        self.gridv = array([[17.5, 13],[42.5, 13], [67.5, 13],[92.5, 13], [117.5, 13],[142.5, 13],
                      [17.5, 39],[42.5, 39], [67.5, 39],[92.5, 39], [117.5, 39],[142.5, 39],
                      [17.5, 65],[42.5, 65], [67.5, 65],[92.5, 65], [117.5, 65],[142.5, 65],
                      [17.5, 91],[42.5, 91], [67.5, 91],[92.5, 91], [117.5, 91],[142.5, 91],
                      [17.5, 117],[42.5, 117], [67.5, 117],[92.5, 117], [117.5, 117],[142.5, 117] ])

        # definindo os angulos de cada grid
        self.AttitudeGrid = array([-pi/2, 0.47282204, 0.56910571, 0.70991061, 0.9279823, 1.27818735,
                             -pi/2, 0.29463669, 0.35945951, 0.46006287, 0.63557154, 1.0038244,
                             0.06148337, 0.07225452, 0.08759046, 0.11115443, 0.15188589, 0.23793116,
                             pi/2, -0.29463669, -0.35945951, -0.46006287, -0.63557154, -1.0038244,
                             pi/2,  -0.47282204, -0.56910571, -0.70991061, -0.9279823, -1.27818735])
        self.robotGridPos = zeros(3)
        self.ballGridPos = 0

    def update(self, robot0, robot1, robot2, ball):

        # encontrando o indice em que cada robo e a bola se encontra
        index0 = argmin(distance.cdist(self.gridv, [robot0.xPos, robot0.yPos]))
        index1 = argmin(distance.cdist(self.gridv, [robot1.xPos, robot1.yPos]))
        index2 = argmin(distance.cdist(self.gridv, [robot2.xPos, robot2.yPos]))
        indexb = argmin(distance.cdist(self.gridv, [ball.xPos, ball.yPos]))

        # Atualizando os valores
        self.robotGridPos = array([index0, index1, index2])
        self.ballGridPos = indexb

    def bestGridMov():

        # Posição dos robôs
        pos0 = self.gridv[index[0]]
        pos1 = self.gridv[index[1]]
        pos2 = self.gridv[index[2]]

        # Lista dos grids mais próximos de cada robô
        listAux0 = distance.cdist(self.gridv, self.gridv[pos0]) # calcula a distancia

        # Removendo o valor 0 da lista de distancias
        zeroId = where(listAux0 == 0)
        listAux0[zeroId] = 1000
        listAux0[zeroId] = listAux0.min()

        listId0 = where(list0Aux <= 37) # encontra o indice dos valores min
        # salva a posição dos valores min
        list0 = []
        for index in listId0[0]:
            list0.append(self.gridv[index])

        listAux1 = distance.cdist(self.gridv, self.gridv[pos1])

        zeroId = where(listAux1 == 0)
        listAux1[zeroId] = 1000
        listAux1[zeroId] = listAux1.min()

        listId1 = where(listAux1 <= 37)

        list1 = []
        for index in listId1[0]:
            list1.append(self.gridv[index])

        listAux2 = distance.cdist(self.gridv, self.gridv[pos2])

        zeroId = where(listAux2 == 0)
        listAux2[zeroId] = 1000
        listAux2[zeroId] = listAux2.min()

        listId2 = where(listAux2 <= 37)
        list2 = []
        for index in listId2[0]:
            list0.append(self.gridv[index])

        #Verifica se a posição que ele vai se mover já tem algum robô

        if self.robotGridPos[1] in listId0:
            listId0n = delete(listId0[0], where(listId0 == self.robotGridPos[1]))
            list0 = delete(list0, where(listId0 == self.robotGridPos[1]), axis = 0)
        if self.robotGridPos[2] in listId0:
            listId0 = delete(listId0[0], where(listId0 == self.robotGridPos[2]))
            list0 = delete(list0, where(listId0 == self.robotGridPos[2]), axis = 0)

        if self.robotGridPos[0] in listId1:
            listId1n = delete(listId1[0], where(listId1 == self.robotGridPos[0]))
            list1 = delete(list1, where(listId1 == self.robotGridPos[0]), axis = 0)
        if self.robotGridPos[2] in listId1:
            listId1 = delete(listId1[0], where(listId1 == self.robotGridPos[2]))
            list1 = delete(list1, where(listId1 == self.robotGridPos[2]), axis = 0)

        if self.robotGridPos[0] in listId2:
            listId2n = delete(listId2[0], where(listId2 == self.robotGridPos[0]))
            list2 = delete(list2, where(listId2 == self.robotGridPos[0]), axis = 0)
        if self.robotGridPos[1] in listId2:
            listId2 = delete(listId2[0], where(listId2 == self.robotGridPos[1]))
            list2 = delete(list2, where(listId2 == self.robotGridPos[1]), axis = 0)

        # Encontrando qual grid é o mais próximo da bola
        targetId0 = argmin(distance.cdist(list0, self.gridv[indexb]))
        target0 = self.gridv[listId0n[0][targetId0]]

        targetId1 = argmin(distance.cdist(list1, self.gridv[indexb]))
        target1 = self.gridv[listId1n[0][targetId1]]

        targetId2 = argmin(distance.cdist(list2, self.gridv[indexb]))
        target2 = self.gridv[listId2n[0][targetId2]]

    #def doInGrid():
'''
