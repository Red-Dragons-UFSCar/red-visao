from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi

import cv2
from enum import Enum

from estruturas import *
from logger import *
import math

class Estado(Enum):
    ORIGINAL = 0
    PERSPECTIVA = 1
    CORTE = 2
    CRUZ = 3
    CENTROIDS = 4
    ROBOS = 5

class GUI_visualizacao(QMainWindow):
    def __init__(self, visao):
        super(GUI_visualizacao, self).__init__()
        loadUi(f'{ui_files}/visualizacao.ui', self)
        self.show()
        self.visao = visao
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1)
        
    def closeEvent(self, event):
    	self.timer.stop()
    	event.accept()
        
    def updateFrame(self):
        estado = self.qt_tipoVisualizacao.currentIndex()
        
        
        Imagem = self.visao.read_Imagem()
        Dados = self.visao.read_Dados()
        
        if estado == Estado.ORIGINAL.value:
            img = Imagem.imagem_original
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.PERSPECTIVA.value:
            img = Imagem.imagem_warp
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.CORTE.value:
            img = Imagem.imagem_crop
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.CRUZ.value:
            img = Imagem.imagem_crop
            for ponto in Dados.cruzetas:
                cv2.drawMarker(img, (ponto[0], ponto[1]), (255,0,0))
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.CENTROIDS.value:
            img = Imagem.imagem_crop
            C = [(55, 55, 55), (200, 200, 200), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
            for c, p in zip(C, Imagem.centroids):
                for _p in p[0]:
                    cv2.circle(img, (int(_p[0]), int(_p[1])), 8, c, -1)
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.ROBOS.value:
            img = Imagem.imagem_crop
            C = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
            for c, p in zip(C, Imagem.centros):
                cv2.circle(img, (int(p[0]), int(p[1])), 25, c, 1)
                cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(p[2])*50), int(p[1]+ math.sin(p[2])*50)), c, 3)
                cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(Dados.angCorr)*50), int(p[1]+ math.sin(Dados.angCorr)*50)), c, 1)
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)