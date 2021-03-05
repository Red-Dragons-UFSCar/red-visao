import copy
import threading
import time

from reddragons.visao import captura, utils, services
from reddragons import estruturas
from reddragons.visao.logger import Logger


class Processamento:
    def __init__(self, *args, **kwargs):
        self._init_data(*args, **kwargs)
        self._init_services(*args, **kwargs)
        self.started = False
        self.cam = captura.Captura()
        self.read_lock = threading.Lock()
        self.verbose = False
        self.cam.iniciar()
        self.recalcular()

    def iniciar(self):
        if self.started:
            return None
        self.started = True
        self.thread = threading.Thread(target=self.main_loop, args=())
        self.thread.start()
        return self

    def _init_data (self, *args, **kwargs):
        self.imagem = estruturas.Imagem()
        self.dados = kwargs.get('dados', estruturas.Dados())
        self.dados_controle = estruturas.Controle()

    def _init_services(self, *args, **kwargs):
        self._perspectiva = services.Perspectiva(self.dados)
        self._corte = services.Corte(self.dados)
        self._converte_hsv = services.ConverteHSV()
        self._centroides = services.Centroides(self.dados)
        self._centros = services.Centros(self.dados)

    def mudar_verbose(self):
        self.verbose = not self.verbose

    def processar(self):
        err = False
        tempo = {}
        tempo['inicial'] = time.time()
        self.conseguiu, self.img = self.cam.read()

        if not self.conseguiu:
            Logger().erro("Sem frame da captura")
            self.cam.stop()
            self.cam = captura.Captura()
            self.cam.iniciar()
            Logger().flag("Câmera reiniciada")

            return (True, None)

        tempo['camera'] = time.time()

        imagem = copy.deepcopy(self.imagem)
        imagem.imagem_original = copy.deepcopy(self.img)
        tempo['copia'] = time.time()

        img_warp, tempo['warp'] = self._perspectiva.run(imagem.imagem_original, imagem)
        img_corte, tempo['corte'] = self._corte.run(img_warp, imagem)
        img_hsv, tempo['hsv'] = self._converte_hsv.run(img_corte, imagem)
        _, tempo['centroids'] = self._centroides.run(img_hsv, imagem)
        _, tempo['centros'] = self._centros.run(imagem.centroids, imagem)
        imagem.adversarios = imagem.centroids[5]

        with self.read_lock:
            self.imagem = copy.deepcopy(imagem)
        tempo['final'] = time.time()

        return err, tempo

    def main_loop(self):
        i_frame = 0
        while self.started:
            self.conseguiu, self.img = self.cam.read()
            err, tempo = self.processar()
            if err: continue
            i_frame+=1

            if self.verbose:
                Logger().tempo(i_frame, *tempo.values())    

    @utils.read_lock
    def recalcular(self):
        self.dados.matriz_warp_perspective = self._perspectiva.calcula()
    
    def stop(self):
        self.started = False
        self.thread.join()
        self.cam.stop()
    
    def __exit__(self, exec_type, exc_value, traceback):
        self.cam.stop()
