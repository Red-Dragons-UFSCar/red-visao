import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..utils import ui_files


class GUI_camera(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_camera, self).__init__()
        loadUi(f"{ui_files}/camera.ui", self)
        self.show()
        self.visao = visao
        self.model = model
        self.QT_listaVideos.clear()
        for files in os.listdir("videos"):
            if files.endswith(".avi"):
                self.QT_listaVideos.addItem(str(files))

        self.QT_camera.clicked.connect(self.set_camera)
        self.QT_video.clicked.connect(self.set_video)
        self.QT_webcam.clicked.connect(self.set_webcam)

    def set_camera(self):

        self.visao.alterar_src(2)

    def set_video(self):

        self.visao.alterar_src("videos/" + self.QT_listaVideos.currentText())

    def set_webcam(self):

        self.visao.alterar_src(0)
