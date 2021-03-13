import numpy as np
from reddragons.utils import _Estrutura


class Controle (_Estrutura):
    def __init__(self):
        self.distCruzX = 1
        self.distCruzY = 1
        self.constX = 70.0 / self.distCruzX
        self.constY = 37.5 / self.distCruzY
        self.d_cent = 7.0
        self.vec_len = 55
        self.trocouCampo = False  # interface
        self.bolaNossa1 = 1  # interface
        self.campo_maxY = 0
        self.campo_maxX = 0
        self.origem = (0, 0)
        self.d_pixel = (self.d_cent / self.constX) ** 2 + (
            self.d_cent / self.constY
        ) ** 2
        self.bola = (0, 0)
        self.simular = False  # interface
        self.duasFaces = False  # interface
        self.debug = False  # interface
        self.clientID = 0
        self.irParaAlvoFixo = False  # interface
        self.angulo_d = np.zeros(3)
        self.flagInverteuTheta = np.zeros(3)
        self.porta = "/dev/tty0"  # interface
        self.velocidade = 115200
        self.ser = 0
        self.robot = np.zeros([6, 3])
        self.adversarios = None

        self.ligado = False
        self.x_ang_d = 0
        self.y_ang_d = 0
        self.flagAtivaKalman = False  # interface
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

if __name__ == '__main__':
    instance = Controle()
    print(instance)
    instance_copy = instance.copy()
    print(instance_copy)

