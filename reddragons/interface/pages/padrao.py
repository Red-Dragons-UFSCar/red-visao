from PyQt5.QtWidgets import QMainWindow, QFileDialog
from .perspectiva import GUI_perspectiva
from PyQt5.uic import loadUi
import pickle
from ..utils import ui_files


class GUI_padrao(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_padrao, self).__init__()
        loadUi(f"{ui_files}/padrao.ui", self)
        self.model = model
        self.visao = visao
        self.show()
        self.btnSim.clicked.connect(self._carrega)
        self.btnNao.clicked.connect(self._next)

    def _carrega (self):
        filename = QFileDialog.getOpenFileName(self, "Open File", filter = "*.red")
        try:
            with open(filename[0], "rb") as f:
                self.model.dados = pickle.load(f)
            self._next()
        except EnvironmentError as err:
            print(f"Falha ao carregar arquivo: {err}")

    def _next (self):
        self._next = GUI_perspectiva(self.visao, self.model)
        self._next.show()
        self.close()