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
        
        for idx, (cor, filtro) in enumerate(zip(dados.cores, dados.filtros)):
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
            objetivo = 3 if idx == 1 else 1
            if centroids.shape[0] < objetivo:
                if dest.centroids is not None and dest.centroids[idx].shape[1] >= objetivo:
                    if objetivo == 1:
                        centroids = dest.centroids[idx][0]
                    else:
                        perto = list(dest.centroids[idx][0])
                        for centr in centroids:
                            perto = sorted(perto, key=lambda x: np.linalg.norm((x[:2]-centr[:2])))
                            perto[0] = centr
                        perto = np.asarray(perto)
                        centroids = perto
            centr_final.append(np.array([centroids]))

        if dest:
            dest.centroids = centr_final
        return centr_final