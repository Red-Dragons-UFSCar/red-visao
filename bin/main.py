from PyQt5.QtWidgets import QApplication
from reddragons.visao import Processamento
from reddragons.estruturas import ModelService
import sys
#from reddragons.interface import GUI_main
from reddragons.interface import GUI_video
from reddragons.utils import Logger

if __name__ == '__main__':
    model = ModelService()
    visao = Processamento(model)
    app = QApplication(sys.argv)
#    window = GUI_main(visao, model)
    window = GUI_video(visao, model)
    window.show()
    print (Logger()._fps_mean)
    sys.exit(app.exec_())
