from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi

from reddragons.visao import Logger

class GUI_controle(QMainWindow):

    def __init__(self, visao):
        super(GUI_controle,self).__init__()
        loadUi(f'{ui_files}/controle.ui',self)
        self.show()
        self.visao = visao
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

        DadosControle = self.visao.sincronizar_controle()

        DadosControle.Kp1 = self.lineKp1.text()
        DadosControle.Kd1 = self.lineKd1.text()
        DadosControle.Ki1 = self.lineKi1.text()
        DadosControle.Kp2 = self.lineKp2.text()
        DadosControle.Kd2 = self.lineKd2.text()
        DadosControle.Ki2 = self.lineKi2.text()
        DadosControle.Kp3 = self.lineKp3.text()
        DadosControle.Kd3 = self.lineKd3.text()
        DadosControle.Ki3 = self.lineKi3.text()
        DadosControle.porta = self.porta_value.text()
        DadosControle.trocouCampo = True if self.dir_radio.isChecked() else False 
        DadosControle.bolaNossa1 = 1 if self.bolaNossa.isChecked() else 0 
        DadosControle.duasFaces = True if self.duasFaces.isChecked() else False 
        DadosControle.flagAtivaKalman = True if self.kalman.isChecked() else False 
        DadosControle.simular = True if self.simular.isChecked() else False 
        DadosControle.irParaAlvoFixo = True if self.alvoFixo.isChecked() else False 

        self.visao.set_dadosControle(DadosControle)

    def inicializarValores(self):

        DadosControle = self.visao.sincronizar_controle()  

        self.lineKd1.setText(str(DadosControle.Kd1)) 
        self.lineKp1.setText(str(DadosControle.Kd1))
        self.lineKi1.setText(str(DadosControle.Ki1))
        self.lineKd2.setText(str(DadosControle.Kd2))
        self.lineKp2.setText(str(DadosControle.Kp2))
        self.lineKi2.setText(str(DadosControle.Ki2))
        self.lineKd3.setText(str(DadosControle.Kd3))
        self.lineKp3.setText(str(DadosControle.Kp3))
        self.lineKi3.setText(str(DadosControle.Ki3))
        self.porta_value.setText(DadosControle.porta)

        self.esq_radio.setChecked(DadosControle.trocouCampo) 
        self.bolaNossa.setChecked(DadosControle.bolaNossa1)
        self.duasFaces.setChecked(DadosControle.duasFaces) 
        self.kalman.setChecked(DadosControle.flagAtivaKalman)  
        self.simular.setChecked(DadosControle.simular) 
        self.alvoFixo.setChecked(DadosControle.irParaAlvoFixo)
