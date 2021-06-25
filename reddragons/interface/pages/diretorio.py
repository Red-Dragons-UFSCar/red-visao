from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_diretorio(QMainWindow):
    def __init__(self, callback):
        super(GUI_diretorio, self).__init__()
        loadUi(f"{ui_files}/diretorio.ui", self)
        self.show()
        self.callback = callback
        self._diretorio = ""
        self.btnDiretorioEscolher.clicked.connect(self._escolher)
        self.btnDiretorioOk.clicked.connect(self._ok)

    def _ok (self):
        self._diretorio = self.CaminhoVideo.text()
        self.callback(self._diretorio)
        self.close()

    def _escolher(self):
        """abre o QFileDialog para a escolha do arquivo
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Videos (*.avi);;All files (*.*)")
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec():
            file_name = file_dialog.selectedFiles()[0]
        
        self.CaminhoVideo.setText(file_name)
