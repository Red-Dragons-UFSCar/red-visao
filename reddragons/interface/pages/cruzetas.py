import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import numpy as np
from .cores import GUI_cores
from ..utils import ui_files

def identificaCruzetas (pts):
     pts_sorted = sorted(pts, key=lambda x: x[1])
     inferior_esq = pts_sorted[2]
     superior_esq, superior_dir = sorted(pts_sorted[:2], key=lambda x: x[0])
     return [superior_esq, superior_dir, inferior_esq]

class GUI_cruzetas(QMainWindow):
    def __init__(self, app):
        super(GUI_cruzetas, self).__init__()
        loadUi(f"{ui_files}/perspectiva.ui", self)
        self.show()
        self.app = app
        self.visao = app.visao
        self.model = app.model
        self.dados = self.model.dados
        self.selecoes = list(self.dados.cruzetas)
        self.get_referencia()
        self.QT_btReferencia.clicked.connect(self.get_referencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)
        self.QT_btVoltar.clicked.connect(self.app.back)

    def get_referencia(self):

        self.referencia = self.model.imagem.imagem_warp
        self.desenhar()

    def finalizar(self):
        if len(self.selecoes) < 3:
            self.selecoes.append([0,0])
            self.finalizar()
        self.dados.cruzetas = np.asarray(identificaCruzetas(self.selecoes))
        self.model.dados = self.dados
        self._next()

    def _next (self):
        self.app.push_widget(GUI_cores(self.app))

    def mouseReleaseEvent(self, QMouseEvent):
        """
        Ponto de seleção do mouse para a cruzeta
        """
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()

        if (0 <= x < self.QT_Imagem.geometry().width()) and (
            0 <= y < self.QT_Imagem.geometry().height()
        ):
            if len(self.selecoes) == 3:
                self.selecoes.sort(key = lambda i: (x-i[0])**2 + (y-i[1])**2)
                self.selecoes[0] = [x,y]
            else:
                self.dados.cruzetas[self.QT_posicao.currentIndex()] = [x, y]
                self.selecoes.append([x,y])
            self.desenhar()

    def desenhar(self):
        img = self.referencia.copy()

        for ponto in self.selecoes:
            cv2.drawMarker(img, (ponto[0], ponto[1]), (255, 0, 0))

        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_Imagem.setPixmap(_q_pixmap)
