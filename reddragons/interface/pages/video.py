"""Modulo responsável por gerenciar as ações da pagina de seleção de entrada

a funcao entrada_valida() foi colocada aqui pra facilitar nesse momento mas a ideia é ela ser movida
para o modulo utils assim que estiver devidamente implementada

fiquem a vontade para mexer nesse arquivo e testar o quanto quiserem já que ele não afeta em nada 
o nosso programa nesse momento
"""

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from typing import Union
from ..utils import ui_files

def entrada_valida (entrada: Union[int,str]) -> bool:
    """verifica se a entrada escolhida é valida

    Args:
        entrada (Union[int,str]): entrada escolhida (int para camera, str para arquivo)

    Returns:
        bool: true para entrada valuda false caso contrario
    """
    pass

class GUI_entrada(QMainWindow):
    def __init__(self):
        super(GUI_entrada, self).__init__()
        loadUi(f"{ui_files}/entrada.ui", self)
        self.show()

        self.QT_btCamera.clicked.connect(self._camera_handler) #botao camera
        self.QT_btVideo.clicked.connect(self._video_handler) #botao video
        self.QT_btNext.clicked.connect(self._next_handler) #botao next ou ok

    def _camera_handler(self) -> int:
        """aqui a gente da um jeito de fazer o usuario escolher uma camera

        Returns:
            int: numero da camera escolhida (geralmente 0 ou 1)
        """
        pass

    def _video_handler(self) -> str:
        """aqui a gente pega o caminho para algum arquivo de video

        Returns:
            str: caminho até o arquivo de video
        """
        pass

    def _next_handler(self):
        """abre a proxima janela (main) e fecha essa
        """
        pass

    def _config_visao (self, entrada) -> bool:
        """chama a funçao alterar_src ou cria um objeto de camera, 
        enfim a ideia aqui é colocar a visao pra pegar o video de onde
        a gente quer que pegue

        Returns:
            bool: sucesso na operação
        """

        if not entrada_valida: # se a entrada nao for valida ja para aqui
            return False
        
        # se for atribui a entrada para a visao aqui 
        # ...
        # ...
        return True # e depois retorna True
            
