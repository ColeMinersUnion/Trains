from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal

class WaysideHardwareController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        self.view.ws_int_sw58.connect(self.model.toggle_sw58)
        self.view.ws_int_sw62.connect(self.model.toggle_sw62)
        self.view.ws_int_sig58.connect(self.model.toggle_sig58)
        self.view.ws_int_sig62.connect(self.model.toggle_sig62)

        