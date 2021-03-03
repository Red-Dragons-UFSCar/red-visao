from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi

from reddragons.visao.estruturas import *
from reddragons.visao.logger import *
from ..utils import ui_files

import os

class GUI_camera(QMainWindow):
    def __init__(self, visao):
        super(GUI_camera, self).__init__()
        loadUi(f'{ui_files}/camera.ui', self)
        self.show()    
        self.visao = visao
        self.QT_listaVideos.clear()
        for files in os.listdir("videos"):
            if files.endswith(".avi"):
                self.QT_listaVideos.addItem(str(files))
        
        self.QT_camera.clicked.connect(self.setCamera)
        self.QT_video.clicked.connect(self.setVideo)
        self.QT_webcam.clicked.connect(self.setWebcam)
        
    def setCamera(self):
        
        self.visao.alterarSrc(2)
        
    def setVideo(self):
        
        self.visao.alterarSrc("videos/" + self.QT_listaVideos.currentText())
        
    def setWebcam(self):
        
        self.visao.alterarSrc(0)