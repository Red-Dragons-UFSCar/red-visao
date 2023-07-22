from dataclasses import field
from email.mime import image
import math
from operator import index
import numpy as np
import pandas as pd
#from vss_communication import Vision

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from yaml import MarkedYAMLError
from reddragons.estruturas.models.imagem import Imagem
from reddragons.interface.pages import controle
from reddragons.utils import Logger
from reddragons.visao import processamento
from reddragons.visao.services import centros
import reddragons.utils as vutils
import time, threading
import matplotlib.pyplot as plt

from reddragons.controle import ControleEstrategia

from ..utils import ui_files



class Entity_Allie:
    def __init__(self, x=0, y=0, vx=0, vy=0, a=0, va=0, index=0):
        """
        Salva posição do robô aliado
        """
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.a = a
        self.va = 0
        self.index = index

class Entity_Enemy:
    def __init__(self, x=0, y=0, vx=0, vy=0, a=0, va=0, index=0):
        """"
        Salva posição do robô adversário
        """
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.a = a
        self.va = 0
        self.index = index

class Entity_ball:
    def __init__(self, x=0, y=0, vx = 0 , vy = 0, a = None, va = None, index = None):
        """"
        Salva posição da bola
        """
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.a = a
        self.va = 0
        self.index = None


class GUI_jogar(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_jogar, self).__init__()
        loadUi(f"{ui_files}/jogar.ui", self)
        self.show()
        self.visao = visao
        self.model = model
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

        self.mray = None

        self.Entidade_bola = [0,0]
        self.Entidades_Aliadas = [[0,0,0],[0,0,0],[0,0,0]]
        self.valores_atrasados_adv = [[0,0],[0,0],[0,0]]

        
        self.valores_PB = []
        self.valores_PB_bola = [0,0]

        self.jogando = False

        self.Entidade_bola = Entity_ball
        
        self.Robo0Aliado = Entity_Allie(index = 0)
        self.Robo1Aliado = Entity_Allie(index = 1)
        self.Robo2Aliado = Entity_Allie(index = 2)



        self.Entidades_Aliadas = [self.Robo0Aliado, self.Robo1Aliado, self.Robo2Aliado]
        #self.objControle = ControleEstrategia(self.mray)

        self.maior = 0
        self.diff_Total = [10000,10000,10000]
        self.indexizacao = [0,1,2]
        self.roboEncontrado = None
        self.roboPerdido = None

        self.btPararTransmissao.clicked.connect(self.pararTransmissao)
        self.btJogar.clicked.connect(self.conversao_controle)
        self.btJogar.clicked.connect(self.indicador)
        self.rJogar.clicked.connect(self.muda_btnJogar)
        self.rParar.clicked.connect(self.muda_btnParar)

        self.rGerarGraf.clicked.connect(self.GerarGraf)


        self.esq_radio.toggled.connect(self.mudancalados)
        self.dir_radio.toggled.connect(self.mudancalados)

        #self.protobuff = Vision()


    def mudancalados(self):
        """
        Definição de lado
        """
        if self.dir_radio.isChecked():
            self.mray = True
            print('Lado direito')
        elif self.esq_radio.isChecked():
            self.mray = False
            print('Lado esquerdo')



    def inicializarValores(self):
        """
        Inicializa como esquerda
        """
        self.esq_radio.setChecked(self.trocouCampo)

    def muda_btnJogar(self):
        """
        Definição do estado de jogo
        """
        game_on = True
        self.jogando = game_on
        print('Game on')

    def indicador(self):
        print('Transmissão iniciada')

    def muda_btnParar(self):
        """
        Parar jogo
        """
        game_on = False
        self.jogando = game_on
        print('Game off')

    def update_frame(self):
        """
        Atualização dos frames na intrface e coloca as informações atuais no frame
        """

        imagem = self.model.imagem
        dados_controle = self.visao.sincronizar_controle_dinamico()

        #primeira cv2 line tem que ser modificada, pois o angulo ficou confuso
        img = imagem.imagem_crop
        cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p, a in zip(cores, imagem.centros, dados_controle.angulo_d):
            cv2.circle(img, (int(p[0]), int(p[1])), 20, c, 1)
            cv2.line(
                img,
                (int(p[0]), int(p[1])),
                (int(p[0] + math.cos(p[2] + 180) * 25), int(p[1] + math.sin(p[2]) * 25)),
                c,
                3,
            )  # Angulo Robo
            # cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(Dados.ang_corr)*50), int(p[1]+ math.sin(Dados.ang_corr)*50)), c, 1)
            cv2.line(
                img,
                (int(p[0]), int(p[1])),
                (int(p[0] + math.cos(a) * 25), int(p[1] + math.sin(a) * 25)),
                (255, 255, 0),
                1,
            )  # Angulo controle

        cores = [(55, 55, 55), (10, 10, 10), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p in zip(cores, imagem.centroids):
            for _p in p[0]:
                cv2.circle(img, (int(_p[0]), int(_p[1])), 4, c, -1)
        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_jogar.setPixmap(_q_pixmap)

        #self.conversao_controle()

    def ativa_serial(self):
        """
        Inicializa antiga transmissão de dados, não mais usada
        """

        dados_controle = self.model.controle

        if self.jogando:
            self.jogando = False
            self.btJogar.setText("Iniciar transmissao")
            self.btJogar.setStyleSheet("background-color:green")
            dados_controle.ser = 0
        else:
            try:
                # Descomentar quando em jogo
                #dados_controle.ser = serial.Serial(dados_controle.porta,dados_controle.velocidade)
                self.jogando = True
                self.btJogar.setText("Terminar transmissao")
                self.btJogar.setStyleSheet("background-color:red")
            except:
                Logger().erro("Porta não encontrada")
                self.jogando = False
                self.btJogar.setText("Iniciar transmissao")
                self.btJogar.setStyleSheet("background-color:green")
                dados_controle.ser = 0

        self.model.controle = dados_controle

    def closeEvent(self, event):
        """
        Fecha e para 
        """
        self.timer.stop()
        event.accept()

    def mudanca(self):
        """
        Antiga inicialização do jogo
        """
        dados_controle = self.visao.sincronizar_controle_dinamico()

        dados_controle.Pjogar = True if self.jogando is True else False
        dados_controle.Pparar = True if self.jogando is False else False

        self.model.controle = dados_controle


    def conversao_controle(self):

        """
        Converte os dados para o controle, também faz tratamento de erro para robôs adversários perdidos
        """

        #Colocar em Loop

        #while True:
        #if not self.jogando:
        #    continue

        alpha = 0.6



        imagem = self.model.imagem

        services = centros.Centros(self.model)

        if imagem.centroids[0] == []:
            print('Bola perdida, usando último valor')
        else:
            try:
                pos_bolax = (imagem.centroids[0][0][0][0])*170/640
                pos_bolay = ((480 - imagem.centroids[0][0][0][1])*130/480)
            except IndexError:
                Logger().erro(str(imagem.centroids[0]))

        
        alpha_bola = 0.7

        if self.valores_PB_bola[0] == 0:
            self.valores_PB_bola[0] = pos_bolax

        if self.valores_PB_bola[1] == 1:
            self.valores_PB_bola[1] = pos_bolay

        self.Entidade_bola.x = alpha_bola*self.valores_PB_bola[0] + (1-alpha_bola)*pos_bolax
        self.valores_PB_bola[0] = alpha_bola*self.valores_PB_bola[0] + (1-alpha_bola)*pos_bolax
        self.Entidade_bola.vx = 0
        self.Entidade_bola.y = alpha_bola*self.valores_PB_bola[1] + (1-alpha_bola)*pos_bolay
        self.valores_PB_bola[1] = alpha_bola*self.valores_PB_bola[1] + (1-alpha_bola)*pos_bolay
        self.Entidade_bola.vy = 0

        XAliado = []
        YAliado = []
        aAliado = []
        indice_roboAliado = []
        #x, y e angulo do robo

        for i in range(0, 3):
            XAliado.append((imagem.centros[i][0])*170/640)
            YAliado.append((480 - imagem.centros[i][1])*130/480)
            aAliado.append((-1)*services.run(imagem.centroids)[0][i][2])
            indice_roboAliado.append(i)



        alpha_angulo = 0.8

        for l in range(0,3):
            self.Entidades_Aliadas[l].x = alpha*self.Entidades_Aliadas[l].x + (1-alpha)*XAliado[l]
            self.Entidades_Aliadas[l].y = alpha*self.Entidades_Aliadas[l].y + (1-alpha)*YAliado[l]
            a_aux = aAliado[l] + np.pi
            aAliado[l] = np.arctan2(np.sin(a_aux), np.cos(a_aux))*180/np.pi
            if aAliado[l] == 0:
                self.Entidades_Aliadas[l].a = aAliado[l]
            elif self.Entidades_Aliadas[l].a/aAliado[l] > 0:
                self.Entidades_Aliadas[l].a = alpha_angulo*self.Entidades_Aliadas[l].a + (1-alpha_angulo)*aAliado[l]
            elif (self.Entidades_Aliadas[l].a/aAliado[l]) < 0 and (-10 < self.Entidades_Aliadas[l].a < 10 or -10 < aAliado[l] < 10):
                self.Entidades_Aliadas[l].a = alpha_angulo*self.Entidades_Aliadas[l].a + (1-alpha_angulo)*aAliado[l]
            else:
                self.Entidades_Aliadas[l].a = aAliado[l]

        XAdversario = []
        YAdversario = []
        indice_roboAdversario = [10,10,10]

        errinho = 0

        for i in range(0,3):
            try:
                XAdversario.append((imagem.centroids[5][0][i][0])*170/640)
                YAdversario.append((480 - imagem.centroids[5][0][i][1])*130/480)
                indice_roboAdversario[i] = i
            except IndexError:
                errinho += 1
                pass


        diff_normal = [10,10,10]

        if errinho == 1:
            try:
                for j in range(0,3):
                    for i in range(0,2):
                        diff_tot = abs(XAdversario[i] - self.valores_atrasados_adv[j][0] + YAdversario[i] - self.valores_atrasados_adv[j][1])
                        if diff_tot < self.diff_Total[j]:
                            self.diff_Total[j] = diff_tot
                            #Até aqui tá rodando perfeitamente
                print('diff', self.diff_Total)
                for l in range(0,3):
                    #atualizar isso para funções minimo e index
                    if self.diff_Total[l] > self.maior:
                        self.maior = self.diff_Total[l]
                        self.roboPerdido = l
                print('robo perdido', self.roboPerdido)
                XAdversario.append(self.valores_atrasados_adv[self.roboPerdido][0])
                YAdversario.append(self.valores_atrasados_adv[self.roboPerdido][1])
            except IndexError:
                pass

        self.mnor = 100000
        a = 1
        if errinho == 2:
            try:
                for i in range(0,3):
                    for k  in range(0,3):
                        for j in range (0,2):
                            if diff_normal[k] < self.mnor:
                                diff_normal[k] = abs(XAdversario[i] - self.valores_atrasados_adv[j][0] + YAdversario[i] - self.valores_atrasados_adv[j][1])
                                self.roboEncontrado = j
                                #Acho que não precisa estar aqui
                                self.mnor = diff_normal[k]



                for i in range(0,3):
                    if self.roboEncontrado != i:
                        XAdversario.append(self.valores_atrasados_adv[i][0])
                        YAdversario.append(self.valores_atrasados_adv[i][1])
                        a += 1
            except:
                pass


        if errinho == 3:
            for i in range(0,3):
                XAdversario.append(self.valores_atrasados_adv[i][0])
                YAdversario.append(self.valores_atrasados_adv[i][1])

        Robo0Adversario = Entity_Enemy(index = 0)
        Robo1Adversario = Entity_Enemy(index = 1)
        Robo2Adversario = Entity_Enemy(index = 2)

        Entidades_Adversarias = [Robo0Adversario, Robo1Adversario, Robo2Adversario]


        for l in range(0,3):
            try:
                Entidades_Adversarias[l].x = XAdversario[l]
                Entidades_Adversarias[l].y = YAdversario[l]
                self.valores_atrasados_adv[l][0] = XAdversario[l]
                self.valores_atrasados_adv[l][1] = YAdversario[l]
            except IndexError:
                #print('Entidade adversária não atualizada', imagem.centroids[5][0])
                pass


        if errinho > 0:
            print('valores atrasados',self.valores_atrasados_adv)
            print('Xadv',XAdversario, 'num de robos perdidos', errinho)


        self.estado = self.jogando

        self.campo = dict(ball = self.Entidade_bola, our_bots = self.Entidades_Aliadas, their_bots = Entidades_Adversarias, Yellow = self.mray) #Ainda está dando erro
        
        self.convertEntidadeProtobuff()

        self.looping = threading.Timer(0.02, self.conversao_controle)
        self.looping.start()

    def Cancel(self):
        self.close()

    def closeEvent(self,event):
        self.looping.cancel()
        event.accept()

    def pararTransmissao(self, event):
        print("Transmissao encerrada")
        self.looping.cancel()
    
    def convertEntidadeProtobuff(self):
        our_bots = []
        their_bots = []
        for i in range(3):
            our_bots.append(dict([ ("robot_id", i), 
                                   ("x", self.campo["our_bots"][i].x), 
                                   ("y", self.campo["our_bots"][i].y), 
                                   ("orientation", self.campo["our_bots"][i].a), 
                                   ("vx", self.campo["our_bots"][i].vx), 
                                   ("vy", self.campo["our_bots"][i].vy), 
                                   ("vorientation", self.campo["our_bots"][i].va) ]))
            their_bots.append(dict([ ("robot_id", i), 
                                     ("x", self.campo["their_bots"][i].x), 
                                     ("y", self.campo["their_bots"][i].y), 
                                     ("orientation", self.campo["their_bots"][i].a), 
                                     ("vx", self.campo["their_bots"][i].vx), 
                                     ("vy", self.campo["their_bots"][i].vy), 
                                     ("vorientation", self.campo["their_bots"][i].va) ]))
        ball = dict([ ("x", self.campo["ball"].x), 
                      ("y", self.campo["ball"].y), 
                      ("z", 0), 
                      ("vx", self.campo["ball"].vx), 
                      ("vy", self.campo["ball"].vy), 
                      ("vz", 0) ])
        
        self.campo_protobuff = dict([ ("ball", ball), ("robots_blue", our_bots), ("robots_yellow", their_bots) ])
        #self.protobuff.send_mensage(self.campo_protobuff)
        #print(self.campo_protobuff)
        
    def GerarGraf(self):
        print("Função desativada")