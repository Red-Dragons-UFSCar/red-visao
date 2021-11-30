import time
import sys

#import fouls
from .fouls import *
from .simClasses import *
from .strategy import *

class ControleEstrategia:
    def __init__(self, team=True, side=True, strategy='default'):
        self.team = team                # Amarelo é true e Azul é falso
        self.side = side                # Verificar as estategias para a mudança de lado
        self.strategies = ['default', 'twoAttackers']

        self.robot0 = Robot(0, None, self.team)
        self.robot1 = Robot(1, None, self.team)
        self.robot2 = Robot(2, None, self.team)

        self.robotEnemy0 = Robot(0, None, not self.team)
        self.robotEnemy1 = Robot(1, None, not self.team)
        self.robotEnemy2 = Robot(2, None, not self.team)

        self.ball = Ball()

        self.strategy = Strategy(self.robot0, self.robot1, self.robot2, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.ball, self.team, strategy)

        print("criou porra!!!!!")

    def update(self, referee, field):

        data_our_bot = field["our_bots"]  # Salva os dados dos robôs aliados
        data_their_bots = field["their_bots"]  # Salva os dados dos robôs inimigos
        data_ball = field["ball"]  # Salva os dados da bola

        self.robot0.sim_get_pose(data_our_bot[0])
        self.robot1.sim_get_pose(data_our_bot[1])
        self.robot2.sim_get_pose(data_our_bot[2])
        self.robotEnemy0.sim_get_pose(data_their_bots[0])
        self.robotEnemy1.sim_get_pose(data_their_bots[1])
        self.robotEnemy2.sim_get_pose(data_their_bots[2])
        self.ball.sim_get_pose(data_ball)

        if ref_data["game_on"]:                                 #TODO: Deixar os comentários em inglês
            # Se o modo de jogo estiver em "Game on"
            # strategy.twoAttackers()
            # strategy.coach()
            self.strategy.decider()

        elif ref_data["foul"] == 1 and ref_data["yellow"] == (not mray):
            # Detectando penalti defensivo
            self.strategy.penaltyDefensive = True
            # actuator.stop() ---- INSERIR FUNÇÃO DE SET: VELOCIDADE DOS ROBOS IGUAIS A ZERO
            replacement_fouls(None, ref_data, mray)

        elif ref_data["foul"] == 1 and ref_data["yellow"] == (mray):
            # Detectando penalti ofensivo
            self.strategy.penaltyOffensive = True
            # actuator.stop() ---- INSERIR FUNÇÃO DE SET: VELOCIDADE DOS ROBOS IGUAIS A ZERO
            replacement_fouls(None, ref_data, mray)

        elif ref_data["foul"] != 7:
            if ref_data["foul"] != 5:  # Mudando a flag exceto em caso de Stop
                self.strategy.penaltyOffensive = False
                self.strategy.penaltyDefensive = False
            replacement_fouls(None, ref_data, mray)
            # actuator.stop() ---- INSERIR FUNÇÃO DE SET: VELOCIDADE DOS ROBOS IGUAIS A ZERO

        else:
            # actuator.stop() ---- INSERIR FUNÇÃO DE SET: VELOCIDADE DOS ROBOS IGUAIS A ZERO
            pass
