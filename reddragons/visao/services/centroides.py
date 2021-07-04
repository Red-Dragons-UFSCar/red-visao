import numpy as np
from reddragons import utils
from reddragons.estruturas import Dados, Imagem
import cv2

class Centroides:
    """Classe resposável pro identificar os centroides dos robôs
    """
    def __init__(self, dados: Dados):
        self._dados = dados
    
    @utils.timing
    def run(self, imagem, dest: Imagem = None):
        centr_final = []
        for cor, filtro in zip(self._dados.cores, self._dados.filtros):
            contornos, _ = utils.get_contorno_cor(
                imagem, cor, filtro
            )
            centroids = np.empty((0, 3))
            for c in contornos:
                moments = cv2.moments(c)
                if self._dados.area_minima <= moments["m00"] <= self._dados.area_maxima:
                    c_x = int(moments["m10"] / moments["m00"])
                    c_y = int(moments["m01"] / moments["m00"])
                    centroids = np.vstack(
                        (centroids, np.asarray([c_x, c_y, moments["m00"]]))
                    )
            centr_final.append(np.array([centroids]))
        if dest:
            dest.centroids = centr_final
        return centr_final
