from typing import Optional
from copy import deepcopy

from reddragons import utils
from reddragons import estruturas


class Corte:
    def __init__ (self, model: estruturas.ModelService):
        self._model = model

    @utils.timing
    def run(self, fonte, dest: Optional[estruturas.Imagem] = None) -> int:
        dados = self._model.dados
        imagem = deepcopy(fonte)

        sup_esquerdo = dados.corte[0]
        imagem[0 : sup_esquerdo[1], 0 : sup_esquerdo[0], :] = 0
        imagem[0 : dados.corte[1][1], dados.corte[1][0] : 640, :] = 0
        imagem[dados.corte[2][1] : 480, 0 : dados.corte[2][0], :] = 0
        imagem[dados.corte[3][1] : 480, dados.corte[3][0] : 640, :] = 0

        if dest:
            dest.imagem_crop = deepcopy(imagem)
        return imagem
