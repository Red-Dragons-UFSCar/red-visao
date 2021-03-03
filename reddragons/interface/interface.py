from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from enum import Enum
from utils import PointsParser, converte_coord
import cv2
import numpy as np

import enviarInfo
from estruturas import *
from logger import *
import captura
import processamento
import serial

import sys
import pickle
import math

import glob, os

class Estado(Enum):
    ORIGINAL = 0
    PERSPECTIVA = 1
    CORTE = 2
    CRUZ = 3
    CENTROIDS = 4
    ROBOS = 5

VISAO = processamento.processamento()
           
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI_main()
    window.show()
    sys.exit(app.exec_())
    

