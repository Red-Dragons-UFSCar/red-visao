import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_corte(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_corte, self).__init__()
        loadUi(f"{ui_files}/corte.ui", self)
        self.show()
        self.model = model
        self.visao = visao
        self.dados = self.model.dados

        self.get_referencia()

        self.QT_btReferencia.clicked.connect(self.get_referencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)

    def get_referencia(self):

        self.referencia = self.model.imagem.imagem_warp
        self.desenhar()

    def finalizar(self):

        self.model.dados = self.dados
        self.visao.recalcular()

    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()

        if (x < self.QT_Imagem.geometry().width()) and (
            y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0
        ):
            self.dados.corte[self.QT_posicao.currentIndex()] = [x, y]
            self.desenhar()

    def desenhar(self):
        img = self.referencia.copy()

        for ponto in self.dados.corte:
            cv2.drawMarker(img, (ponto[0], ponto[1]), (0, 255, 0))

        img[0 : self.dados.corte[0][1], 0 : self.dados.corte[0][0], :] = 0
        img[0 : self.dados.corte[1][1], self.dados.corte[1][0] : 640, :] = 0
        img[self.dados.corte[2][1] : 480, 0 : self.dados.corte[2][0], :] = 0
        img[self.dados.corte[3][1] : 480, self.dados.corte[3][0] : 640, :] = 0

        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_Imagem.setPixmap(_q_pixmap)
