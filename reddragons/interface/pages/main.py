from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi
import cv2

from estruturas import *
from logger import *

#import GUIs
from .camera import GUI_camera
from .carregar import GUI_carregar
from .centros import GUI_centro
from .controle import GUI_controle
from .cores import GUI_cores
from .corte import GUI_corte
from .cruzetas import GUI_cruzetas
from .jogar import GUI_jogar
from .perspectiva import GUI_perspectiva
from .salvar import GUI_salvar
from .visualizacao import GUI_visualizacao

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
        self.QT_FPS.clicked.connect(self.mudarVerbose)
        self.QT_Versao.clicked.connect(self.versao)
        self.QT_camera.clicked.connect(self.setCamera)
        self.QT_btcontrole.clicked.connect(self.controle)
        self.QT_jogo.clicked.connect(self.jogar)
        self.show()
        
        
        self.visao.iniciar()
        
    def setCamera(self):
        self.tela = GUI_camera(self.visao)
        
    def visualizacao(self):
        self.tela = GUI_visualizacao(self.visao)
        
    def perspectiva(self):
        self.tela = GUI_perspectiva(self.visao)
        
    def corte(self):
        self.tela = GUI_corte(self.visao)
        
    def cruzetas(self):
        self.tela = GUI_cruzetas(self.visao)
        
    def cores(self):
        self.tela = GUI_cores(self.visao)
        
    def centro(self):
        self.tela = GUI_centro(self.visao)

    def controle(self):
        self.tela = GUI_controle(self.visao)

    def jogar(self):
        self.tela = GUI_jogar(self.visao)

    def versao(self):
        logger().dado(cv2.getBuildInformation())
        
    def closeEvent(self, event):
        self.visao.stop()
        
    def mudarVerbose(self):
        self.visao.mudarVerbose()
        
    def salvar(self):
        self.tela = GUI_salvar(self.visao)
    
    def carregar(self):
        self.tela = GUI_carregar(self.visao)
