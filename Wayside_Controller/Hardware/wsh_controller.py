from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal

class WaysideHardwareController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        self.view.wsh_int_sw58.connect(self.model.toggle_sw58)
        self.view.wsh_int_sw62.connect(self.model.toggle_sw62)
        self.view.wsh_int_sig58.connect(self.model.toggle_sig58)
        self.view.wsh_int_sig62.connect(self.model.toggle_sig62)
        self.view.wsh_int_connect.connect(self.model.connect)

        self.model.wsh_tm_sw58.connect(self.view.update_sw58)
        self.model.wsh_tm_sw62.connect(self.view.update_sw62)
        self.model.wsh_tm_sig58.connect(self.view.update_sig58)
        self.model.wsh_tm_sig62.connect(self.view.update_sig62)

        
        self.model.wsh_tm_authority.connect(self.view.update_authority_table)

