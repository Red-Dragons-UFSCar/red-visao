import time
import sys

#import fouls
from .fouls import *
from .simClasses import *
from .strategy import *

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


    def update(self, game_on, field):

        
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
        

        if game_on:                                 #TODO: Deixar os comentários em inglês
            # Se o modo de jogo estiver em "Game on"
            # strategy.twoAttackers()
            # strategy.coach()
            #self.strategy.decider()
            print('Jogo rodando')
        else:
            print('Jogo parado')