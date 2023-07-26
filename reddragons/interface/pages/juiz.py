from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
import threading

from ..utils import ui_files

#from vss_communication import Referee


class GUI_juiz(QMainWindow):
    def __init__(self,visao,model):
        super(GUI_juiz, self).__init__()
        loadUi(f"{ui_files}/juiz.ui", self)
        self.show()
        self.visao = visao
        self.model = model
        self.timer = QTimer(self)
        self.timer.start(1)

        self.btPararTransmissao.clicked.connect(self.terminarTransmissao)
        self.btJogar.clicked.connect(self.iniciarTransmissao)

        self.QT_btFreeBall.clicked.connect(lambda: self.mudanca_foul(3))
        self.QT_btPenaltyKick.clicked.connect(lambda: self.mudanca_foul(1))
        self.QT_btGoalKick.clicked.connect(lambda: self.mudanca_foul(2))
        self.QT_btKickOff.clicked.connect(lambda: self.mudanca_foul(4))
        
        self.QT_btHalt.stateChanged.connect(lambda: self.mudanca_foul(7))
        self.QT_btStop.stateChanged.connect(lambda: self.mudanca_foul(5))
        self.QT_btStart.stateChanged.connect(lambda: self.mudanca_foul(6))
        
        self.QT_btQ1.stateChanged.connect(lambda: self.mudanca_quadrante(1))
        self.QT_btQ2.stateChanged.connect(lambda: self.mudanca_quadrante(2))
        self.QT_btQ3.stateChanged.connect(lambda: self.mudanca_quadrante(3))
        self.QT_btQ4.stateChanged.connect(lambda: self.mudanca_quadrante(4))
        self.QT_btYellow.stateChanged.connect(lambda: self.mudanca_teamcolor(1))
        self.QT_btBlue.stateChanged.connect(lambda: self.mudanca_teamcolor(0))

        self.qt_Label.setText("Esperando iniciar")
        self.qt_Label.setStyleSheet("background-color:yellow")
        self.qt_FaltaAtual.setText("Juiz acabou de ser iniciado")
        self.qt_UltimaFalta.setText("Juiz acabou de ser iniciado")

        self.Color = 1
        self.quadrante = 1
        self.foul = 1

        self.QuadranteAtual = 0
        self.FaltaAtual = 4
        self.CorAtual = 2

        self.QuadranteAnterior = 0
        self.FaltaAnterior = 4
        self.CorAnterior = 2

        #self.referee = Referee()
        
    def mudanca_quadrante(self,enum):
        self.quadrante = enum
        if enum == 1:
            if self.QT_btQ1.isChecked():
                self.QT_btQ2.setCheckable(False)
                self.QT_btQ3.setCheckable(False)
                self.QT_btQ4.setCheckable(False)
            else:
                self.QT_btQ2.setCheckable(True)
                self.QT_btQ3.setCheckable(True)
                self.QT_btQ4.setCheckable(True)

        elif enum == 2:
            if self.QT_btQ2.isChecked():
                self.QT_btQ1.setCheckable(False)
                self.QT_btQ3.setCheckable(False)
                self.QT_btQ4.setCheckable(False)
            else:
                self.QT_btQ1.setCheckable(True)
                self.QT_btQ3.setCheckable(True)
                self.QT_btQ4.setCheckable(True)
        elif enum == 3:
            if self.QT_btQ3.isChecked():
                self.QT_btQ1.setCheckable(False)
                self.QT_btQ2.setCheckable(False)
                self.QT_btQ4.setCheckable(False)
            else:
                self.QT_btQ1.setCheckable(True)
                self.QT_btQ2.setCheckable(True)
                self.QT_btQ4.setCheckable(True)
        elif enum == 4:
            if self.QT_btQ4.isChecked():
                self.QT_btQ2.setCheckable(False)
                self.QT_btQ3.setCheckable(False)
                self.QT_btQ1.setCheckable(False)
            else:
                self.QT_btQ2.setCheckable(True)
                self.QT_btQ3.setCheckable(True)
                self.QT_btQ1.setCheckable(True)
            

    def mudanca_foul(self,enum):
        self.foul = enum
        if enum == 1:
            self.RegistraFalta()
            self.cria_dic()
            self.quadrante = 0
        elif enum == 2:
            self.RegistraFalta()
            self.cria_dic()
            self.quadrante = 0
            self.color = 2
        elif enum == 4:
            self.RegistraFalta()
            self.cria_dic()
            self.quadrante = 0
        elif enum == 0:
            self.RegistraFalta()
            self.cria_dic()
            self.quadrante = 0
        elif enum == 3:
            self.RegistraFalta()
            self.cria_dic()
            self.color = 2
        elif enum == 5:
            if self.QT_btStop.isChecked():
                self.qt_Label.setText("Stop")
                self.qt_Label.setStyleSheet("background-color:red")
                self.cria_dic()
                self.QT_btHalt.setCheckable(False)
                self.QT_btStart.setCheckable(False)
            else:
                self.QT_btHalt.setCheckable(True)
                self.QT_btStart.setCheckable(True)
        elif enum == 6:
            if self.QT_btStart.isChecked():
                self.cria_dic()
                self.qt_Label.setText("Start")
                self.qt_Label.setStyleSheet("background-color:green")
                self.QT_btHalt.setCheckable(False)
                self.QT_btStop.setCheckable(False)
            else:
                self.QT_btHalt.setCheckable(True)
                self.QT_btStop.setCheckable(True)
        elif enum == 7:
            if self.QT_btHalt.isChecked():
                self.cria_dic()
                self.qt_Label.setText("Halt")
                self.qt_Label.setStyleSheet("background-color:red")
                self.QT_btStop.setCheckable(False)
                self.QT_btStart.setCheckable(False)
            else:
                self.QT_btStop.setCheckable(True)
                self.QT_btStart.setCheckable(True)         
        

    def mudanca_teamcolor(self, enum):
        self.Color = enum
        if enum == 0:
            if self.QT_btBlue.isChecked():
                self.QT_btYellow.setCheckable(False)
            else:
                self.QT_btYellow.setCheckable(True)
        elif enum == 1:
            if self.QT_btYellow.isChecked():
                self.QT_btBlue.setCheckable(False)
            else:
                self.QT_btBlue.setCheckable(True)

    def RegistraFalta(self):
        self.FaltaAnterior = self.FaltaAtual
        self.FaltaAtual = self.foul
        self.QuadranteAnterior = self.QuadranteAtual
        self.QuadranteAtual = self.quadrante
        self.CorAnterior = self.CorAtual
        self.CorAtual = self.Color


        #Parte dos valores atuais
        if self.FaltaAtual == 0:
            self.FaltaTextoAtual = "Free Kick"
        elif self.FaltaAtual == 1:
            self.FaltaTextoAtual = "Penalty Kick"
        elif self.FaltaAtual == 2:
            self.FaltaTextoAtual = "Goal Kick"
        elif self.FaltaAtual == 3:
            self.FaltaTextoAtual = "Free Ball"
        elif self.FaltaAtual == 4:
            self.FaltaTextoAtual = "KickOff"


        if self.QuadranteAtual == 0:
            self.QuadranteTextoAtual = ", Sem Quadrante"
        elif self.QuadranteAtual == 1:
            self.QuadranteTextoAtual = ", Quadrante 1"
        elif self.QuadranteAtual == 2:
            self.QuadranteTextoAtual = ", Quadrante 2"
        elif self.QuadranteAtual == 3:
            self.QuadranteTextoAtual = ", Quadrante 3"
        elif self.QuadranteAtual == 4:
            self.QuadranteTextoAtual = ", Quadrante 4"

        if self.CorAtual == 0:
            self.CorTextoAtual = ", Blue"
        elif self.CorAtual == 1:
            self.CorTextoAtual = ", Yellow"
        elif self.CorAtual == 2:
            self.CorTextoAtual = ", No color"
        
        #Parte dos valores anteriores
        if self.FaltaAnterior == 0:
            self.FaltaTextoAnterior = "Free Kick"
        elif self.FaltaAnterior == 1:
            self.FaltaTextoAnterior = "Penalty Kick"
        elif self.FaltaAnterior == 2:
            self.FaltaTextoAnterior = "Goal Kick"
        elif self.FaltaAnterior == 3:
            self.FaltaTextoAnterior = "Free Ball"
        elif self.FaltaAnterior == 4:
            self.FaltaTextoAnterior = "KickOff"

        if self.QuadranteAnterior == 0:
            self.QuadranteTextoAnterior = ", Sem Quadrante"
        elif self.QuadranteAnterior == 1:
            self.QuadranteTextoAnterior = ", Quadrante 1"
        elif self.QuadranteAnterior == 2:
            self.QuadranteTextoAnterior = ", Quadrante 2"
        elif self.QuadranteAnterior == 3:
            self.QuadranteTextoAnterior = ", Quadrante 3"
        elif self.QuadranteAnterior == 4:
            self.QuadranteTextoAnterior = ", Quadrante 4"

        if self.CorAnterior == 0:
            self.CorTextoAnterior = ", Blue"
        elif self.CorAnterior == 1:
            self.CorTextoAnterior = ", Yellow"
        elif self.CorAnterior == 2:
            self.CorTextoAnterior = ", No color"

        textoAtual = "Caso atual:" +str(self.FaltaTextoAtual) +str(self.CorTextoAtual) +str(self.QuadranteTextoAtual)
        textoAntigo = "Caso Anterior:" +str(self.FaltaTextoAnterior) +str(self.CorTextoAnterior) +str(self.QuadranteTextoAnterior)


        self.qt_FaltaAtual.setText(textoAtual)
        self.qt_UltimaFalta.setText(textoAntigo)

    def cria_dic(self):
        dicionario_faltas = dict([("foul", self.foul), ("teamcolor", self.Color), ("foulQuadrant", self.quadrante), ("timestamp", 0), ("gameHalf", 1)])
        #self.protobuff.send_mensage(self.dicionario_faltas)
        #self.referee.send_mensage(dicionario_faltas)
        print(dicionario_faltas)

    def iniciarTransmissao(self):
        self.looping = threading.Timer(0.02, self.iniciarTransmissao)
        print(self.QuadranteAnterior)
        self.cria_dic()
        self.looping.start()

    def terminarTransmissao(self):
        self.looping.cancel()
    
    def closeEvent(self,event):
        try:
            self.looping.cancel()
            event.accept()
        except:
            event.accept()