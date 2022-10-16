from dataclasses import field
from email.mime import image
import math
from operator import index
import numpy as np

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

from reddragons.controle import ControleEstrategia

from ..utils import ui_files



class Entity_Allie:
    def __init__(self, x=0, y=0, vx=0, vy=0, a=0, va=0, index=0):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.a = a
        self.va = 0
        self.index = index

class Entity_Enemie:
    def __init__(self, x=0, y=0, vx=0, vy=0, a=0, va=0, index=0):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.a = a
        self.va = 0
        self.index = index

class Entity_ball:
    def __init__(self, x=0, y=0, vx = 0 , vy = 0, a = None, va = None, index = None):
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

        self.mray = True

        self.valores_atrasados = [[0,0],[0,0],[0,0]]

        self.jogando = False
        self.objControle = ControleEstrategia(self.mray)

        self.btJogar.clicked.connect(self.conversao_controle)
        self.rJogar.clicked.connect(self.muda_btnJogar)
        self.rParar.clicked.connect(self.muda_btnParar)


        self.esq_radio.toggled.connect(self.mudancalados)
        self.dir_radio.toggled.connect(self.mudancalados)

    def mudancalados(self):
        if self.dir_radio.isChecked():
            mray = True
            print('Lado direito')
        elif self.esq_radio.isChecked():
            mray = False
            print('Lado esquerdo')
        


    def inicializarValores(self):
        self.esq_radio.setChecked(self.trocouCampo)

    def muda_btnJogar(self):
        game_on = True
        self.jogando = game_on
        print('Game on')

    def muda_btnParar(self):
        game_on = False
        self.jogando = game_on
        print('Game off')

    def update_frame(self):

        imagem = self.model.imagem
        dados_controle = self.visao.sincronizar_controle_dinamico()

        img = imagem.imagem_crop
        cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p, a in zip(cores, imagem.centros, dados_controle.angulo_d):
            cv2.circle(img, (int(p[0]), int(p[1])), 20, c, 1)
            cv2.line(
                img,
                (int(p[0]), int(p[1])),
                (int(p[0] + math.cos(p[2]) * 25), int(p[1] + math.sin(p[2]) * 25)),
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
        self.timer.stop()
        event.accept()

    def mudanca(self):

        dados_controle = self.visao.sincronizar_controle_dinamico()

        dados_controle.Pjogar = True if self.jogando is True else False
        dados_controle.Pparar = True if self.jogando is False else False

        self.model.controle = dados_controle


    def conversao_controle(self):


        #Colocar em Loop

        #while True:
        #if not self.jogando:
        #    continue

        imagem = self.model.imagem
        #dados = self.model.dados.copy()

        services = centros.Centros(self.model)

        #Tratamento de erro da bolinha a fazer
        if imagem.centroids[0] == []:
            print('Bola perdida, usando último valor')
        else:
            try:
                pos_bolax = (imagem.centroids[0][0][0][0])*170/640
                pos_bolay = ((480 - imagem.centroids[0][0][0][1])*130/480)
            except IndexError:
                Logger().erro(str(imagem.centroids[0]))

        Entidade_bola = Entity_ball
        Entidade_bola.x = pos_bolax
        Entidade_bola.vx = 0
        Entidade_bola.y = pos_bolay
        Entidade_bola.vy = 0

        XAliado = []
        YAliado = []
        aAliado = []
        indice_roboAliado = []
        #x, y e angulo do robo

        for i in range(0, 3):
            XAliado.append((imagem.centros[i][0])*170/640)
            YAliado.append((480 - imagem.centros[i][1])*130/480)
            #aAliado.append((-1)*services.run(imagem.centroids)[0][i][2]*180/np.pi)
            aAliado.append((-1)*services.run(imagem.centroids)[0][i][2])
            indice_roboAliado.append(i)


        #    Entity_Allie(x = XAliado[l], y = YAliado[l], a = aAliado[l], index = indice_roboAliado[l])

        Robo0Aliado = Entity_Allie(index = 0)
        Robo1Aliado = Entity_Allie(index = 1)
        Robo2Aliado = Entity_Allie(index = 2)


        Entidades_Aliadas = [Robo0Aliado, Robo1Aliado, Robo2Aliado]


        for l in range(0,3):
            Entidades_Aliadas[l].x = XAliado[l]
            Entidades_Aliadas[l].y = YAliado[l]
            a_aux = aAliado[l] - np.pi/4
            aAliado[l] = np.arctan2(np.sin(a_aux), np.cos(a_aux))*180/np.pi
            Entidades_Aliadas[l].a = aAliado[l]


        XAdversario = [1,1,1]
        YAdversario = [1,1,1]
        indice_roboAdversario = [10,10,10]

        errinho = 0

        for i in range(0,3):
            try:
                XAdversario[i] = ((imagem.centroids[5][0][i][0])*170/640)
                YAdversario[i] = ((480 - imagem.centroids[5][0][i][1])*130/480)
                indice_roboAdversario[i] = i
                if self.valores_atrasados[i][0] != XAdversario[i]:
                    self.valores_atrasados[i][0] = XAdversario[i]
                    self.valores_atrasados[i][1] = YAdversario[i]
            except IndexError:
                #print('Um adversário foi perdido, usando últimos valores')
                XAdversario[i] = self.valores_atrasados[i][0]
                YAdversario[i] = self.valores_atrasados[i][1]
                errinho =+ 1
                print('Robô perdido:', i)
                pass

        #Entity_Enemie(x = XAdversario[l], y = YAdversario[l], index = indice_roboAdversario)
        
            """
            try:
                for k in range(0,3):
                    diff_Total[k] = XAdversario[j] - self.valores_atrasados[k][0] + YAdversario[j] - self.valores_atrasados[k][0]
                    if maior < abs(diff_Total[k]):
                        maior = abs(diff_Total[k])
                        roboperdido = k
                    XAdversario.append(self.valores_atrasados[roboperdido][0])
                    YAdversario.append(self.valores_atrasados[roboperdido][1])
            except IndexError:
                pass
            except ValueError:
                pass
            """

        Robo0Adversario = Entity_Enemie(index = 0)
        Robo1Adversario = Entity_Enemie(index = 1)
        Robo2Adversario = Entity_Enemie(index = 2)

        Entidades_Adversarias = [Robo0Adversario, Robo1Adversario, Robo2Adversario]


        for l in range(0,3):
            try:
                Entidades_Adversarias[l].x = XAdversario[l]
                Entidades_Adversarias[l].y = YAdversario[l]
            except IndexError:
                #print('Entidade adversária não atualizada')
                pass
            
        if errinho > 0:
            print('valores atrasados',self.valores_atrasados)
            print('Xadv',XAdversario)

        #mray: (Verdadeiro: Amarelo - Direito, Falso: Azul - Esquerdo) COLOCAR

        #direito = []
        #esquerdo = []

        #if mray is True:
        #    esquerdo.append(Entidades_Aliadas)
        #    direito.append(Entidades_Adversarias)
        #else:
        #    direito.append(Entidades_Aliadas)
        #    #esquerdo.append(Entidades_Adversarias)

        self.estado = self.jogando

        self.campo = dict(ball = Entidade_bola, our_bots = Entidades_Aliadas, their_bots = Entidades_Adversarias, Yellow = self.mray) #Ainda está dando erro
        #their_bots = Entidades_Adversarias

        #Descomentar quando terminar integracao
        self.objControle.update(self.estado, self.campo)

        self.looping = threading.Timer(0.02, self.conversao_controle)
        self.looping.start()

    def Cancel(self):
        self.close()

    def closeEvent(self,event):
        self.looping.cancel()
        event.accept()