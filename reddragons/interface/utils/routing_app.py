from PyQt5.QtWidgets import QMainWindow, QStackedWidget

class RoutingApp (QMainWindow):
    def __init__ (self):
        super(RoutingApp, self).__init__()
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        self.show()

    def fit(self, widget):
        fmg = widget.frameGeometry()
        size = (fmg.width(), fmg.height())
        self.setFixedSize(*size)

    def push_widget (self, widget):
        now = self.stack.currentWidget()
        if now is not None:
            self.stack.removeWidget(now)
            now.destroy()
        self.fit(widget)
        idx = self.stack.addWidget(widget)
        self.stack.setCurrentIndex(idx)
    
