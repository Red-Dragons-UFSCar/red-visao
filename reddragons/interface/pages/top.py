from reddragons.interface.utils import RoutingApp

class VisaoTop(RoutingApp):
    def __init__ (self, visao, model):
        super(VisaoTop, self).__init__()
        self.visao = visao
        self.model = model
