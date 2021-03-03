from PyQt5.QtWidgets import QApplication
from reddragons.visao import processamento
import sys
from reddragons.interface import GUI_main

           
if __name__ == '__main__':
    visao = processamento.processamento()
    app = QApplication(sys.argv)
    window = GUI_main(visao)
    window.show()
    sys.exit(app.exec_())