import numpy as np
from reddragons.utils import _Estrutura

class Imagem(_Estrutura):
    def __init__(self):
        self.imagem_original = np.zeros((640, 480, 3))
        self.imagem_warp = np.zeros((640, 480, 3))
        self.imagem_crop = np.zeros((640, 480, 3))
        self.imagem_hsv = np.zeros((640, 480, 3))
        self.mascaras = None
        self.centroids = None #imagem centroids[0] = bola
        self.centros = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        #centros aliados [1][2][3]
        #centros aliados [i] = [meiox, meioy, ang]
        self.adversarios = None
        #centros adversarios [1][2][3]
        #centros adversarios [i] = [meiox, meioy, ang]
