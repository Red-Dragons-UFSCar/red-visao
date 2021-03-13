import os
import pickle

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_carregar(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_carregar, self).__init__()
        loadUi(f"{ui_files}/carregar.ui", self)
        self.show()
        self.visao = visao
        self.model = model
        self.QT_listaSalvos.clear()
        for files in os.listdir("modelos"):
            if files.endswith(".red"):
                self.QT_listaSalvos.addItem(str(files))
        self.QT_carregar.clicked.connect(self.carregar)

    def carregar(self):

        arquivo = open("modelos/" + self.QT_listaSalvos.currentText(), "rb")
        self.model.dados = pickle.load(arquivo)
