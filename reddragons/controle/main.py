import time
import sys
import serial
import numpy as np

#import fouls
from .fouls import *
from .simClasses import *
from .strategy import *
from .action import shoot
#from .bridge import (Actuator, Replacer, Vision, Referee)

class ControleEstrategia:
    def __init__(self, side=True, strategy='default'):
        self.side = side                 # Amarelo é true e Azul é falso # Verificar as estategias para a mudança de lado
        self.strategies = ['default', 'twoAttackers']

        self.robot0 = Robot(0, None, self.side)
        self.robot1 = Robot(1, None, self.side)
        self.robot2 = Robot(2, None, self.side)

        self.robotEnemy0 = Robot(0, None, not self.side)
        self.robotEnemy1 = Robot(1, None, not self.side)
        self.robotEnemy2 = Robot(2, None, not self.side)

        self.ball = Ball()

        self.strategy = Strategy(self.robot0, self.robot1, self.robot2, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.ball, self.side, strategy)

        self.serialPort = '/dev/ttyACM0'
        self.serialBaudRate = 115200

        self.startSerial()

        #self.referee = Referee(side, "224.5.23.2", 10003)
        #self.r = RefereeComm(config_file = "config.json")
        #self.r.start()

    def startSerial(self):
        # Instanciamento do objeto serial de comunicação
        self.ser = serial.Serial()
        self.ser.baudrate = self.serialBaudRate
        self.ser.port = self.serialPort # Conferir a porta USB que será utilizada
        self.ser.open()

    def update(self, game_on, field):

        #self.referee.update()
        #ref_data = self.referee.get_data()

        #game_on = ref_data["game_on"]

        #ref_data = self.r.get_last_foul()

        self.robot0.mray = field["Yellow"]
        self.robot1.mray = field["Yellow"]
        self.robot2.mray = field["Yellow"]

        data_our_bot = field["our_bots"] # Salva os dados dos robôs aliados
        data_their_bots = field["their_bots"]  # Salva os dados dos robôs inimigos
        data_ball = field["ball"]  # Salva os dados da bola

        self.robot0.sim_get_pose(data_our_bot[0])
        self.robot1.sim_get_pose(data_our_bot[1])
        self.robot2.sim_get_pose(data_our_bot[2])
        self.robotEnemy0.sim_get_pose(data_their_bots[0])
        self.robotEnemy1.sim_get_pose(data_their_bots[1])
        self.robotEnemy2.sim_get_pose(data_their_bots[2])
        self.ball.sim_get_pose(data_ball)

        # if(self.ball.xPos > self.robot1.xPos):
        #     dirMot1_Robo2 = 0b00001000
        #     dirMot2_Robo2 = 0b00000010
        #     v1 = 25
        #     v2 = 25
        # else:
        #     dirMot1_Robo2 = 0b00000100
        #     dirMot2_Robo2 = 0b00000001
        #     v1 = 25
        #     v2 = 25

        # print("x = " + str(self.robot0.xPos))
        # print("y = " + str(self.robot0.yPos))
        # print("a = " + str(self.robot0.theta))



        dirMot1_Robo3 = 0b11000000
        dirMot2_Robo3 = 0b00110000
        v3 = 0
        v4 = 0
        dirMot1_Robo1 = 0b11000000
        dirMot2_Robo1 = 0b00110000
        va = 0
        vb = 0
        #direcao1 = dirMot1_Robo1 + dirMot2_Robo1 + dirMot1_Robo2 + dirMot2_Robo2
        #direcao2 = dirMot1_Robo3 + dirMot2_Robo3
        direcao1 = self.robot0.dir_R + self.robot0.dir_L + self.robot1.dir_R + self.robot1.dir_L
        direcao2 = self.robot2.dir_R + self.robot2.dir_L
        Rd = bytearray([111, direcao1, direcao2, self.robot0.vR, self.robot0.vL, self.robot1.vR, self.robot1.vL, self.robot2.vR, self.robot2.vL, 112])
        self.ser.write(Rd)
        """
        print("Bola: ")
        print("x = " + str(self.ball.xPos))
        print("y = " + str(self.ball.yPos))
        print("Robo 0: ")
        print("x = " + str(self.robot0.xPos))
        print("y = " + str(self.robot0.yPos))
        print("a = " + str(self.robot0.theta))
        print("Robo 1: ")
        print("x = " + str(self.robot1.xPos))
        print("y = " + str(self.robot1.yPos))
        print("a = " + str(self.robot1.theta))
        print("Robo 2: ")
        print("x = " + str(self.robot2.xPos))
        print("y = " + str(self.robot2.yPos))
        print("a = " + str(self.robot2.theta))
        print("Robo 0: ")
        print("x = " + str(self.robotEnemy0.xPos))
        print("y = " + str(self.robotEnemy0.yPos))
        print("a = " + str(self.robotEnemy0.theta))
        print("Robo 1: ")
        print("x = " + str(self.robotEnemy1.xPos))
        print("y = " + str(self.robotEnemy1.yPos))
        print("a = " + str(self.robotEnemy1.theta))
        print("Robo 2: ")
        print("x = " + str(self.robotEnemy2.xPos))
        print("y = " + str(self.robotEnemy2.yPos))
        print("a = " + str(self.robotEnemy2.theta))
        """
        #print(ref_data)
        if game_on:                                 #TODO: Deixar os comentários em inglês
        #if ref_data['can_play']:                                 #TODO: Deixar os comentários em inglês
            # Se o modo de jogo estiver em "Game on"
            # strategy.twoAttackers()
            # strategy.coach()
            #self.strategy.decider()
            #print('Jogo rodando')
            #shoot(self.robot1, self.ball, left_side=self.robot1.mray)
            #shoot(self.robot0, self.ball, left_side=self.robot1.mray)
            #shoot(self.robot2, self.ball, left_side=self.robot2.mray)
            #shoot(self.robot1, self.ball, left_side=not self.robot2.mray)
            #self.robot2.sim_set_vel(10, 0)

            # Zagueiro
            #'''
            if not self.robot1.mray:
                if self.ball.xPos > 85:
                    screen_out_ball(self.robot1, self.ball, 50, upper_lim=110, lower_lim=20, left_side=not self.robot1.mray, doubleFace=False)
                else:
                    shoot(self.robot1, self.ball, left_side= not self.robot1.mray)
            #self.robot1.sim_set_vel(10, 5)
            #'''

            #'''
            # Atacante
            if not self.robot2.mray:
                if self.ball.xPos > 75:
                    shoot(self.robot2, self.ball, left_side= not self.robot2.mray)
                else:
                    screen_out_ball(self.robot2, self.ball, 90, upper_lim=110, lower_lim=20, left_side=not self.robot2.mray, doubleFace=False)
            else:
                if self.ball.xPos < 160-75:
                    shoot(self.robot2, self.ball, left_side= not self.robot2.mray)
                else:
                    screen_out_ball(self.robot2, self.ball, 60, upper_lim=110, lower_lim=20, left_side=not self.robot2.mray, doubleFace=False)
            #'''

            #testar amanhã
            if self.ball.yPos > self.robot0.yPos and self.robot0.mray:
                self.robot0.sim_set_vel(0, 20)
            else:
                self.robot0.sim_set_vel(0, -20)

            if self.ball.yPos < self.robot0.yPos and not self.robot0.mray:
                self.robot0.sim_set_vel(0, 20)
            else:
                self.robot0.sim_set_vel(0, -20)

            #shoot(self.robot2, self.ball, left_side= not self.robot2.mray)
            #roboSimples(self.robot1, self.ball)


        else:
            print('Jogo parado')
            self.robot1.sim_set_vel(0, 0)
            self.robot0.sim_set_vel(0, 0)
            self.robot2.sim_set_vel(0, 0)
