import cv2
import numpy as np
from reddragons import utils
from reddragons import estruturas
from copy import deepcopy


class ConverteHSV:
    @utils.timing # Essa linha printa o tempo utilizado no proscessamento
    def run (self, imagem, dest: estruturas.Imagem = None):
        """
        Converte uma imagem de RGB para HSV
        
        Args:
            self, imagem, dest
        
        """
        img_proc = cv2.cvtColor(
            np.uint8(imagem), cv2.COLOR_RGB2HSV
        )
        if dest:
            dest.imagem_hsv = deepcopy(img_proc) # Possibilita escolher o local que a imagem vai ser salva
        return img_proc
