from copy import deepcopy

from reddragons.visao import Captura, Logger, Processamento, estruturas, utils


class VisaoController:
    def __init__ (self, **kwargs):
        self._controle: estruturas.Controle = kwargs.get('dados_controle', estruturas.Controle())
        self._dados:estruturas.Dados = kwargs.get('dados_visao', estruturas.Dados())
        self._captura: Captura = kwargs.get('captura')
        self._processamento: Processamento = kwargs.get('processamento')

    @property
    @utils.read_lock
    def controle(self):
        return self._controle

    @controle.setter
    @utils.read_lock
    def controle(self, attr):
        utils.update_instance(self._controle, attr)

    @property
    @utils.read_lock
    def dados(self):
        return vars(self._dados)

    @dados.setter
    @utils.read_lock
    def dados(self, attr):
        utils.update_instance(self._dados, attr)
        self._processamento.recalcular()

    @utils.read_lock
    def read_imagem (self, tipo: str):
        return getattr(self._processamento.imagem, tipo)

    @property
    def src (self):
        return self._captura.src

    @src.setter
    @utils.read_lock
    def src (self, novo_src):
        self._processamento.stop()
        self._captura.alterar_src(novo_src)
        self._processamento.iniciar()

    def mudar_verbose(self):
        self._processamento.mudar_verbose()

    def sincronizar_controle(self):
        dados_controle = self._controle
        dados = self.dados

        dados_controle.distCruzX = abs(dados.cruzetas[0][0] - dados.cruzetas[1][0])
        dados_controle.distCruzY = abs(dados.cruzetas[0][1] - dados.cruzetas[2][1])
        dados_controle.constX = 70.0 / dados_controle.distCruzX
        dados_controle.constY = 37.5 / dados_controle.distCruzY

        dados_controle = self.sincronizar_controle_dinamico(dados_controle)
        self._controle = dados_controle
        return dados_controle

    def sincronizar_controle_dinamico(self, dados_controle=None):
        if dados_controle is None:
            dados_controle = deepcopy(self._controle)
        imagem = self._processamento.imagem

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
                dados_controle.robot[i] = self._controle.robot[i]
                Logger().erro(
                    "Robô #" + str(i) + " não detectado. Usando última posição"
                )
        # Logger().variavel('dados_controle.robot', dados_controle.robot)

        dados_controle.adversarios = imagem.adversarios[0]
        # Logger().variavel('dados_controle.adversarios', dados_controle.adversarios.T)

        self._controle = dados_controle

        return dados_controle
