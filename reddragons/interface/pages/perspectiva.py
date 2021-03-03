from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi

from utils import PointsParser, converte_coord
import cv2

from estruturas import *
from logger import *

class GUI_perspectiva(QMainWindow):
    def __init__(self, visao):
        super(GUI_perspectiva, self).__init__()
        loadUi(f'{ui_files}/perspectiva.ui', self)
        self.show()    
        self.visao = visao
        self.dados = self.visao.read_Dados()
        self.inputCount = 0
        self.inputs = []
        self.getReferencia()
        
        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)
        
    def getReferencia(self):
        
        self.referencia = self.visao.read_Imagem().imagem_original
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
            if (self.inputCount <= 8):
                self.inputCount+=1
                self.inputs.append((x,y))
                self.desenhar()
                if(self.inputCount == 8):
                    parser = PointsParser(self.inputs)
                    pts = parser.run()
                    self.dados.warpPerspective = pts['externos']
                    self.finalizar()
                    self.dados.corte = [
                        converte_coord(self.visao.read_Dados().M_warpPerspective, p) for p in pts['internos']
                    ]
            
    def desenhar(self):
        img = self.referencia.copy()
        
        for ponto in self.inputs:
            cv2.circle(img, (ponto[0], ponto[1]), 6, (205,0,0),-1)
            
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Imagem.setPixmap(_qPixmap)