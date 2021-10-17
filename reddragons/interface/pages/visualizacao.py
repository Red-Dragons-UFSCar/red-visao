import math
from enum import Enum

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from .main import GUI_main
from ..utils import ui_files


class Estado(Enum):
    ORIGINAL = 0
    PERSPECTIVA = 1
    CORTE = 2
    CRUZ = 3
    CENTROIDS = 4
    ROBOS = 5


class GUI_visualizacao(QMainWindow):
    def __init__(self, app):
        super(GUI_visualizacao, self).__init__()
        loadUi(f"{ui_files}/visualizacao.ui", self)
        self.show()
        self.app = app
        self.model = app.model
        self.visao = app.visao
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)
        self.btnVoltar.clicked.connect(self.app.back)
        self.btnMenu.clicked.connect(self.push_menu)


    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

    def push_menu (self):
        self.app.push_widget(GUI_main(self.app))
    def update_frame(self):
        estado = self.qt_tipoVisualizacao.currentIndex()

        imagem = self.model.imagem
        dados = self.model.dados

        if estado == Estado.ORIGINAL.value:
            img = imagem.imagem_original
            _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _q_pixmap = QPixmap.fromImage(_q_image)
            self.QT_visualizacao.setPixmap(_q_pixmap)

        if estado == Estado.PERSPECTIVA.value:
            img = imagem.imagem_warp
            _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _q_pixmap = QPixmap.fromImage(_q_image)
            self.QT_visualizacao.setPixmap(_q_pixmap)

        if estado == Estado.CORTE.value:
            img = imagem.imagem_crop
            _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _q_pixmap = QPixmap.fromImage(_q_image)
            self.QT_visualizacao.setPixmap(_q_pixmap)

        if estado == Estado.CRUZ.value:
            img = imagem.imagem_crop
            for ponto in dados.cruzetas:
                cv2.drawMarker(img, (ponto[0], ponto[1]), (255, 0, 0))
            _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _q_pixmap = QPixmap.fromImage(_q_image)
            self.QT_visualizacao.setPixmap(_q_pixmap)

        if estado == Estado.CENTROIDS.value:
            img = imagem.imagem_crop
            cores = [
                (55, 55, 55),
                (200, 200, 200),
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
            ]
            for c, p in zip(cores, imagem.centroids):
                for _p in p[0]:
                    cv2.circle(img, (int(_p[0]), int(_p[1])), 8, c, -1)
            _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _q_pixmap = QPixmap.fromImage(_q_image)
            self.QT_visualizacao.setPixmap(_q_pixmap)

        if estado == Estado.ROBOS.value:
            img = imagem.imagem_crop
            cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
            for c, p in zip(cores, imagem.centros):
                cv2.circle(img, (int(p[0]), int(p[1])), 25, c, 1)
                cv2.line(
                    img,
                    (int(p[0]), int(p[1])),
                    (int(p[0] + math.cos(p[2]) * 50), int(p[1] + math.sin(p[2]) * 50)),
                    c,
                    3,
                )
                cv2.line(
                    img,
                    (int(p[0]), int(p[1])),
                    (
                        int(p[0] + math.cos(dados.ang_corr) * 50),
                        int(p[1] + math.sin(dados.ang_corr) * 50),
                    ),
                    c,
                    1,
                )
            _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _q_pixmap = QPixmap.fromImage(_q_image)
            self.QT_visualizacao.setPixmap(_q_pixmap)
