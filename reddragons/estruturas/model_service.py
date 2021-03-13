from . import models
from reddragons.utils import read_lock

class ModelService (object):
    def __init__ (self):
        self._imagem = models.imagem.Imagem()
        self._controle = models.controle.Controle()
        self._dados = models.dados.Dados()

    @property
    def imagem (self):
        return self._imagem
    @imagem.setter
    @read_lock
    def imagem (self, data):
        self._imagem = data

    @property
    def controle (self):
        return self._controle
    @controle.setter
    @read_lock
    def controle (self, data):
        self._controle = data

    @property
    def dados (self):
        return self._dados
    @dados.setter
    @read_lock
    def dados (self, data):
        self._dados = data
