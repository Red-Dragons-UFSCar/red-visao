from copy import deepcopy

import cv2
import numpy as np
from reddragons.visao import utils
from reddragons import estruturas


class Perspectiva():
    def __init__ (self, dados: estruturas.Dados):
        self._dados = dados

    def calcula(self):
        width = self._dados.size[0]
        height = self._dados.size[1]

        src = np.float32(self._dados.warp_perspective)
        dst = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        self._dados.matriz_warp_perspective = cv2.getPerspectiveTransform(src, dst)
        return self._dados.matriz_warp_perspective

    @utils.timing
    def run(self, imagem, dest: estruturas.Imagem = None):
        img_processada = cv2.warpPerspective (
            imagem,
            self._dados.matriz_warp_perspective,
            (self._dados.size[0], self._dados.size[1])
        )
        if dest:
            dest.imagem_warp = deepcopy(img_processada)
        return img_processada
