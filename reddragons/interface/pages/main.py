import cv2
import reddragons.interface as ifc
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from reddragons.utils import Logger

from ..utils import ui_files


class GUI_main(QMainWindow):
    def __init__(self, visao, model):

        super(GUI_main, self).__init__()
        loadUi(f"{ui_files}/main.ui", self)
        self.visao = visao
        self.model = model

        self.QT_btVisualizacao.clicked.connect(self.visualizacao)
        self.QT_btPerspectiva.clicked.connect(self.perspectiva)
        self.QT_btCorte.clicked.connect(self.corte)
        self.QT_btCruzetas.clicked.connect(self.cruzetas)
        self.QT_btCores.clicked.connect(self.cores)
        self.QT_Load.clicked.connect(self.carregar)
        self.QT_Save.clicked.connect(self.salvar)
        self.QT_Centro.clicked.connect(self.centro)
        self.QT_FPS.clicked.connect(self.mudar_verbose)
        self.QT_Versao.clicked.connect(self.versao)
        self.QT_camera.clicked.connect(self.set_camera)
        self.QT_btcontrole.clicked.connect(self.controle)
        self.QT_jogo.clicked.connect(self.jogar)
        self.show()

        self.visao.iniciar()

    def set_camera(self):
        self.tela = ifc.GUI_camera(self.visao, self.model)

    def visualizacao(self):
        self.tela = ifc.GUI_visualizacao(self.visao, self.model)

    def perspectiva(self):
        self.tela = ifc.GUI_perspectiva(self.visao, self.model)

    def corte(self):
        self.tela = ifc.GUI_corte(self.visao, self.model)

    def cruzetas(self):
        self.tela = ifc.GUI_cruzetas(self.visao, self.model)

    def cores(self):
        self.tela = ifc.GUI_cores(self.visao, self.model)

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
