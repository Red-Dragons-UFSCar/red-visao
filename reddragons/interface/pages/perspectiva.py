import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from reddragons.utils import PointsParser, converte_coord

from ..utils import ui_files


class GUI_perspectiva(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_perspectiva, self).__init__()
        loadUi(f"{ui_files}/perspectiva.ui", self)
        self.show()
        self.visao = visao
        self.model = model
        self.dados = self.model.dados
        self.input_count = 0
        self.inputs = []
        self.get_referencia()

        self.QT_btReferencia.clicked.connect(self.get_referencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)

    def get_referencia(self):

        self.referencia = self.model.imagem.imagem_original
        self.desenhar()

    def finalizar(self):

        self.model.dados = self.dados
        self.visao.recalcular()
        self.close()

    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()

        if (x < self.QT_Imagem.geometry().width()) and (
            y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0
        ):
            if self.input_count <= 8:
                self.input_count += 1
                self.inputs.append((x, y))
                self.desenhar()
                if self.input_count == 8:
                    parser = PointsParser(self.inputs)
                    pts = parser.run()
                    self.dados.warp_perspective = pts["externos"]
                    self.finalizar()
                    self.dados.corte = [
                        converte_coord(
                            self.model.dados.matriz_warp_perspective, p
                        )
                        for p in pts["internos"]
                    ]

    def desenhar(self):
        img = self.referencia.copy()

        for ponto in self.inputs:
            cv2.circle(img, (ponto[0], ponto[1]), 6, (205, 0, 0), -1)

        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_Imagem.setPixmap(_q_pixmap)
