import numpy as np


class Dados:
    def __init__(self):
        self.size = np.asarray([640, 480, 3])
        self.warp_perspective = np.asarray([[10, 10], [630, 10], [10, 470], [630, 470]])
        self.matriz_warp_perspective = np.zeros((3, 3))
        self.cruzetas = np.asarray([[10, 10], [630, 10], [10, 470]])
        self.corte = np.asarray([[40, 40], [600, 40], [40, 440], [600, 440]])
        self.cores = np.asarray(
            [
                [[10, 10, 10], [170, 200, 200]],
                [[30, 30, 30], [40, 40, 40]],
                [[50, 50, 50], [60, 60, 60]],
                [[70, 70, 70], [80, 80, 80]],
                [[90, 90, 90], [100, 100, 100]],
                [[90, 90, 90], [100, 100, 100]],
            ]
        )
        self.filtros = np.asarray(
            [
                # Tipo do filtro (Nenhum, Abertura, Fechamento)
                # Formato do Kernel
                # Valor do Kernel
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]
        )

        self.area_minima = 20
        self.area_maxima = 200

        self.ang_corr = 90
