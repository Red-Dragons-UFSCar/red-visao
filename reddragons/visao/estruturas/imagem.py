import numpy as np

class Imagem():
    def __init__(self):
        self.imagem_original = np.zeros((640,480,3))
        self.imagem_warp = np.zeros((640,480,3))
        self.imagem_crop = np.zeros((640,480,3))
        self.imagem_HSV = np.zeros((640,480,3))
        self.mascaras = None
        self.centroids = None
        self.centros = None
        self.adversarios = None