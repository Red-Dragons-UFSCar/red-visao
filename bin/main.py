from PyQt5.QtWidgets import QApplication
from reddragons.visao import Processamento, VisaoController
from reddragons import estruturas 
import sys
from reddragons.interface import GUI_main
           
if __name__ == '__main__':
    dados = estruturas.Dados()
    visao = Processamento(dados=dados)
    controller = VisaoController(
        dados_visao=dados,
        processamento=visao
    )
    app = QApplication(sys.argv)
    window = GUI_main(visao, controller)
    window.show()
    sys.exit(app.exec_())