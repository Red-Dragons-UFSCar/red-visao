import math

from reddragons import utils
from reddragons import estruturas
from reddragons.estruturas import Dados, Imagem

class Centros():

    def __init__ (self, model: estruturas.ModelService):
        self._model = model
        self._centros = []

    @utils.timing
    def run (self, centroids, dest: Imagem = None, corr: bool = True):

        self._centros = self._calcula_centros (centroids)
        if dest:
            if corr and dest.centros:
                self._correcao(dest.centros)
            dest.centros = self._centros
        return self._centros

    def _centro_robo(self, princ, sec):
        meio_x = (princ[0] + sec[0]) / 2
        meio_y = (princ[1] + sec[1]) / 2
        ang = math.atan2(princ[1] - sec[1], princ[0] - sec[0])
        angulo = ang + self._model.dados.ang_corr
        return meio_x, meio_y, angulo

    def _calcula_centros(self, centroids):
        centros = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i_sec in range(2, 5):
            menor = 10000.0
            for principal in centroids[1][0]:
                try:
                    for secundario in centroids[i_sec][0]:
                        dist = math.hypot(
                            principal[0] - secundario[0], principal[1] - secundario[1]
                        )
                        if dist < menor:
                            menor = dist
                            m_x, m_y, ang = self._centro_robo(principal, secundario)
                            centros[i_sec - 2][0] = m_x
                            centros[i_sec - 2][1] = m_y
                            centros[i_sec - 2][2] = ang
                except ValueError:
                    pass
        return centros

    def _correcao (self, ref):
        if abs(self._centros[0][2] - ref[0][2]) < 0.30:
            self._centros[0][2] = (
                self._centros[0][2]
                - (self._centros[0][2] - ref[0][2]) * 0.85
            )

        if abs(self._centros[1][2] - ref[1][2]) < 0.30:
            self._centros[1][2] = (
                self._centros[1][2]
                - (self._centros[1][2] - ref[1][2]) * 0.85
            )

        if abs(self._centros[2][2] - ref[2][2]) < 0.30:
            self._centros[2][2] = (
                self._centros[2][2]
                - (self._centros[2][2] - ref[2][2]) * 0.85
            )
