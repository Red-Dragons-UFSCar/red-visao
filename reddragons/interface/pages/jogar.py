import math

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from reddragons.visao import Logger

from ..utils import ui_files


class GUI_jogar(QMainWindow):
    def __init__(self, visao):
        super(GUI_jogar, self).__init__()
        loadUi(f"{ui_files}/jogar.ui", self)
        self.show()
        self.visao = visao
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

        self.jogando = False
        self.rJogar.setChecked(True)
        self.btJogar.clicked.connect(self.ativa_serial)
        self.rJogar.toggled.connect(self.mudanca)
        self.rParar.toggled.connect(self.mudanca)
        self.rPosInicial.toggled.connect(self.mudanca)

    def update_frame(self):

        imagem = self.visao.read_imagem()
        dados_controle = self.visao.sincronizar_controle_dinamico()

        img = imagem.imagem_crop
        cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p, a in zip(cores, imagem.centros, dados_controle.angulo_d):
            cv2.circle(img, (int(p[0]), int(p[1])), 20, c, 1)
            cv2.line(
                img,
                (int(p[0]), int(p[1])),
                (int(p[0] + math.cos(p[2]) * 25), int(p[1] + math.sin(p[2]) * 25)),
                c,
                3,
            )  # Angulo Robo
            # cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(Dados.ang_corr)*50), int(p[1]+ math.sin(Dados.ang_corr)*50)), c, 1)
            cv2.line(
                img,
                (int(p[0]), int(p[1])),
                (int(p[0] + math.cos(a) * 25), int(p[1] + math.sin(a) * 25)),
                (255, 255, 0),
                1,
            )  # Angulo controle

        cores = [(55, 55, 55), (10, 10, 10), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p in zip(cores, imagem.centroids):
            for _p in p[0]:
                cv2.circle(img, (int(_p[0]), int(_p[1])), 4, c, -1)
        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_jogar.setPixmap(_q_pixmap)

        if self.jogando:
            # Descomentar quando o controle estiver funcional
            # dados_controle = enviarInfo.InicializaControle(dados_controle)
            self.visao.set_dados_controle(dados_controle)

    def ativa_serial(self):

        dados_controle = self.visao.read_dados_controle()
        if self.jogando:
            self.jogando = False
            self.btJogar.setText("Iniciar transmissao")
            self.btJogar.setStyleSheet("background-color:green")
            dados_controle.ser = 0
        else:
            try:
                # Descomentar quando em jogo
                # dados_controle.ser = serial.Serial(dados_controle.porta,dados_controle.velocidade)
                self.jogando = True
                self.btJogar.setText("Terminar transmissao")
                self.btJogar.setStyleSheet("background-color:red")
            except:
                Logger().erro("Porta não encontrada")
                self.jogando = False
                self.btJogar.setText("Iniciar transmissao")
                self.btJogar.setStyleSheet("background-color:green")
                dados_controle.ser = 0

        self.visao.set_dados_controle(dados_controle)

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

    def mudanca(self):

        dados_controle = self.visao.sincronizar_controle_dinamico()

        dados_controle.Pjogar = True if self.rJogar.isChecked() else False
        dados_controle.Pparar = True if self.rParar.isChecked() else False
        dados_controle.Pinicial = True if self.rPosInicial.isChecked() else False

        self.visao.set_dados_controle(dados_controle)
