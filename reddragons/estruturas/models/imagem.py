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
        self.centros = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.adversarios = None
