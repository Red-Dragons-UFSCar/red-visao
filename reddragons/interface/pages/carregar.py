import os
import pickle

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from reddragons.visao import VisaoController

from ..utils import ui_files


class GUI_carregar(QMainWindow):
    def __init__(self, visao: VisaoController):
        super(GUI_carregar, self).__init__()
        loadUi(f"{ui_files}/carregar.ui", self)
        self.show()
        self.visao = visao
        self.QT_listaSalvos.clear()
        for files in os.listdir("modelos"):
            if files.endswith(".red"):
                self.QT_listaSalvos.addItem(str(files))
        self.QT_carregar.clicked.connect(self.carregar)

    def carregar(self):

        arquivo = open("modelos/" + self.QT_listaSalvos.currentText(), "rb")
        self.visao.dados = pickle.load(arquivo)
