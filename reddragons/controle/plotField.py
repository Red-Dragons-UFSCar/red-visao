import matplotlib.pyplot as plt

import behaviours
from bridge import (Vision)
from simClasses import *
from strategy import *


class PlotField:
    def __init__(self):
        self.figureOpen = False

    def plot_interactive(self, target, robot, obstacle=None):
        self.univec = behaviours.Univector()  # Objeto univector
        self.x_pos = range(1, 150, 5)  # Plot do campo inteiro
        self.y_pos = range(1, 150, 5)

        self.robo = robot

        self.x_plot = []
        self.y_plot = []
        self.V = []

        for i in self.x_pos:
            for j in self.y_pos:
                self.robo.xPos = i  # Variação da posição do robô
                self.robo.yPos = j
                if obstacle is None:
                    self.theta = self.univec.hip_vec_field(self.robo, target)
                else:
                    # Calculo do angulo desejado pelo campo hiperbólico
                    self.theta = self.univec.univec_field_h(self.robo, target,
                                                            obstacle)

                self.theta.astype(np.float64)  # Adequações
                if type(self.theta) == type(np.array([])):
                    self.theta = self.theta[0]

                self.matrix = self.univec.rot_matrix(self.theta)  # Criando vetores unitarios com o angulo retornado
                self.vetPos = np.dot(self.matrix, np.array([[1], [0]]))
                self.V.append([list(self.vetPos[0])[0], list(self.vetPos[1])[0]])
                self.x_plot.append(i)
                self.y_plot.append(j)

        self.V = np.array(self.V)
        origin = np.array([self.x_plot, self.y_plot])

        if not self.figureOpen:
            plt.ion()
            self.fig, ax = plt.subplots(1, 1)
            self.Q = ax.quiver(*origin, self.V[:, 0], self.V[:, 1])
            self.figureOpen = True
        else:
            self.Q.set_UVC(self.V[:, 0], self.V[:, 1])

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # plt.quiver(*origin, V[:,0], V[:,1])
        # plt.show(block=True)


if __name__ == '__main__':
    mray = True

    vision = Vision(mray, "224.0.0.1", 10002)

    teamYellow = mray

    robot0 = Robot(0, actuator=None, mray=teamYellow)
    robot1 = Robot(1, actuator=None, mray=teamYellow)
    robot2 = Robot(2, actuator=None, mray=teamYellow)

    robotEnemy0 = Robot(0, actuator=None, mray=teamYellow)
    robotEnemy1 = Robot(1, actuator=None, mray=teamYellow)
    robotEnemy2 = Robot(2, actuator=None, mray=teamYellow)

    ball = Ball()

    strategy = Strategy(robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, ball, mray)

    plot = PlotField()

    while True:
        # Atualiza os dados da visão
        vision.update()
        field = vision.get_field_data()

        data_our_bot = field["our_bots"]  # Salva os dados dos robôs aliados
        data_their_bots = field["their_bots"]  # Salva os dados dos robôs inimigos
        data_ball = field["ball"]  # Salva os dados da bola

        # Atualiza em cada objeto do campo os dados da visão
        robot0.sim_get_pose(data_our_bot[0])
        robot1.sim_get_pose(data_our_bot[1])
        robot2.sim_get_pose(data_our_bot[2])
        robotEnemy0.sim_get_pose(data_their_bots[0])
        robotEnemy1.sim_get_pose(data_their_bots[1])
        robotEnemy2.sim_get_pose(data_their_bots[2])
        ball.sim_get_pose(data_ball)

        # Shoot
        # if not mray:
        #    arrivalTheta=arctan2(65-ball.yPos,150-ball.xPos) #? Angle between the ball and point (150,65)
        # else:
        #    arrivalTheta=arctan2(65-ball.yPos,-ball.xPos) #? Angle between the ball and point (0,65)

        # Shoot 2
        if not mray:
            if (ball.yPos > 45) and (ball.yPos < 85):
                arrivalTheta = 0
            elif ball.yPos <= 45:
                y = 45 + (45 - ball.yPos) / (45 - 0) * 20
                arrivalTheta = arctan2(y - 45, 160 - ball.xPos)
            else:
                y = 85 - (ball.yPos - 85) / (130 - 85) * 20
                arrivalTheta = arctan2(y - 85, 160 - ball.xPos)
        else:
            if (ball.yPos > 45) and (ball.yPos < 85):
                arrivalTheta = pi
            elif ball.yPos <= 45:
                y = 45 + (45 - ball.yPos) / (45 - 0) * 20
                arrivalTheta = arctan2(y - 45, 10 - ball.xPos)
            else:
                y = 85 - (ball.yPos - 85) / (130 - 85) * 20
                arrivalTheta = arctan2(y - 85, 10 - ball.xPos)

        robot2.target.update(ball.xPos, ball.yPos, arrivalTheta)
        robot2.obst.update(robot2, robot0, robot1, robotEnemy0, robotEnemy1, robotEnemy2)

        plot.plot_interactive(robot2.target, robot2.obst)
