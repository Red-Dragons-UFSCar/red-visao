from PyQt5.QtWidgets import QMainWindow, QFileDialog
from .perspectiva import GUI_perspectiva
from .main import GUI_main
from PyQt5.uic import loadUi
import pickle
from ..utils import ui_files


class GUI_padrao(QMainWindow):
    def __init__(self, app):
        super(GUI_padrao, self).__init__()
        loadUi(f"{ui_files}/padrao.ui", self)
        self.app = app
        self.model = app.model
        self.visao = app.visao
        self.show()
        self.btnSim.clicked.connect(self._carrega)
        self.btnNao.clicked.connect(self._next)
        self.btnVoltar.clicked.connect(self.app.back)

    def _carrega (self):
        filename = QFileDialog.getOpenFileName(self, "Open File", filter = "*.red")
        try:
            with open(filename[0], "rb") as f:
                self.model.dados = pickle.load(f)
            self.app.push_widget(GUI_main(self.app))
        except EnvironmentError as err:
            print(f"Falha ao carregar arquivo: {err}")

    def _next (self):
        self.app.push_widget(GUI_perspectiva(self.app))
        