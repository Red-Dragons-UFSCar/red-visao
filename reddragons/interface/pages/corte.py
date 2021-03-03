from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi
import cv2
from estruturas import *
from logger import *

class GUI_corte(QMainWindow):
    def __init__(self, visao):
        super(GUI_corte, self).__init__()
        loadUi(f'{ui_files}/corte.ui', self)
        self.show()    
        self.visao = visao
        self.dados = self.visao.read_Dados()
        
        self.getReferencia()
        
        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)
        
    def getReferencia(self):
        
        self.referencia = self.visao.read_Imagem().imagem_warp
        self.desenhar()
        
    def finalizar(self):
        
        self.visao.set_Dados(self.dados)
        self.visao.recalcular()
        
    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()
        
        if (x < self.QT_Imagem.geometry().width()) and (y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0):
            self.dados.corte[self.QT_posicao.currentIndex()] = [x, y]
            self.desenhar()
            
    def desenhar(self):
        img = self.referencia.copy()
        
        for ponto in self.dados.corte:
            cv2.drawMarker(img, (ponto[0], ponto[1]), (0,255,0))
            
        img[0:self.dados.corte[0][1], 0:self.dados.corte[0][0], :] = 0
        img[0:self.dados.corte[1][1], self.dados.corte[1][0]:640, :] = 0
        img[self.dados.corte[2][1]:480, 0:self.dados.corte[2][0], :] = 0
        img[self.dados.corte[3][1]:480, self.dados.corte[3][0]:640, :] = 0
            
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Imagem.setPixmap(_qPixmap) 