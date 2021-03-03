import numpy as np
from reddragons.visao.logger import *
from inspect import currentframe, getframeinfo
import serial

class estruturaDados():
    def __init__(self):
        self.size = np.asarray([640, 480, 3])
        self.warpPerspective = np.asarray([[10, 10], [630, 10], [10, 470], [630, 470]])
        self.M_warpPerspective = np.zeros((3,3))
        self.cruzetas = np.asarray([[10, 10], [630, 10], [10, 470]])
        self.corte = np.asarray([[40, 40], [600, 40], [40, 440], [600, 440]])
        self.cores = np.asarray([
            [[10, 10, 10], [170,200,200]], 
            [[30, 30, 30], [40,40,40]], 
            [[50, 50, 50], [60,60,60]], 
            [[70, 70, 70], [80,80,80]], 
            [[90, 90, 90], [100,100,100]],
            [[90, 90, 90], [100,100,100]]
        ])
        self.filtros = np.asarray([ 
        #Tipo do filtro (Nenhum, Abertura, Fechamento)
        #Formato do Kernel
        #Valor do Kernel
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        
        self.AreaMinimo = 20
        self.AreaMaxima = 200
        
        self.angCorr = 90

class estruturaImagem():
    def __init__(self):
        self.imagem_original = np.zeros((640,480,3))
        self.imagem_warp = np.zeros((640,480,3))
        self.imagem_crop = np.zeros((640,480,3))
        self.imagem_HSV = np.zeros((640,480,3))
        self.mascaras = None
        self.centroids = None
        self.centros = None
        self.adversarios = None

class estruturaControle():
    def __init__(self):
        self.distCruzX = 1
        self.distCruzY = 1
        self.constX = 70.0 / self.distCruzX 
        self.constY =  37.5 / self.distCruzY
        self.d_cent = 7.0
        self.vec_len = 55
        self.trocouCampo = False  #interface
        self.bolaNossa1 = 1 #interface
        self.campo_maxY = 0
        self.campo_maxX = 0
        self.origem = (0,0)
        self.d_pixel = (self.d_cent / self.constX) ** 2 + \
                        (self.d_cent/self.constY) ** 2
        self.bola = (0,0)
        self.simular = False #interface
        self.duasFaces = False #interface
        self.debug = False #interface
        self.clientID = 0 
        self.irParaAlvoFixo = False #interface 
        self.angulo_d = np.zeros(3)
        self.flagInverteuTheta = np.zeros(3)
        self.porta = '/dev/tty0' #interface
        self.velocidade = 115200 
        self.ser = 0
        self.robot = np.zeros([6, 3])
        self.adversarios = None
        
        
        self.ligado = False
        self.x_ang_d = 0 
        self.y_ang_d = 0
        self.flagAtivaKalman = False #interface
        self.Kp1 = 0
        self.Kd1 = 0
        self.Ki1 = 0
        self.Kp2 = 0
        self.Kd2 = 0
        self.Ki2 = 0
        self.Kp3 = 0
        self.Kd3 = 0
        self.Ki3 = 0
        self.Pjogar = True
        self.Pinicial = False
        self.Pparar = False
        
        
                   
