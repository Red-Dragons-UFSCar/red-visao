import math
import numpy as np

from reddragons import utils
from reddragons import estruturas
from reddragons.estruturas import Dados, Imagem

class Centros():
    """Classe responsável por identificar os centros e ângulos dos robôs
    """
    def __init__ (self, model: estruturas.ModelService):
        """Construtor da classe

        Args:
            model (estruturas.ModelService): modelo de dados a ser utilizado
        """

        self._model = model
        self._centros = []

    @utils.timing
    def run (self, centroids, dest: Imagem = None, corr: bool = True):
        """executa o algoritmo de identificação de centros e angulos

        Args:
            centroids (np.ndarray): candidatos a centroides
            dest (Imagem, optional): instancia de imagem para salar o resultado. Defaults to None.
            corr (bool, optional): correcao de angulo. Defaults to True.

        Returns:
            np.ndarray: centros e angulos dos robos no formato (meio_x, meio_y, angulo)
        """

        self._centros = self._calcula_centros (centroids)
        if dest:
            if corr and dest.centros:
                self._correcao(dest.centros)
            dest.centros = self._centros
        return self._centros

    def _centro_robo(self, princ, sec):
        """identifica o centro do robo a partir dos centros dos marcadores

        Args:
            princ ((int,int)): posicao do marcador principal (x,y)
            sec ((int,int)): posicao do marcador secundario (x,y)

        Returns:
            (int,int,float): (meio_x, meio_y, angulo)
        """
        meio_x = (princ[0] + sec[0]) / 2
        meio_y = (princ[1] + sec[1]) / 2
        ang = math.atan2(princ[1] - sec[1], princ[0] - sec[0])
        angulo = ang + (self._model.dados.ang_corr)*np.pi/180
        return meio_x, meio_y, angulo

    def _calcula_centros(self, centroids):
        """identifica os centros e angulos de todos os robos

        Args:
            centroids (np.ndarray): centroides encontrados na imagem

        Returns:
            np.ndarray: centros e angulos dos robos no formato (meio_x, meio_y, angulo)
        """
        centros = self._model.imagem.centros
        for i_sec in range(2, 5): #para cada marcador secundario
            menor = 10000.0
            for principal in centroids[1][0]: #para cada candidato a centroide principal
                try:
                    for secundario in centroids[i_sec][0]: #para cada candidato a centroide secundario
                        dist = math.hypot(
                            principal[0] - secundario[0], principal[1] - secundario[1]
                        )
                        if dist < 30 < menor: #30 é a maior distancia aceitavel entre um marcador principal e secundario
                            menor = dist
                            m_x, m_y, ang = self._centro_robo(principal, secundario)
                            centros[i_sec - 2][0] = m_x
                            centros[i_sec - 2][1] = m_y
                            centros[i_sec - 2][2] = ang
                except ValueError:
                    pass
        return centros

    def _correcao (self, ref):
        """aplica correcao de angulos

        Args:
            ref (np.ndarray): referencia para correcao (geralmente medida anterior)
        """
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
