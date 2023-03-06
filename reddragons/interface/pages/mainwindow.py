"""Modulo responsável por gerenciar as ações da pagina de seleção de entrada

fiquem a vontade para mexer nesse arquivo e testar o quanto quiserem já que ele não afeta em nada 
o nosso programa nesse momento
"""

from .padrao import GUI_padrao
from .diretorio import GUI_diretorio
from .camera import GUI_camera

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from ..utils import ui_files
from reddragons.utils import test_device




class GUI_video(QMainWindow):
    def __init__(self, app):
        super(GUI_video, self).__init__()
        loadUi(f"{ui_files}/mainwindow.ui", self)
        self.show()
        self.app = app
        self.visao = app.visao
        self.model = app.model
        self.btnChooseCamera.clicked.connect(self._camera_handler) #botao camera
        self.btnChooseArquivo.clicked.connect(self._janela_diretorio)

    def callback_diretorio (self, diretorio: str):
        """funcao chamada depois do ok da janela do diretorio

        Args:
            diretorio (str): diretorio escolhido
        """
        res = self._config_visao(diretorio)
        if not res:
            self.app.push_widget(self)

    def _janela_diretorio(self):
        """abre a janela de escolha do diretorio
        """
        self.app.push_widget(GUI_diretorio(self.app, self.callback_diretorio))

    def _mudar_janela_arquivo(self): # essa aq era usada antes mas nao foi apagada
        self.stack.setCurrentIndex(1)

    def _camera_handler(self):
        """Aqui a gente da um jeito de fazer o usuario escolher uma camera
        """
        self.app.push_widget(GUI_camera(self.callback_diretorio))      

    def _next_handler(self):
        """abre a proxima janela (main) e fecha essa
        """
        self.app.visao.iniciar()
        self.app.push_widget(GUI_padrao(self.app))

    def _config_visao (self, entrada) -> bool:
        """chama a funçao alterar_src ou cria um objeto de camera, 
        enfim a ideia aqui é colocar a visao pra pegar o video de onde
        a gente quer que pegue

        Returns:
            bool: sucesso na operação
        """

        if not test_device(entrada): # se a entrada nao for valida ja para aqui
            print("Erro ao selecionar entrada, por favor tente novamente")
            return False
        self.visao.alterar_src(entrada) # se for atribui a entrada para a visao aqui 
        self._next_handler()
        return True # e depois retorna True
            
