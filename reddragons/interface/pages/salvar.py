import pickle

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_salvar(QMainWindow):
    def __init__(self, visao):
        super(GUI_salvar, self).__init__()
        loadUi(f"{ui_files}/salvar.ui", self)
        self.show()
        self.visao = visao
        self.QT_salvar.clicked.connect(self.salvar)

    def salvar(self):
        arquivo = open("modelos/" + self.QT_nomeSalvar.text() + ".red", "wb")

        pickle.dump(self.visao.read_dados(), arquivo)
