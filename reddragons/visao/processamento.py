import cv2
import numpy as np
import threading
from reddragons.visao import estruturas
from reddragons.visao import captura
import time
from reddragons.visao.logger import logger
from reddragons.visao import utils
import copy
import math

cam = captura.Imagem()


class processamento:
    def __init__(self, src="videos/jogo.avi"):
        self.Imagem = estruturas.Imagem()
        self.Dados = estruturas.Dados()
        self.DadosControle = estruturas.Controle()
        self.started = False
        self.read_lock = threading.Lock()
        global cam
        cam.iniciar()

        self.recalcular()
        self.verbose = False

    def alterarSrc(self, src="videos/jogo.avi"):
        self.stop()
        global cam
        cam.alterarSrc(src)
        self.started = False
        self.iniciar()

    def mudarVerbose(self):
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
            tempoInicial = time.time()

            global cam
            self.conseguiu, self.img = cam.read()

            if self.conseguiu:
                # self.img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                i_frame += 1
                tempoCamera = time.time()

                Imagem = copy.deepcopy(self.Imagem)
                Dados = copy.deepcopy(self.Dados)
                Imagem.imagem_original = copy.deepcopy(self.img)
                tempoCopia = time.time()

                _img = utils.warpPerspective(Imagem.imagem_original, Dados)
                Imagem.imagem_warp = copy.deepcopy(_img)
                tempoWarp = time.time()

                _img2 = utils.corteImagem(_img, Dados)
                Imagem.imagem_crop = copy.deepcopy(_img2)
                tempoCorte = time.time()

                Imagem.imagem_HSV = cv2.cvtColor(
                    np.uint8(Imagem.imagem_crop), cv2.COLOR_RGB2HSV
                )
                tempoHSV = time.time()

                D = []
                for cor, filtro in zip(self.Dados.cores, self.Dados.filtros):
                    cortornos, hierarquia = utils.getContornoCor(
                        Imagem.imagem_HSV, cor, filtro
                    )
                    centroids = np.empty((0, 3))
                    for c in cortornos:
                        M = cv2.moments(c)
                        if (M["m00"] >= self.Dados.AreaMinimo) and (
                            M["m00"] <= self.Dados.AreaMaxima
                        ):
                            cX = int(M["m10"] / M["m00"])
                            cY = int(M["m01"] / M["m00"])
                            centroids = np.vstack(
                                (centroids, np.asarray([cX, cY, M["m00"]]))
                            )
                    D.append(np.array([centroids]))
                Imagem.centroids = D

                tempoCentroids = time.time()

                centros = utils.calculaCentros(D, Dados.angCorr)

                if self.Imagem.centros is not None:
                    if abs(centros[0][2] - self.Imagem.centros[0][2]) < 0.30:
                        centros[0][2] = (
                            centros[0][2]
                            - (centros[0][2] - self.Imagem.centros[0][2]) * 0.85
                        )

                    if abs(centros[1][2] - self.Imagem.centros[1][2]) < 0.30:
                        centros[1][2] = (
                            centros[1][2]
                            - (centros[1][2] - self.Imagem.centros[1][2]) * 0.85
                        )

                    if abs(centros[2][2] - self.Imagem.centros[2][2]) < 0.30:
                        centros[2][2] = (
                            centros[2][2]
                            - (centros[2][2] - self.Imagem.centros[2][2]) * 0.85
                        )

                Imagem.centros = centros

                adversarios = [[0, 0], [0, 0], [0, 0]]
                Imagem.adversarios = D[5]

                tempoCentros = time.time()

                with self.read_lock:
                    self.Imagem = copy.deepcopy(Imagem)

                tempoFinal = time.time()

                if self.verbose:
                    logger().tempo(
                        i_frame,
                        tempoInicial,
                        tempoCamera,
                        tempoCopia,
                        tempoWarp,
                        tempoCorte,
                        tempoHSV,
                        tempoCentroids,
                        tempoCentros,
                        tempoFinal,
                    )
            else:
                logger().erro("Sem frame da captura")
                cam.stop()
                cam = captura.Imagem()
                cam.iniciar()
                logger().flag("Câmera reiniciada")

    def recalcular(self):
        Dados = self.Dados
        Dados.M_warpPerspective = utils.matriz_warpPerspective(Dados)

        with self.read_lock:
            self.Dados = Dados

    def read_Imagem(self):
        with self.read_lock:
            Imagem = self.Imagem
        return Imagem

    def read_Dados(self):
        with self.read_lock:
            Dados = self.Dados
        return Dados

    def set_Dados(self, dados):
        with self.read_lock:
            self.Dados = dados

    def get_referencia(self):
        with self.read_lock:
            img = self.Imagem.imagem
        return img

    def stop(self):
        self.started = False
        self.thread.join()
        global cam
        cam.stop()

    def read_DadosControle(self):
        with self.read_lock:
            DadosControle = self.DadosControle
        return DadosControle

    def set_DadosControle(self, DadosControle):
        with self.read_lock:
            self.DadosControle = DadosControle

    def sincronizar_Controle(self):
        DadosControle = self.DadosControle
        Dados = self.Dados

        DadosControle.distCruzX = abs(Dados.cruzetas[0][0] - Dados.cruzetas[1][0])
        DadosControle.distCruzY = abs(Dados.cruzetas[0][1] - Dados.cruzetas[2][1])
        DadosControle.constX = 70.0 / DadosControle.distCruzX
        DadosControle.constY = 37.5 / DadosControle.distCruzY

        DadosControle = self.sincronizar_Controle_dinamico(DadosControle)
        self.set_DadosControle(DadosControle)
        return DadosControle

    def sincronizar_Controle_dinamico(self, DadosControle=None):
        if DadosControle is None:
            DadosControle = copy.deepcopy(self.DadosControle)
        Imagem = self.Imagem

        if Imagem.centroids[0] == []:
            logger().erro("Bola não detectada. Usando última posição")
        else:
            try:
                DadosControle.bola = (
                    Imagem.centroids[0][0][0][0],
                    Imagem.centroids[0][0][0][1],
                )
            except:
                logger().erro(str(Imagem.centroids[0]))

        # logger().variavel('DadosControle.bola', DadosControle.bola)

        DadosControle.robot = Imagem.centros
        # logger().variavel('DadosControle.robot', DadosControle.robot)
        err = self.checarErroCentroide(Imagem.centros)
        for i in range(3):
            if err[i] != 0:
                DadosControle.robot[i] = self.DadosControle.robot[i]
                logger().erro(
                    "Robô #" + str(i) + " não detectado. Usando última posição"
                )
        # logger().variavel('DadosControle.robot', DadosControle.robot)

        DadosControle.adversarios = Imagem.adversarios[0]
        # logger().variavel('DadosControle.adversarios', DadosControle.adversarios.T)

        self.set_DadosControle(DadosControle)

        return DadosControle

    def checarErroCentroide(self, centros):
        erros = [0, 0, 0]
        i = 0

        for c in centros:
            if c[0] == 0 or c[1] == 0:
                erros[i] += 1
                logger().erro("Um centro não detectado")
            i += 1
        return erros

    def __exit__(self, exec_type, exc_value, traceback):
        global cam
        cam.stop()
