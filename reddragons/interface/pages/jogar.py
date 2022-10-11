from dataclasses import field
import math
from operator import index

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from reddragons.estruturas.models.imagem import Imagem
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

        pos_bola = []
        pos_bola.append(imagem.centroids[0])

        XAliado = []
        YAliado = []

        for i in range(0, 2):
            XAliado.append(imagem.centros[i][0])
            for j in range(0,2):
                YAliado.append(imagem.centros[j][0])     
                for n in range(0,2):
                    indice_roboAliado = n
                    Entity_Allie(x = XAliado[i], y = YAliado[j], index = indice_roboAliado)

        #XAdversario = []
        #YAdversario = []

        #for i in range(0,2):
        #    XAdversario.append(imagem.adversarios[i][0])
        #    for j in range(0,2):
        #        YAdversario.append(imagem.adversarios[j][1])
        #        for n in range(0,2):
        #            indice_roboAdversario = n
        #            Entity_Enemie(x = XAdversario[i], y = YAdversario[j], index = indice_roboAdversario)



        Robo0Aliado = Entity_Allie(index = 0)
        Robo1Aliado = Entity_Allie(index = 1)
        Robo2Aliado = Entity_Allie(index = 2)

        
        Entidades_Aliadas = [Robo0Aliado, Robo1Aliado, Robo2Aliado]

        #Robo0Adversario = Entity_Enemie(index = 0)
        #Robo1Adversario = Entity_Enemie(index = 1)
        #Robo2Adversario = Entity_Enemie(index = 2)

        #Entidades_Adversarias = [Robo0Adversario, Robo1Adversario, Robo2Adversario]
        
        #mray: (Verdadeiro: Amarelo - Direito, Falso: Azul - Esquerdo) COLOCAR
        mray = True

        direito = []
        esquerdo = []

        if mray is True:
            esquerdo.append(Entidades_Aliadas)
            #direito.append(Entidades_Adversarias)
        else:
            direito.append(Entidades_Aliadas)
            #esquerdo.append(Entidades_Adversarias)


        lado = dict(yellow=direito, blue=esquerdo)
        

        estado = self.jogando

        campo = dict(ball = pos_bola, our_bots = Entidades_Aliadas)
        #their_bots = Entidades_Adversarias 


        #ControleEstrategia.update(None, estado, campo)
