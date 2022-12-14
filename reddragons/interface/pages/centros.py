import math

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import reddragons.utils as vutils

from ..utils import ui_files


class GUI_centro(QMainWindow):
    def __init__(self, visao, model):

        super(GUI_centro, self).__init__()
        loadUi(f"{ui_files}/centros.ui", self)
        self.show()
        self.visao = visao
        self.model = model
        self.dados = self.model.dados.copy()

        self.getReferencia()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mudanca)
        self.timer.start(1)

        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_btSalvar.clicked.connect(self.finalizar)

    def closeEvent(self, event):
        """fecha o evento/página

        Args:
            event (qtEvent): evento/página a ser fechado
        """
        self.timer.stop()
        event.accept()

    def getReferencia(self):
        """ carrega a referência de onde se encontra o centro
        """
        self.referencia = self.model.imagem.imagem_crop
        self.centroids = self.model.imagem.centroids
        self.desenhar()

    def mudanca(self):
        """muda o desenho da angulação do robô
        """
        self.dados.ang_corr = self.QT_angCorr.value() / 180.0 * math.pi
        self.value_ang.setText("{0:.2f}º".format(self.dados.ang_corr * 180 / math.pi))
        self.getReferencia()

    def finalizar(self):
        """ finaliza as mudanças
        """
        self.model.dados = self.dados

    def desenhar(self):
        """desenha os centros dos robôs
        """
        centros = vutils.calcula_centros(self.centroids, self.dados.ang_corr)

        img = self.referencia.copy()
        cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p in zip(cores, centros):
            cv2.circle(img, (int(p[0]), int(p[1])), 25, c, 1)
            cv2.line(
                img,
                (int(p[0]), int(p[1])),
                (int(p[0] + math.cos(p[2]) * 50.0), int(p[1] + math.sin(p[2]) * 50.0)),
                c,
                3,
            )
            cv2.line(
                img,
                (int(p[0]), int(p[1])),
                (
                    int(p[0] + math.cos(self.dados.ang_corr) * 50.0),
                    int(p[1] + math.sin(self.dados.ang_corr) * 50.0),
                ),
                c,
                1,
            )
        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_Imagem.setPixmap(_q_pixmap)
