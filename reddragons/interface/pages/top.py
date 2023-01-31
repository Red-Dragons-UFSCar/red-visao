from reddragons.interface.utils import RoutingApp

class VisaoTop(RoutingApp):
    
    def __init__ (self, visao, model):
        """ Construtor da classe

        Args:
            visao (): processamento da imagem
            model (): imagem que vai ser transformada em dados
        """
        super(VisaoTop, self).__init__()
        self.visao = visao
        self.model = model
    def closeEvent(self, event) -> None:
        """ Tenta fechar o evento atual

        Args:
            event (): evento atual
        """
        try:
            self.visao.stop()
        except:
            return
