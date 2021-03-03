from PyQt5.QtWidgets import QApplication
from reddragons.visao import Processamento
import sys
from reddragons.interface import GUI_main

           
if __name__ == '__main__':
    visao = Processamento()
    app = QApplication(sys.argv)
    window = GUI_main(visao)
    window.show()
    sys.exit(app.exec_())