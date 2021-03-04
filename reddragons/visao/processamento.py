import copy
import threading
import time

import cv2
import numpy as np
from reddragons.visao import captura, estruturas, utils, services
from reddragons.visao.logger import Logger


class Processamento:
    def __init__(self):
        self._init_data()
        self._init_services()
        self.started = False
        self.cam = captura.Imagem()
        self.read_lock = threading.Lock()
        self.verbose = False
        self.cam.iniciar()
        self.recalcular()

    def _init_data (self):
        self.imagem = estruturas.Imagem()
        self.dados = estruturas.Dados()
        self.dados_controle = estruturas.Controle()

    def _init_services(self):
        self._perspectiva = services.Perspectiva(self.dados)
        self._corte = services.Corte(self.dados)
        self._converte_hsv = services.ConverteHSV()
        self._centroides = services.Centroides(self.dados)
        self._centros = services.Centros(self.dados)

    def alterar_src(self, src="videos/jogo.avi"):
        self.stop()
        self.cam.alterar_src(src)
        self.started = False
        self.iniciar()

    def mudar_verbose(self):
        self.verbose = not self.verbose

    def iniciar(self):
        if self.started:
            return None
        self.started = True
        self.thread = threading.Thread(target=self.main, args=())
        self.thread.start()
        return self

    def processar(self):
        err = False
        tempo = {}
        tempo['inicial'] = time.time()
        self.conseguiu, self.img = self.cam.read()

        if not self.conseguiu:
            Logger().erro("Sem frame da captura")
            self.cam.stop()
            self.cam = captura.Imagem()
            self.cam.iniciar()
            Logger().flag("Câmera reiniciada")

            return (True, None)

        tempo['camera'] = time.time()

        imagem = copy.deepcopy(self.imagem)
        imagem.imagem_original = copy.deepcopy(self.img)
        tempo['copia'] = time.time()

        _, tempo['warp'] = self._perspectiva.run(imagem.imagem_original, imagem)
        _, tempo['corte'] = self._corte.run(imagem.imagem_warp, imagem)
        _, tempo['hsv'] = self._converte_hsv.run(imagem.imagem_crop, imagem)
        _, tempo['centroids'] = self._centroides.run(imagem.imagem_hsv, imagem)
        _, tempo['centros'] = self._centros.run(imagem.centroids, imagem)
        imagem.adversarios = imagem.centroids[5]

        with self.read_lock:
            self.imagem = copy.deepcopy(imagem)
        tempo['final'] = time.time()

        return err, tempo

    def main(self):
        i_frame = 0
        while self.started:
            self.conseguiu, self.img = self.cam.read()
            err, tempo = self.processar()
            if err: continue
            i_frame+=1

            if self.verbose:
                Logger().tempo(i_frame, *tempo.values())    

    def recalcular(self):
        dados = self.dados
        dados.matriz_warp_perspective = self._perspectiva.calcula()

        with self.read_lock:
            self.dados = dados

    def read_imagem(self):
        with self.read_lock:
            imagem = self.imagem
        return imagem

    def read_dados(self):
        with self.read_lock:
            dados = self.dados
        return dados

    def set_dados(self, dados):
        with self.read_lock:
            self.dados = dados

    def get_referencia(self):
        with self.read_lock:
            img = self.imagem.imagem
        return img

    def stop(self):
        self.started = False
        self.thread.join()
        self.cam.stop()

    def read_dados_controle(self):
        with self.read_lock:
            dados_controle = self.dados_controle
        return dados_controle

    def set_dados_controle(self, dados_controle):
        with self.read_lock:
            self.dados_controle = dados_controle

    def sincronizar_controle(self):
        dados_controle = self.dados_controle
        dados = self.dados

        dados_controle.distCruzX = abs(dados.cruzetas[0][0] - dados.cruzetas[1][0])
        dados_controle.distCruzY = abs(dados.cruzetas[0][1] - dados.cruzetas[2][1])
        dados_controle.constX = 70.0 / dados_controle.distCruzX
        dados_controle.constY = 37.5 / dados_controle.distCruzY

        dados_controle = self.sincronizar_controle_dinamico(dados_controle)
        self.set_dados_controle(dados_controle)
        return dados_controle

    def sincronizar_controle_dinamico(self, dados_controle=None):
        if dados_controle is None:
            dados_controle = copy.deepcopy(self.dados_controle)
        imagem = self.imagem

        if imagem.centroids[0] == []:
            Logger().erro("Bola não detectada. Usando última posição")
        else:
            try:
                dados_controle.bola = (
                    imagem.centroids[0][0][0][0],
                    imagem.centroids[0][0][0][1],
                )
            except ValueError:
                Logger().erro(str(imagem.centroids[0]))

        # Logger().variavel('dados_controle.bola', dados_controle.bola)

        dados_controle.robot = imagem.centros
        # Logger().variavel('dados_controle.robot', dados_controle.robot)
        err = utils.checar_erro_centroide(imagem.centros)
        for i in range(3):
            if err[i] != 0:
                dados_controle.robot[i] = self.dados_controle.robot[i]
                Logger().erro(
                    "Robô #" + str(i) + " não detectado. Usando última posição"
                )
        # Logger().variavel('dados_controle.robot', dados_controle.robot)

        dados_controle.adversarios = imagem.adversarios[0]
        # Logger().variavel('dados_controle.adversarios', dados_controle.adversarios.T)

        self.set_dados_controle(dados_controle)

        return dados_controle

    def __exit__(self, exec_type, exc_value, traceback):
        self.cam.stop()
