import numpy as np
from reddragons.utils import _Estrutura

class Imagem(_Estrutura):
    def __init__(self):
        self.imagem_original = np.zeros((640, 480, 3))
        self.imagem_warp = np.zeros((640, 480, 3))
        self.imagem_crop = np.zeros((640, 480, 3))
        self.imagem_hsv = np.zeros((640, 480, 3))
        self.mascaras = None
        self.centroids = None
        #centroisds [0] bola
        #centroids [1] = bola
        #centroids [2] centros dos aliados
        print('Centroids', self.centroids)
        self.centros = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        #suposicao centros aliados [1][2][3]
        #suposica entros aliados [i] = [meiox, meioy, ang]
        self.adversarios = None
        #suposicao centros adversarios [1][2][3]
        #suposicao centros adversarios [i] = [meiox, meioy, ang]
