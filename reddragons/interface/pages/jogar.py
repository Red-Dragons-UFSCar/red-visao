from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi

import cv2

from estruturas import *
from logger import *
import math

class GUI_jogar(QMainWindow):
    def __init__(self, visao):
        super(GUI_jogar,self).__init__()
        loadUi(f'{ui_files}/jogar.ui',self)
        self.show()
        self.visao = visao
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1)

        self.jogando = False
        self.rJogar.setChecked(True)
        self.btJogar.clicked.connect(self.AtivaSerial)
        self.rJogar.toggled.connect(self.mudanca)
        self.rParar.toggled.connect(self.mudanca)
        self.rPosInicial.toggled.connect(self.mudanca)
        
    def updateFrame(self):
        
        Imagem = self.visao.read_Imagem()
        Dados = self.visao.read_Dados()
        DadosControle = self.visao.sincronizar_Controle_dinamico()

        img = Imagem.imagem_crop
        C = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p,a in zip(C, Imagem.centros,DadosControle.angulo_d):
            cv2.circle(img, (int(p[0]), int(p[1])), 20, c, 1)
            cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(p[2])*25), int(p[1]+ math.sin(p[2])*25)), c, 3) #Angulo Robo
            #cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(Dados.angCorr)*50), int(p[1]+ math.sin(Dados.angCorr)*50)), c, 1)
            cv2.line(img,(int(p[0]),int(p[1])),(int(p[0]+math.cos(a)*25),int(p[1]+math.sin(a)*25)),(255,255,0),1) #Angulo controle

        C = [(55, 55, 55), (10, 10, 10), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p in zip(C, Imagem.centroids):
            for _p in p[0]:
                cv2.circle(img, (int(_p[0]), int(_p[1])), 4, c, -1)
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_jogar.setPixmap(_qPixmap)



        if self.jogando:
            #Descomentar quando o controle estiver funcional
            #DadosControle = enviarInfo.InicializaControle(DadosControle)
            self.visao.set_DadosControle(DadosControle)
    
    def AtivaSerial(self):          
        
        DadosControle = self.visao.read_DadosControle()
        if self.jogando:
                self.jogando = False
                self.btJogar.setText('Iniciar transmissao')
                self.btJogar.setStyleSheet("background-color:green")
                DadosControle.ser = 0
        else:
            try:
                #Descomentar quando em jogo
                #DadosControle.ser = serial.Serial(DadosControle.porta,DadosControle.velocidade)
                self.jogando = True
                self.btJogar.setText('Terminar transmissao')
                self.btJogar.setStyleSheet("background-color:red")
            except:
                logger().erro('Porta não encontrada')
                self.jogando = False
                self.btJogar.setText('Iniciar transmissao')
                self.btJogar.setStyleSheet("background-color:green")
                DadosControle.ser = 0

        self.visao.set_DadosControle(DadosControle)
        
    def closeEvent(self, event):
    	self.timer.stop()
    	event.accept()

    def mudanca(self):
        
        DadosControle = self.visao.sincronizar_Controle_dinamico()
 
        DadosControle.Pjogar = True if self.rJogar.isChecked() else False
        DadosControle.Pparar = True if self.rParar.isChecked() else False
        DadosControle.Pinicial = True if self.rPosInicial.isChecked() else False
            
        self.visao.set_DadosControle(DadosControle)