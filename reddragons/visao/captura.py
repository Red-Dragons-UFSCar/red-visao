import threading
import time

import cv2
from reddragons import utils
from reddragons.utils.logger import Logger


class Imagem:
    def __init__(self, src):
        """ Construtor da classe
        Args:
             src (any): fonte a qual provê a captura da imagem
        """
        self.started = False
        self.thread = None
        self.conseguiu, self.frame = False, None
        self.alterar_src(src)
        self.read_lock = threading.Lock()

    def alterar_src(self, src):
        """ Verifica a necessidade de alterar o dispositivo de entrada
        Args:
             src (any): fonte a qual provê a captura da imagem
        Raises:
            Exception: exceção caso o dispositivo de entradaseja inválido 
        """
        self.stop()
        if not utils.test_device(src):
            raise Exception (f'Entrada {src} é inválida')

        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.conseguiu, self.frame = self.cap.read()

        self.started = False
        self.iniciar()

    def iniciar(self):
        """ Inicia a captura de imagem caso não tenha sido iniciada
        """
        if self.started:
            Logger().dado("Captura já iniciada")
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        """ Atualiza o frame
        """
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
        """ Realiza a parada na captura da imagem
        """
        if not self.started:
            return
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        """Encerra a execução da camera
        Args:
            exec_type (_type_): classe da exceção
            exc_value (_type_): instância da exceção
            traceback (_type_): objeto de rastreamento que rastreia a última função chamada na pilha
        """
        self.cap.release()
