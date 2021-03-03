from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi

import cv2

class GUI_cruzetas(QMainWindow):
    def    __init__(self, visao):
        super(GUI_cruzetas, self).__init__()
        loadUi(f'{ui_files}/cruzetas.ui', self)
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
    
    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()
        
        if (x < self.QT_Imagem.geometry().width()) and (y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0):
            self.dados.cruzetas[self.QT_posicao.currentIndex()] = [x, y]
            self.desenhar()
            
    def desenhar(self):
        img = self.referencia.copy()
        
        for ponto in self.dados.cruzetas:
            cv2.drawMarker(img, (ponto[0], ponto[1]), (255,0,0))
            
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Imagem.setPixmap(_qPixmap) 
