import numpy as np
from reddragons import utils
from reddragons import estruturas
from reddragons.estruturas import Dados, Imagem
import cv2

class Centroides:
    """Classe resposável pro identificar os centroides dos robôs
    """
    def __init__(self, model: estruturas.ModelService):
        self._model = model
    
    @utils.timing
    def run(self, imagem, dest: Imagem = None):
        dados = self._model.dados
        centr_final = []
        
        for cor, filtro in zip(dados.cores, dados.filtros):
            contornos, _ = utils.get_contorno_cor(
                imagem, cor, filtro
            )
            centroids = np.empty((0, 3))
            for c in contornos:
                moments = cv2.moments(c)
                if dados.area_minima <= moments["m00"] <= dados.area_maxima:
                    c_x = int(moments["m10"] / moments["m00"])
                    c_y = int(moments["m01"] / moments["m00"])
                    centroids = np.vstack(
                        (centroids, np.asarray([c_x, c_y, moments["m00"]]))
                    )
            centr_final.append(np.array([centroids]))
        if dest:
            dest.centroids = centr_final
        return centr_final
