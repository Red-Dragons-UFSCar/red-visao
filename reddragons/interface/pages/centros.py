import math
import cv2
import processamento
from estruturas import *
from logger import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi

class GUI_centro(QMainWindow):
    def __init__(self, visao):
        super(GUI_centro, self).__init__()
        loadUi(f'{ui_files}/centros.ui', self)
        self.show()    
        self.visao = visao
        self.dados = self.visao.read_Dados()
        
        self.getReferencia()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mudanca)
        self.timer.start(1)
        
        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_btSalvar.clicked.connect(self.finalizar)
        
    def closeEvent(self, event):
    	self.timer.stop()
    	event.accept()
        
    def getReferencia(self):
        
        self.referencia = self.visao.read_Imagem().imagem_crop
        self.centroids = self.visao.read_Imagem().centroids
        self.desenhar()
        
    def mudanca(self):
        self.dados.angCorr = self.QT_angCorr.value()/180.0*math.pi
        self.value_ang.setText("{0:.2f}º".format(self.dados.angCorr*180/math.pi))
        self.getReferencia()
        
    def finalizar(self):
        
        self.visao.set_Dados(self.dados)
            
    def desenhar(self):
        centros = processamento.calculaCentros(self.centroids, self.dados.angCorr)
        
        img = self.referencia.copy()
        C = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p in zip(C, centros):
            cv2.circle(img, (int(p[0]), int(p[1])), 25, c, 1)
            cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(p[2])*50.0), int(p[1]+ math.sin(p[2])*50.0)), c, 3)
            cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(self.dados.angCorr)*50.0), int(p[1]+ math.sin(self.dados.angCorr)*50.0)), c, 1)
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Imagem.setPixmap(_qPixmap)
