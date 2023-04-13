me explique o funcionameto do condigo a seguir:

import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from .cruzetas import GUI_cruzetas
from reddragons.utils import PointsParser, converte_coord

from ..utils import ui_files

#Esse código muda a interface do programa para quando a perspectiva do campo é alterada


class GUI_perspectiva(QMainWindow):

    # A parte a seguir basicamente referencia um arquivo .ui que configura o que será mostrado ao usuario
    def __init__(self, app):
        super(GUI_perspectiva, self).__init__()
        loadUi(f"{ui_files}/perspectiva.ui", self) #Nessa linha é referenciado o arquivo .ui
        self.show()
        self.app = app
        self.visao = app.visao
        self.model = app.model
        self.dados = self.model.dados
        self.inputs = []
        self.get_referencia()

        self.QT_btReferencia.clicked.connect(self.get_referencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)
        self.QT_btVoltar.clicked.connect(self.app.back)

    # A parte a seguir pega a imagem do jogo e mostra no programa ao chamar a funcao desenhar
    def get_referencia(self):

        self.referencia = self.model.imagem.imagem_original
        self.desenhar()

    # Passa para a configuração das cruzetas
    def _next (self):
        self.app.push_widget(GUI_cruzetas(self.app))

    # Pega as cordenadas do mouse para realizar a transformação e chama a funcão _next
    def finalizar(self):
        if len(self.inputs) == 8:
            parser = PointsParser(self.inputs)
            pts = parser.run()
            self.dados.warp_perspective = pts["externos"]
            self.visao.recalcular()
            self.dados.corte = [
                converte_coord(
                    self.model.dados.matriz_warp_perspective, p
                )
                for p in pts["internos"]
            ]
        self.model.dados = self.dados
        self._next()

    # Reinicia o que o usuario fez
    def _undo (self):
        if len(self.inputs) == 0:
            return
        self.inputs.pop()
        self.desenhar()

    # Reinicia o que o usuario fez por meio do ctrl + z
    def keyPressEvent(self, event):
        if event.key() == (Qt.Key_Control and Qt.Key_Z):
            self._undo()

    # Quando o usuario clica na imagem do jogo essa parte pega as cordenadas do mouse
    # e desenha um circulo nela
    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()

        if (x < self.QT_Imagem.geometry().width()) and (
            y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0
        ):
            if len(self.inputs) <= 8:
                self.inputs.append((x, y))
                self.desenhar()

    # Essa funcao atualiza a imagem do jogo na tela. é chamada pelos botoes 'Referencia', 'Finalizar' ou usando ctrl + z
    def desenhar(self):
        img = self.referencia.copy()

        for ponto in self.inputs:
            cv2.circle(img, (ponto[0], ponto[1]), 6, (205, 0, 0), -1)

        _q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _q_pixmap = QPixmap.fromImage(_q_image)
        self.QT_Imagem.setPixmap(_q_pixmap)
