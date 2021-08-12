from reddragons.interface.utils import RoutingApp

class VisaoTop(RoutingApp):
    def __init__ (self, visao, model):
        super(VisaoTop, self).__init__()
        self.visao = visao
        self.model = model
    def closeEvent(self, event) -> None:
        try:
            self.visao.stop()
        except:
            return
