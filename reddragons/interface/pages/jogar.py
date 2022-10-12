from dataclasses import field
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
import reddragons.utils as vutils

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

        self.jogando = False

        self.btJogar.clicked.connect(self.ativa_serial)
        self.btJogar.clicked.connect(self.conversao_controle)
        self.rJogar.clicked.connect(self.muda_btnJogar)
        self.rParar.clicked.connect(self.muda_btnParar)

        self.esq_radio.toggled.connect(self.mudancalados)
        self.dir_radio.toggled.connect(self.mudancalados)
    
    def mudancalados(self):
        mray = True
        mray = True if self.dir_radio.isChecked() else False
        mray = False if self.esq_radio.isChecked() else True
        if mray is False:
            self.esq_radio.setChecked(True)
        return mray
            
    
    def inicializarValores(self):
        self.esq_radio.setChecked(self.trocouCampo)
        
    def muda_btnJogar(self):
        game_on = True
        self.jogando = game_on
    
    def muda_btnParar(self):
        game_on = False
        self.jogando = game_on

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

        if self.jogando:
            # Descomentar quando o controle estiver funcional
            #dados_controle = enviarInfo.InicializaControle(dados_controle)
            self.model.controle = dados_controle

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
        
        imagem = self.model.imagem
        dados = self.model.dados.copy()
        


        pos_bola = []
        pos_bola.append(imagem.centroids[0][0][0][0])
        pos_bola.append(imagem.centroids[0][0][0][1])
        #print(pos_bola)
        #print(pos_bola[1])


        XAliado = []
        YAliado = []
        aAliado = []
        indice_roboAliado = []
        #x, y e angulo do robo

        for i in range(0, 3):
            XAliado.append(imagem.centros[i][0])

        for j in range(0,3):
            YAliado.append(480 - imagem.centros[j][1])

        for k in range(0,3):
            #calcular ângulo com uso dos centroids
            CateX = int(YAliado[k] + math.cos(imagem.centros[k][2]) * 50)
            CateY = int(XAliado[k] + math.sin(imagem.centros[k][2]) * 50)
            angulo = math.atan(CateY/CateX)*(180/np.pi)
            aAliado.append(angulo)

        for n in range(0,3):
            indice_roboAliado.append(n)

        print('centroides:',imagem.centros)
        print('X aliados:', XAliado, 'Y aliados:', YAliado)
        

        for l in range(0,3):
            Entity_Allie(x = XAliado[l], y = YAliado[l], a = aAliado[l], index = indice_roboAliado[l])
        

        XAdversario = []
        YAdversario = []

        for i in range(0,3):
            XAdversario.append(imagem.centroids[5][0][i][0])
        for j in range(0,3):
            YAdversario.append(imagem.centroids[5][0][j][1])
        for n in range(0,3):
            indice_roboAdversario = n

        for l in range(0,3):
            Entity_Enemie(x = XAdversario[l], y = YAdversario[l], index = indice_roboAdversario)



        Robo0Aliado = Entity_Allie(index = 0)
        Robo1Aliado = Entity_Allie(index = 1)
        Robo2Aliado = Entity_Allie(index = 2)

        
        Entidades_Aliadas = [Robo0Aliado, Robo1Aliado, Robo2Aliado]

        Robo0Adversario = Entity_Enemie(index = 0)
        Robo1Adversario = Entity_Enemie(index = 1)
        Robo2Adversario = Entity_Enemie(index = 2)

        Entidades_Adversarias = [Robo0Adversario, Robo1Adversario, Robo2Adversario]
        
        #mray: (Verdadeiro: Amarelo - Direito, Falso: Azul - Esquerdo) COLOCAR

        mray = self.mudancalados()
        
        #direito = []
        #esquerdo = []

        #if mray is True:
        #    esquerdo.append(Entidades_Aliadas)
        #    direito.append(Entidades_Adversarias)
        #else:
        #    direito.append(Entidades_Aliadas)
        #    #esquerdo.append(Entidades_Adversarias)#
        

        lado = dict(direito = mray)
        

        estado = self.jogando

        campo = dict(ball = pos_bola, our_bots = Entidades_Aliadas, their_bots = Entidades_Adversarias) #Ainda está dando erro
        print(campo)
        #their_bots = Entidades_Adversarias 

        #Descomentar quando terminar integracao
        #ControleEstrategia.update(None, estado, campo)
