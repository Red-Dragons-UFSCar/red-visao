import copy
import threading
import time

import cv2
import numpy as np
from reddragons.visao import captura, estruturas, utils
from reddragons.visao.logger import Logger


class Processamento:
    def __init__(self):
        self.imagem = estruturas.Imagem()
        self.dados = estruturas.Dados()
        self.dados_controle = estruturas.Controle()
        self.started = False
        self.cam = captura.Imagem()
        self.read_lock = threading.Lock()
        self.verbose = False
        self.cam.iniciar()
        self.recalcular()

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
        self.thread = threading.Thread(target=self.processar, args=())
        self.thread.start()
        return self

    def processar(self):
        i_frame = 0
        while self.started:
            tempo_inicial = time.time()

            self.conseguiu, self.img = self.cam.read()

            if self.conseguiu:
                # self.img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                i_frame += 1
                tempo_camera = time.time()

                imagem = copy.deepcopy(self.imagem)
                dados = copy.deepcopy(self.dados)
                imagem.imagem_original = copy.deepcopy(self.img)
                tempo_copia = time.time()

                _img = utils.warp_perspective(imagem.imagem_original, dados)
                imagem.imagem_warp = copy.deepcopy(_img)
                tempo_warp = time.time()

                _img2 = utils.corte_imagem(_img, dados)
                imagem.imagem_crop = copy.deepcopy(_img2)
                tempo_corte = time.time()

                imagem.imagem_hsv = cv2.cvtColor(
                    np.uint8(imagem.imagem_crop), cv2.COLOR_RGB2HSV
                )
                tempo_hsv = time.time()

                centr_final = []
                for cor, filtro in zip(self.dados.cores, self.dados.filtros):
                    cortornos, _ = utils.get_contorno_cor(
                        imagem.imagem_hsv, cor, filtro
                    )
                    centroids = np.empty((0, 3))
                    for c in cortornos:
                        moments = cv2.moments(c)
                        if (moments["m00"] >= self.dados.area_minima) and (
                            moments["m00"] <= self.dados.area_maxima
                        ):
                            c_x = int(moments["m10"] / moments["m00"])
                            c_y = int(moments["m01"] / moments["m00"])
                            centroids = np.vstack(
                                (centroids, np.asarray([c_x, c_y, moments["m00"]]))
                            )
                    centr_final.append(np.array([centroids]))
                imagem.centroids = centr_final

                tempo_centroids = time.time()

                centros = utils.calcula_centros(centr_final, dados.ang_corr)

                if self.imagem.centros is not None:
                    if abs(centros[0][2] - self.imagem.centros[0][2]) < 0.30:
                        centros[0][2] = (
                            centros[0][2]
                            - (centros[0][2] - self.imagem.centros[0][2]) * 0.85
                        )

                    if abs(centros[1][2] - self.imagem.centros[1][2]) < 0.30:
                        centros[1][2] = (
                            centros[1][2]
                            - (centros[1][2] - self.imagem.centros[1][2]) * 0.85
                        )

                    if abs(centros[2][2] - self.imagem.centros[2][2]) < 0.30:
                        centros[2][2] = (
                            centros[2][2]
                            - (centros[2][2] - self.imagem.centros[2][2]) * 0.85
                        )

                imagem.centros = centros
                imagem.adversarios = centr_final[5]
                tempo_centros = time.time()

                with self.read_lock:
                    self.imagem = copy.deepcopy(imagem)

                tempo_final = time.time()

                if self.verbose:
                    Logger().tempo(
                        i_frame,
                        tempo_inicial,
                        tempo_camera,
                        tempo_copia,
                        tempo_warp,
                        tempo_corte,
                        tempo_hsv,
                        tempo_centroids,
                        tempo_centros,
                        tempo_final,
                    )
            else:
                Logger().erro("Sem frame da captura")
                self.cam.stop()
                self.cam = captura.Imagem()
                self.cam.iniciar()
                Logger().flag("Câmera reiniciada")

    def recalcular(self):
        dados = self.dados
        dados.matriz_warp_perspective = utils.matriz_warp_perspective(dados)

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
