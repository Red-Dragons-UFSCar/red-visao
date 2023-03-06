from PyQt5.QtWidgets import QApplication
import sys
from reddragons.interface import GUI_video, VisaoTop
from reddragons.utils import Logger
from reddragons.visao import Processamento
from reddragons.estruturas import ModelService

from reddragons.controle import ControleEstrategia

def init_app ():
    model = ModelService()
    visao = Processamento(model)

    app = VisaoTop(visao, model)
    app.push_widget(GUI_video(app))
    return app

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = init_app()
    window.show()
    print (Logger()._fps_mean)
    sys.exit(app.exec_())
