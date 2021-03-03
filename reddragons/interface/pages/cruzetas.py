import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_cruzetas(QMainWindow):
    def __init__(self, visao):
        super(GUI_cruzetas, self).__init__()
        loadUi(f"{ui_files}/cruzetas.ui", self)
        self.show()
        self.visao = visao
        self.dados = self.visao.read_dados()
        self.get_referencia()
        self.QT_btReferencia.clicked.connect(self.get_referencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)

    def get_referencia(self):

        self.referencia = self.visao.read_imagem().imagem_warp
        self.desenhar()

    def finalizar(self):

        self.visao.set_dados(self.dados)

    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()

        if (x < self.QT_Imagem.geometry().width()) and (
            y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0
        ):
            self.dados.cruzetas[self.QT_posicao.currentIndex()] = [x, y]
            self.desenhar()

    def desenhar(self):
        img = self.referencia.copy()

        for ponto in self.dados.cruzetas:
            cv2.drawMarker(img, (ponto[0], ponto[1]), (255, 0, 0))

        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_Imagem.setPixmap(_q_pixmap)
