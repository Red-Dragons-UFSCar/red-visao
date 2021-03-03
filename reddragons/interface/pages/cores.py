import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from reddragons.visao import utils as vutils

from ..utils import ui_files


class GUI_cores(QMainWindow):
    def __init__(self, visao):
        super(GUI_cores, self).__init__()
        loadUi(f"{ui_files}/cores.ui", self)
        self.show()
        self.visao = visao
        self.centroids = np.empty([0, 3])

        self.dados = self.visao.read_dados()

        self.QT_AreaMax.setValue(self.dados.area_maxima)
        self.QT_AreaMin.setValue(self.dados.area_minima)

        self.get_referencia()
        self.QT_btReferencia.clicked.connect(self.get_referencia)
        self.QT_btSalvar.clicked.connect(self.salvar)
        self.QT_HMin.sliderMoved.connect(self.mudanca)
        self.QT_HMax.sliderMoved.connect(self.mudanca)
        self.QT_SMin.sliderMoved.connect(self.mudanca)
        self.QT_SMax.sliderMoved.connect(self.mudanca)
        self.QT_VMin.sliderMoved.connect(self.mudanca)
        self.QT_VMax.sliderMoved.connect(self.mudanca)
        self.QT_valorKernel.sliderMoved.connect(self.mudanca)
        self.QT_qualKernel.currentIndexChanged.connect(self.mudanca)
        self.QT_tipoKernel.currentIndexChanged.connect(self.mudanca)
        self.QT_AreaMax.sliderMoved.connect(self.mudanca)
        self.QT_AreaMin.sliderMoved.connect(self.mudanca)
        self.QT_selecao.currentIndexChanged.connect(self.nova_cor)
        self.QT_fatorClique.sliderMoved.connect(self.fator_filtro)
        self.QT_fatorCor.sliderMoved.connect(self.fator_filtro)

        self.fator_filtro()

        self.setMouseTracking(True)

        self.mask = None
        self.nova_cor()

    def get_referencia(self):

        self.referencia = self.visao.read_imagem().imagem_crop
        self.imagem_hsv = self.visao.read_imagem().imagem_hsv
        self.dados = self.visao.read_dados()
        self.contornos, _ = vutils.get_contorno_cor(
            self.imagem_hsv, self.dados.cores[0], self.dados.filtros[0]
        )
        self.desenhar()

    def salvar(self):
        i = self.QT_selecao.currentIndex()
        self.dados.cores[i] = [
            [self.QT_HMin.value(), self.QT_SMin.value(), self.QT_VMin.value()],
            [self.QT_HMax.value(), self.QT_SMax.value(), self.QT_VMax.value()],
        ]
        self.dados.filtros[i] = [
            int(self.QT_qualKernel.currentIndex()),
            int(self.QT_tipoKernel.currentIndex()),
            self.QT_valorKernel.value(),
        ]

        self.dados.area_minima = self.QT_AreaMin.value()
        self.dados.area_maxima = self.QT_AreaMax.value()

        self.visao.set_dados(self.dados)

    def nova_cor(self):
        i = self.QT_selecao.currentIndex()
        self.contornos, _ = vutils.get_contorno_cor(
            self.imagem_hsv, self.dados.cores[i], self.dados.filtros[i]
        )

        cores = self.dados.cores[i]
        filtros = self.dados.filtros[i]

        self.QT_HMin.setValue(cores[0][0])
        self.QT_HMax.setValue(cores[1][0])

        self.QT_SMin.setValue(cores[0][1])
        self.QT_SMax.setValue(cores[1][1])

        self.QT_VMin.setValue(cores[0][2])
        self.QT_VMax.setValue(cores[1][2])

        self.QT_qualKernel.setCurrentIndex(filtros[0])
        self.QT_valorKernel.setValue(filtros[2])
        self.QT_tipoKernel.setCurrentIndex(filtros[1])

        self.desenhar()

    def fator_filtro(self):
        self.fator_clique = self.QT_fatorClique.value()
        self.fator_cor = self.QT_fatorCor.value()

    def mudanca(self):
        i = self.QT_selecao.currentIndex()

        self.dados.cores[i] = [
            [self.QT_HMin.value(), self.QT_SMin.value(), self.QT_VMin.value()],
            [self.QT_HMax.value(), self.QT_SMax.value(), self.QT_VMax.value()],
        ]
        self.dados.filtros[i] = [
            int(self.QT_qualKernel.currentIndex()),
            int(self.QT_tipoKernel.currentIndex()),
            self.QT_valorKernel.value(),
        ]

        self.contornos, _ = vutils.get_contorno_cor(
            cv2.cvtColor(np.uint8(self.referencia), cv2.COLOR_RGB2HSV),
            self.dados.cores[i],
            self.dados.filtros[i],
        )

        self.centroids = np.empty([0, 3])
        for c in self.contornos:
            moments = cv2.moments(c)
            if (moments["m00"] >= self.QT_AreaMin.value()) and (
                moments["m00"] <= self.QT_AreaMax.value()
            ):
                c_x = int(moments["m10"] / moments["m00"])
                c_y = int(moments["m01"] / moments["m00"])
                self.centroids = np.append(
                    self.centroids, [[c_x, c_y, moments["m00"]]], axis=0
                )

        self.desenhar()

    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()

        if (x < self.QT_Imagem.geometry().width()) and (
            y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0
        ):
            # Logger().variavel("Cor no ponto ({0}, {1})".format(x,y), "RGB {0} HSV {1}".format(self.referencia[y, x], self.imagem_hsv[y, x]))
            if (
                y > self.fator_clique
                and x > self.fator_clique
                and x < 640 - self.fator_clique
                and y < 480 - self.fator_clique
            ):
                h_max = max(
                    self.imagem_hsv[y, x - self.fator_clique][0],
                    self.imagem_hsv[y - self.fator_clique, x][0],
                    self.imagem_hsv[y, x][0],
                    self.imagem_hsv[y, x + self.fator_clique][0],
                    self.imagem_hsv[y + self.fator_clique, x][0],
                )
                h_min = min(
                    self.imagem_hsv[y, x - self.fator_clique][0],
                    self.imagem_hsv[y - self.fator_clique, x][0],
                    self.imagem_hsv[y, x][0],
                    self.imagem_hsv[y, x + self.fator_clique][0],
                    self.imagem_hsv[y + self.fator_clique, x][0],
                )
                self.QT_HMin.setValue(max(0, h_min - self.fator_cor))
                self.QT_HMax.setValue(min(179, h_max + self.fator_cor))

                s_max = max(
                    self.imagem_hsv[y, x - self.fator_clique][1],
                    self.imagem_hsv[y - self.fator_clique, x][1],
                    self.imagem_hsv[y, x][1],
                    self.imagem_hsv[y, x + self.fator_clique][1],
                    self.imagem_hsv[y + self.fator_clique, x][1],
                )
                s_min = min(
                    self.imagem_hsv[y, x - self.fator_clique][1],
                    self.imagem_hsv[y - self.fator_clique, x][1],
                    self.imagem_hsv[y, x][1],
                    self.imagem_hsv[y, x + self.fator_clique][1],
                    self.imagem_hsv[y + self.fator_clique, x][1],
                )
                self.QT_SMin.setValue(max(0, s_min - self.fator_cor))
                self.QT_SMax.setValue(min(255, s_max + self.fator_cor))

                v_max = max(
                    self.imagem_hsv[y, x - self.fator_clique][2],
                    self.imagem_hsv[y - self.fator_clique, x][2],
                    self.imagem_hsv[y, x][2],
                    self.imagem_hsv[y, x + self.fator_clique][2],
                    self.imagem_hsv[y + self.fator_clique, x][2],
                )
                v_min = min(
                    self.imagem_hsv[y, x - self.fator_clique][2],
                    self.imagem_hsv[y - self.fator_clique, x][2],
                    self.imagem_hsv[y, x][2],
                    self.imagem_hsv[y, x + self.fator_clique][2],
                    self.imagem_hsv[y + self.fator_clique, x][2],
                )
                self.QT_VMin.setValue(max(0, v_min - self.fator_cor))
                self.QT_VMax.setValue(min(255, v_max + self.fator_cor))
            else:
                h, s, v = self.imagem_hsv[y, x]
                self.QT_HMin.setValue(max(0, h - self.fator_cor))
                self.QT_HMax.setValue(min(179, h + self.fator_cor))
                self.QT_SMin.setValue(max(0, s - self.fator_cor))
                self.QT_SMax.setValue(min(255, s + self.fator_cor))
                self.QT_VMin.setValue(max(0, v - self.fator_cor))
                self.QT_VMax.setValue(min(255, v + self.fator_cor))

            self.mudanca()

    def desenhar(self):
        img = self.referencia.copy()
        img2 = self.referencia.copy()

        img = cv2.drawContours(img2, self.contornos, -1, (255, 0, 0), 1)
        # img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_Imagem.setPixmap(_q_pixmap)

        img = cv2.drawContours(
            np.zeros((img2.shape[0], img2.shape[1], 3), np.uint8),
            self.contornos,
            -1,
            (255, 0, 0),
            -1,
        )
        img = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))
        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_PB.setPixmap(_q_pixmap)

        img = self.referencia.copy()
        img = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))
        for c in self.centroids:
            cv2.circle(img, (int(c[0] / 2), int(c[1] / 2)), 5, (255, 0, 0), -1)
        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_Contorno.setPixmap(_q_pixmap)
