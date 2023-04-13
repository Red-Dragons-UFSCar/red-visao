from copy import deepcopy

import cv2
import numpy as np
from reddragons import utils
from reddragons import estruturas


class Perspectiva():
    def __init__ (self, model: estruturas.ModelService):
        self._model = model


    # A função calcula pega os pontos definidos para a transformação de perspectiva e realiza as operações matematicas
    # Os pontos foram definidos em reddragons/interface/pages/perspectivas.py
    def calcula(self):
        width = self._model.dados.size[0]
        height = self._model.dados.size[1]

        src = np.float32(self._model.dados.warp_perspective)
        dst = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        self._model.dados.matriz_warp_perspective = cv2.getPerspectiveTransform(src, dst) # Chama a função do Open CV que realiza essa transformação
        return self._model.dados.matriz_warp_perspective

    @utils.timing#calcula o tempo gasto com a operação

    # Essa função aplica a transformação a imagem
    def run(self, imagem, dest: estruturas.Imagem = None):
        img_processada = cv2.warpPerspective (
            imagem,
            self._model.dados.matriz_warp_perspective,
            (self._model.dados.size[0], self._model.dados.size[1])
        )
        if dest:
            dest.imagem_warp = deepcopy(img_processada) # Opção de escolher onde a imagem vai ser salva
        return img_processada
