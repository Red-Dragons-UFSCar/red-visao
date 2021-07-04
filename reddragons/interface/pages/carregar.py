import os
import pickle

from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_carregar(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_carregar, self).__init__()
        self.model = model
        self.carregar()

    def carregar(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", filter = "*.red")
        try:
            with open(filename[0], "rb") as f:
                self.model.dados = pickle.load(f)
        except EnvironmentError as err:
            print(f"Falha ao carregar arquivo: {err}")

