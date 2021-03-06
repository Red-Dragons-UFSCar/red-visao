from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from cv2 import VideoCapture
from ..utils import ui_files

def list_ports():
    is_working = True
    dev_port = 0
    working_ports = []
    available_ports = []
    while is_working:
        camera = VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
        else:
            is_reading, _ = camera.read()
            if is_reading:
                working_ports.append(dev_port)
            else:
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports

class GUI_camera(QMainWindow):
    def __init__(self, callback):
        super(GUI_camera, self).__init__()
        loadUi(f"{ui_files}/EscolheCamera.ui", self)
        self.show()
        _, wrk_ports = list_ports()
        self.CaixaSelecionar.addItems([f'Dispositivo {i}' for i in wrk_ports])
        self.callback = callback
        self._camera = ""
        self.btnCameraOk.clicked.connect(self._ok)

    def _ok (self):
        try:
            self._camera = int(self.CaixaSelecionar.currentText()[-1])
        except:
            self._camera = ''
        self.callback(self._camera)
        self.close()