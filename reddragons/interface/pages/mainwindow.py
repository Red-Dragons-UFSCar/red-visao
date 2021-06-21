"""Modulo responsável por gerenciar as ações da pagina de seleção de entrada

fiquem a vontade para mexer nesse arquivo e testar o quanto quiserem já que ele não afeta em nada 
o nosso programa nesse momento
"""

from .main import GUI_main

from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from ..utils import ui_files
from reddragons.utils import test_device

class GUI_video(QMainWindow):
    def __init__(self, visao, model):
        super(GUI_video, self).__init__()
        loadUi(f"{ui_files}/mainwindow.ui", self)
        self.show()
        self.visao = visao
        self.model = model
        self.btnChooseCamera.clicked.connect(self._camera_handler) #botao camera
        #self.btnChooseArquivo.clicked.connect(self._arquivo_handler) #botao video
        self.btnChooseArquivo.clicked.connect(self._mudar_janela_arquivo)

    def _mudar_janela_arquivo(self):
        self.stack.setCurrentIndex(1)

    def _camera_handler(self):
        """aqui a gente da um jeito de fazer o usuario escolher uma camera
        """

        escolha = input ("Escolha uma opção de camera (0/1): ")
        escolha = int(escolha)
        
        self._config_visao(escolha)

    def _arquivo_handler(self):
        """aqui a gente pega o caminho para algum arquivo de video
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Videos (*.avi);;All files (*.*)")
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec():
            file_name = file_dialog.selectedFiles()[0]
        
        self._config_visao(file_name)        

    def _next_handler(self):
        """abre a proxima janela (main) e fecha essa
        """
        self._next = GUI_main(self.visao, self.model)
        self._next.show()
        self.close()

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
            
