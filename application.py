from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import * 
from WaysideShell import WaysideShell
import importlib
class Application(object):
    def __init__(self, app):
        self.app = app
        self.shell = WaysideShell()
        self.plc = None
        self.ui = uic.loadUi('WaysideShell.ui')

        # Sets the maintenance states to unchecked, they need to start checked for the checkboxes to activate
        for index in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(index)
            item.setCheckState(QtCore.Qt.Unchecked)

        # Connects the buttons to their functions
        self.ui.plc_upload_button.clicked.connect(self.upload_plc)
        self.ui.listWidget.itemChanged.connect(self.ctc_maintenance)
        self.blocks = []
        self.auth = []
        self.plc_uploaded = False
        # Setup the periodic update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(1000)  # Updates every 1 second 

        self.ui.show()
        self.run()
    def run(self):
        self.app.exec_()

    def upload_plc(self):
        file_name = self.ui.plc_file_input.text()

        try:
            plc = importlib.import_module(file_name)
            # Now you can use the imported module

        except ImportError:
            print(f"Error: Module '{file_name}' not found.")

    
        blue_plc = getattr(plc, file_name)         
        self.plc = blue_plc()
        self.plc.say_hi()
        self.ui.wayside_log.append("PLC uploaded")
        self.plc_uploaded = True
    
    def ctc_maintenance(self):
        maint_blocks = []
        for index in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(index)
            maint_blocks.append(item.checkState() == QtCore.Qt.Checked)
        


    def update_blocks(self):
        self.blocks, self.auth = self.plc.get_blocks()
        for i in range(len(self.blocks)):
            self.ui.wayside_block_table.setItem(i,0, QTableWidgetItem(str(self.blocks[i])))
            self.ui.wayside_block_table.setItem(i,1, QTableWidgetItem(str(self.auth[i])))
            self.ui.tm_block_table.setItem(i,0, QTableWidgetItem(str(self.blocks[i])))
            self.ui.tm_block_table.setItem(i,1, QTableWidgetItem(str(self.auth[i])))
    
    def update_ui(self):
        if self.plc_uploaded:
            self.update_blocks()
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Application(app)
