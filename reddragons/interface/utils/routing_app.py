from PyQt5.QtWidgets import QMainWindow, QStackedWidget

class RoutingApp (QMainWindow):
    def __init__ (self):
        super(RoutingApp, self).__init__()
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        self.hist = []
        self.pages = {}
        self.show()

    def register (self, name, widget):
        index = len(self.pages)
        self.pages.update({
            name: (index, widget)
        })
        self.stack.addWidget(widget)
        return index

    def fit(self, widget):
        fmg = widget.frameGeometry()
        size = (fmg.width(), fmg.height())
        print(size)
        self.resize(*size)

    def push_page (self, page):
        try:
            idx, widget = self.pages[page]
        except Exception as e:
            print('falha ao encontrar pagina')
            raise e
        self.stack.setCurrentIndex(idx)
        self.fit(widget)
        self.hist.append(idx)
    
    def back (self):
        if len(self.hist) < 2:
            return -1
        self.hist.pop()

        idx = self.hist[-1]
        widget = dict(self.pages.values())[idx]
        self.stack.setCurrentIndex(idx)
        self.fit(widget)
        return idx