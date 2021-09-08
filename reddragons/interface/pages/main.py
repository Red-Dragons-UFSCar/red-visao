import cv2
import reddragons.interface as ifc
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from reddragons.utils import Logger

from ..utils import ui_files


class GUI_main(QMainWindow):
    def __init__(self, app):

        super(GUI_main, self).__init__()
        loadUi(f"{ui_files}/main.ui", self)
        self.app = app
        self.visao = app.visao
        self.model = app.model

        self.QT_btVisualizacao.clicked.connect(self.visualizacao)
        self.QT_btPerspectiva.clicked.connect(self.perspectiva)
        self.QT_btCruzetas.clicked.connect(self.cruzetas)
        self.QT_btCores.clicked.connect(self.cores)
        self.QT_Load.clicked.connect(self.carregar)
        self.QT_Save.clicked.connect(self.salvar)
        self.QT_Centro.clicked.connect(self.centro)
        self.QT_FPS.clicked.connect(self.mudar_verbose)
        self.QT_Versao.clicked.connect(self.versao)
        self.QT_btcontrole.clicked.connect(self.controle)
        self.QT_jogo.clicked.connect(self.jogar)
        self.QT_voltar.clicked.connect(self.voltar)
        self.show()

        self.visao.iniciar()

    def voltar (self):
        self.app.back()

    def visualizacao(self):
        self.app.push_widget(ifc.GUI_visualizacao(self.app))

    def perspectiva(self):
        self.tela = ifc.GUI_perspectiva(self.app)

    def cruzetas(self):
        self.tela = ifc.GUI_cruzetas(self.app)

    def cores(self):
        self.app.push_widget(ifc.GUI_cores(self.app))

    def centro(self):
        self.tela = ifc.GUI_centro(self.visao, self.model)

    def controle(self):
        self.tela = ifc.GUI_controle(self.visao, self.model)

    def jogar(self):
        self.tela = ifc.GUI_jogar(self.visao, self.model)

    def versao(self):
        Logger().dado(cv2.getBuildInformation())

    def closeEvent(self, event):
        print(Logger()._fps_mean)
        self.visao.stop()

    def mudar_verbose(self):
        self.visao.mudar_verbose()

    def salvar(self):
        self.tela = ifc.GUI_salvar(self.visao, self.model)

    def carregar(self):
        self.tela = ifc.GUI_carregar(self.visao, self.model)
