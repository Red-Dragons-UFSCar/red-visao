import threading
import time

import cv2
from reddragons import utils
from reddragons.visao.logger import Logger


class Captura(metaclass=utils._Singleton):
    def __init__(self, src=utils.VIDEO_PATH):
        self.started = False
        self.thread = None
        self.conseguiu, self.frame = False, None
        self.alterar_src(src)
        self.read_lock = threading.Lock()

    def alterar_src(self, src=utils.VIDEO_PATH):
        self.stop()
        estado = utils.test_device(src)
        if estado:
            self.src = src
        else:
            self.src = utils.VIDEO_PATH
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.conseguiu, self.frame = self.cap.read()

        self.started = False
        self.iniciar()

    def iniciar(self):
        if self.started:
            Logger().dado("Captura já iniciada")
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            time.sleep(0.03)
            conseguiu, frame = self.cap.read()
            with self.read_lock:
                self.conseguiu = conseguiu
                if frame is not None:
                    frame = frame[:, :, ::-1]
                self.frame = frame

    def read(self):
        with self.read_lock:
            if self.frame is None:
                frame = None
                conseguiu = False
            else:
                frame = self.frame.copy()
                conseguiu = self.conseguiu
        return conseguiu, frame

    def stop(self):
        if not self.started:
            return
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
