import copy
import threading
import time

from reddragons.visao import captura, services
from reddragons import utils
from reddragons.utils.logger import Logger

class Processamento:
    def __init__(self, model):
        self.started = False
        self.verbose = False
        self.cam = None

        self._model = model
        self.read_lock = threading.Lock()

        self._init_services()
        self.recalcular()

    def _init_services(self):
        self._perspectiva = services.Perspectiva(self._model)
        self._corte = services.Corte(self._model)
        self._converte_hsv = services.ConverteHSV()
        self._centroides = services.Centroides(self._model)
        self._centros = services.Centros(self._model)

    def alterar_src(self, src):
        """ Verifica a necessidade de recomeçar a captura de imagem.
            Se necessário captura uma próxima imagem, senão, gera uma
            recursão.

        Args:
            src (any): fonte a qual provê a captura da imagem
        """
        recomeca = self.started
        if recomeca:
            self.stop()

        if self.cam is None:
            self.cam = captura.Imagem(src)
        else:
            self.cam.alterar_src(src)

        if recomeca:
            self.iniciar()

    def mudar_verbose(self):
        """ Inverte o sinal booleano da variável verbose
        """
        self.verbose = not self.verbose

    def iniciar(self):
        """ Inicia o processamento da fonte de video caso exista e já
            não tenha sido iniciado.

        Raises:
            Exception: exceção caso não exista fonte de video disponível
        """
        if self.cam is None:
            raise Exception ("Tentativa de iniciar processamento sem fonte de video")
        if self.started:
            return None
        self.started = True
        self.thread = threading.Thread(target=self.main, args=())
        self.thread.start()
        return self

    def processar(self):
        """Processamento reponsável por transformar a imagem em dados

        Returns:
            temp(dict): dicionario com os tempos utilizados pelo processamento
            err(bool): booleano com a constatação se houve ou não um erro
        """
        err = False
        tempo = {}
        tempo['inicial'] = time.time()
        self.conseguiu, self.img = self.cam.read()

        if not self.conseguiu:
            Logger().erro("Sem frame da captura")
            self.cam.stop()
            self.cam = captura.Imagem()
            self.cam.iniciar()
            Logger().flag("Câmera reiniciada")

            return (True, None)

        tempo['camera'] = time.time()

        imagem = self._model.imagem.copy()
        imagem.imagem_original = copy.deepcopy(self.img)
        tempo['copia'] = time.time()

        _, tempo['warp'] = self._perspectiva.run(imagem.imagem_original, imagem)
        _, tempo['corte'] = self._corte.run(imagem.imagem_warp, imagem)
        _, tempo['hsv'] = self._converte_hsv.run(imagem.imagem_crop, imagem)
        _, tempo['centroids'] = self._centroides.run(imagem.imagem_hsv, imagem)
        _, tempo['centros'] = self._centros.run(imagem.centroids, imagem)
        imagem.adversarios = imagem.centroids[5]

        with self.read_lock:
            self._model.imagem = copy.deepcopy(imagem)
        tempo['final'] = time.time()

        return err, tempo

    def main(self):
        """ Main que inicia a captura, a leitura e
            o processamento da imagem enquanto necessário.
        """
        i_frame = 0
        while self.started:
            self.conseguiu, self.img = self.cam.read()
            err, tempo = self.processar()
            if err: continue
            i_frame+=1

            if self.verbose:
                Logger().tempo(i_frame, *tempo.values())

    def recalcular(self):
        """ Recalcula a perspectiva dos dados
        """
        dados = self._model.dados
        dados.matriz_warp_perspective = self._perspectiva.calcula()

        with self.read_lock:
            self.dados = dados

    def stop(self):
        """ Realiza a parada na captura da imagem
        """
        self.started = False
        self.thread.join()
        self.cam.stop()

    def sincronizar_controle(self):
        """ Calcula e retorna os dados necessários pelo controle

        Returns:
            dados_controle: dados necessários e requisitados pelo controle
        """
        dados_controle = self._model.controle
        dados = self.dados

        dados_controle.distCruzX = abs(dados.cruzetas[0][0] - dados.cruzetas[1][0])
        dados_controle.distCruzY = abs(dados.cruzetas[0][1] - dados.cruzetas[2][1])
        dados_controle.constX = 70.0 / dados_controle.distCruzX
        dados_controle.constY = 37.5 / dados_controle.distCruzY

        dados_controle = self.sincronizar_controle_dinamico(dados_controle)
        self._model.controle = dados_controle
        return dados_controle

    def sincronizar_controle_dinamico(self, dados_controle=None):
        """ Calcula e retorna os dados necessários pelo controle de forma dinâmica,
            ou seja, leva em conta situações inesperadas. Como quando a bola ou o
            robô não foi detectado corretamente, utilizando assim, a ultima posição.

        Args:
            dados_controle (): dados necessários e requisitados pelo controle. Defaults to None.

        Returns:
            dados_controle: ''', porém com as alterações necessárias realizadas. 
        """
        if dados_controle is None:
            dados_controle = copy.deepcopy(self._model.controle)
        imagem = self._model.imagem

        if imagem.centroids[0] == []:
            Logger().erro("Bola não detectada. Usando última posição")
        else:
            try:
                dados_controle.bola = (
                    imagem.centroids[0][0][0][0],
                    imagem.centroids[0][0][0][1],
                )
            except ValueError:
                Logger().erro(str(imagem.centroids[0]))

        # Logger().variavel('dados_controle.bola', dados_controle.bola)

        dados_controle.robot = imagem.centros
        # Logger().variavel('dados_controle.robot', dados_controle.robot)
        err = utils.checar_erro_centroide(imagem.centros)
        for i in range(3):
            if err[i] != 0:
                dados_controle.robot[i] = self._model.controle.robot[i]
                #Logger().erro(
                    #"Robô #" + str(i) + " não detectado. Usando última posição"
                #)
        # Logger().variavel('dados_controle.robot', dados_controle.robot)

        dados_controle.adversarios = imagem.adversarios[0]
        # Logger().variavel('dados_controle.adversarios', dados_controle.adversarios.T)

        self._model.controle = dados_controle

        return dados_controle

    def __exit__(self, exec_type, exc_value, traceback):
        """Encerra a execução da camera

        Args:
            exec_type (_type_): classe da exceção
            exc_value (_type_): instância da exceção
            traceback (_type_): objeto de rastreamento que rastreia a última função chamada na pilha
        """
        self.cam.stop()
