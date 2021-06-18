import os
import pickle

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_video(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_video, self).__init__()
        loadUi(f"{ui_files}/mainwindow.ui", self)
        self.visao = visao
        self.model = model
        self.show()



