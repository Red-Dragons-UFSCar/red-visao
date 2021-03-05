from typing import Optional
from copy import deepcopy

from reddragons.visao import utils
from reddragons import estruturas


class Corte:
    def __init__ (self, dados):
        self._dados = dados

    @utils.timing
    def run(self, fonte, dest: Optional[estruturas.Imagem] = None) -> int:
        imagem = fonte

        sup_esquerdo = self._dados.corte[0]
        imagem[0 : sup_esquerdo[1], 0 : sup_esquerdo[0], :] = 0
        imagem[0 : self._dados.corte[1][1], self._dados.corte[1][0] : 640, :] = 0
        imagem[self._dados.corte[2][1] : 480, 0 : self._dados.corte[2][0], :] = 0
        imagem[self._dados.corte[3][1] : 480, self._dados.corte[3][0] : 640, :] = 0

        if dest:
            dest.imagem_crop = deepcopy(imagem)
        return imagem
