from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi
import cv2

from reddragons.visao import Logger

#import GUIs
import reddragons.interface as ifc

class GUI_main(QMainWindow):
    def __init__(self, visao):
    
        super(GUI_main, self).__init__()
        loadUi(f'{ui_files}/main.ui', self)
        self.visao = visao

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
        self.QT_camera.clicked.connect(self.setCamera)
        self.QT_btcontrole.clicked.connect(self.controle)
        self.QT_jogo.clicked.connect(self.jogar)
        self.show()
        
        
        self.visao.iniciar()
        
    def setCamera(self):
        self.tela = ifc.GUI_camera(self.visao)
        
    def visualizacao(self):
        self.tela = ifc.GUI_visualizacao(self.visao)
        
    def perspectiva(self):
        self.tela = ifc.GUI_perspectiva(self.visao)
        
    def corte(self):
        self.tela = ifc.GUI_corte(self.visao)
        
    def cruzetas(self):
        self.tela = ifc.GUI_cruzetas(self.visao)
        
    def cores(self):
        self.tela = ifc.GUI_cores(self.visao)
        
    def centro(self):
        self.tela = ifc.GUI_centro(self.visao)

    def controle(self):
        self.tela = ifc.GUI_controle(self.visao)

    def jogar(self):
        self.tela = ifc.GUI_jogar(self.visao)

    def versao(self):
        Logger().dado(cv2.getBuildInformation())
        
    def closeEvent(self, event):
        self.visao.stop()
        
    def mudar_verbose(self):
        self.visao.mudar_verbose()
        
    def salvar(self):
        self.tela = ifc.GUI_salvar(self.visao)
    
    def carregar(self):
        self.tela = ifc.GUI_carregar(self.visao)
