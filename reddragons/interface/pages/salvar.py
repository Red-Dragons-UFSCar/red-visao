import pickle

from PyQt5.QtWidgets import QMainWindow, QFileDialog

class GUI_salvar(QMainWindow):
    def __init__(self, visao, model):
        """ Construtor da classe

        Args:
            visao (): processamento da imagem
            model (Any): imagem que vai ser transformada em dados
        """
        super(GUI_salvar, self).__init__()
        self.model = model
        self.salvar()

    def salvar(self):
        """ Salva o arquivo com o nome atribuido à filename e com extensão .red
            utilizando o modulo pickle para a serialização da estrutura, ou seja,
            converte o _type_objeto em um fluxo de bytes para armazenar em um arquivo.
        """

        filename = QFileDialog.getSaveFileName(self, 'Dialog Title', filter='*.red')
        
        try:
            if filename[0].endswith('.red'):
                filename = filename[0]
            else:
                filename = f"{filename[0]}.red"
            with open(filename, "wb") as f:
                pickle.dump(self.model.dados, f)

        except (IndexError, EnvironmentError) as err:
            print(f"Falha ao salvar arquivo: {err}")
        self.close()
