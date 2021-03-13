from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_controle(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_controle, self).__init__()
        loadUi(f"{ui_files}/controle.ui", self)
        self.show()
        self.visao = visao
        self.model = model
        self.inicializarValores()

        self.lineKd1.textChanged.connect(self.mudanca)
        self.lineKp1.textChanged.connect(self.mudanca)
        self.lineKi1.textChanged.connect(self.mudanca)
        self.lineKd2.textChanged.connect(self.mudanca)
        self.lineKp2.textChanged.connect(self.mudanca)
        self.lineKi2.textChanged.connect(self.mudanca)
        self.lineKd3.textChanged.connect(self.mudanca)
        self.lineKp3.textChanged.connect(self.mudanca)
        self.lineKi3.textChanged.connect(self.mudanca)
        self.porta_value.textChanged.connect(self.mudanca)
        self.esq_radio.toggled.connect(self.mudanca)
        self.dir_radio.toggled.connect(self.mudanca)
        self.bolaNossa.stateChanged.connect(self.mudanca)
        self.duasFaces.stateChanged.connect(self.mudanca)
        self.kalman.stateChanged.connect(self.mudanca)
        self.simular.stateChanged.connect(self.mudanca)
        self.alvoFixo.stateChanged.connect(self.mudanca)

        self.visao.sincronizar_controle()

    def mudanca(self):

        dados_controle = self.visao.sincronizar_controle()

        dados_controle.Kp1 = self.lineKp1.text()
        dados_controle.Kd1 = self.lineKd1.text()
        dados_controle.Ki1 = self.lineKi1.text()
        dados_controle.Kp2 = self.lineKp2.text()
        dados_controle.Kd2 = self.lineKd2.text()
        dados_controle.Ki2 = self.lineKi2.text()
        dados_controle.Kp3 = self.lineKp3.text()
        dados_controle.Kd3 = self.lineKd3.text()
        dados_controle.Ki3 = self.lineKi3.text()
        dados_controle.porta = self.porta_value.text()
        dados_controle.trocouCampo = True if self.dir_radio.isChecked() else False
        dados_controle.bolaNossa1 = 1 if self.bolaNossa.isChecked() else 0
        dados_controle.duasFaces = True if self.duasFaces.isChecked() else False
        dados_controle.flagAtivaKalman = True if self.kalman.isChecked() else False
        dados_controle.simular = True if self.simular.isChecked() else False
        dados_controle.irParaAlvoFixo = True if self.alvoFixo.isChecked() else False

        self.model.controle = dados_controle

    def inicializarValores(self):

        dados_controle = self.visao.sincronizar_controle()

        self.lineKd1.setText(str(dados_controle.Kd1))
        self.lineKp1.setText(str(dados_controle.Kd1))
        self.lineKi1.setText(str(dados_controle.Ki1))
        self.lineKd2.setText(str(dados_controle.Kd2))
        self.lineKp2.setText(str(dados_controle.Kp2))
        self.lineKi2.setText(str(dados_controle.Ki2))
        self.lineKd3.setText(str(dados_controle.Kd3))
        self.lineKp3.setText(str(dados_controle.Kp3))
        self.lineKi3.setText(str(dados_controle.Ki3))
        self.porta_value.setText(dados_controle.porta)

        self.esq_radio.setChecked(dados_controle.trocouCampo)
        self.bolaNossa.setChecked(dados_controle.bolaNossa1)
        self.duasFaces.setChecked(dados_controle.duasFaces)
        self.kalman.setChecked(dados_controle.flagAtivaKalman)
        self.simular.setChecked(dados_controle.simular)
        self.alvoFixo.setChecked(dados_controle.irParaAlvoFixo)
