from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_diretorio(QMainWindow):
    def __init__(self, callback):
        super(GUI_diretorio, self).__init__()
        loadUi(f"{ui_files}/diretorio.ui", self)
        self.show()
        self.callback = callback
        self._diretorio = "FUNCIONA"
        self.btnDiretorioEscolher.clicked.connect(self._escolher)
        self.btnDiretorioOk.clicked.connect(self._ok)

    def _escolher (self):
        print("VOCE CLICOU NO BOTAO DE DIRETORIO")
    
    def _ok (self):
        self.callback(self._diretorio)
        self.close()
