import threading
import cv2
from reddragons.visao.logger import logger
import time
from pathlib import Path

jogo_path = str(Path(__file__, "../../../data/jogo.avi").resolve())


def testDevice(src):
    cap = cv2.VideoCapture(src)
    if cap is None or not cap.isOpened():
        logger().erro("Não foi possível abrir o dispositivo: " + str(src))
        return 0
    return 1


class Imagem:
    def __init__(self, src=jogo_path):
        estado = testDevice(src)
        if estado:
            self.src = src
        else:
            self.src = jogo_path
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.conseguiu, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def alterarSrc(self, src=jogo_path):
        self.stop()
        estado = testDevice(src)
        if estado:
            self.src = src
        else:
            self.src = jogo_path
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.conseguiu, self.frame = self.cap.read()

        self.started = False
        self.iniciar()

    def iniciar(self):
        if self.started:
            logger().dado("Captura já iniciada")
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
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
