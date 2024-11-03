from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import * 
import importlib
import copy
import sys
sys.path.insert(0, 'Wayside_Controller/Hardware/Backend')
from WaysideHardwareShell import WaysideShell

class Application(object):
    def __init__(self, app):
        self.app = app
        self.wayside = WaysideShell()

        self.ui = uic.loadUi('Wayside_Controller/Hardware/Frontend/app.ui')

        self.ui.plc_upload_button.clicked.connect(self.plc_file_dialog)

       
        self.ui.show()
        self.run()
        
    def plc_file_dialog(self):
                file_dialog = QFileDialog()
                selected_file = None
                file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
                if file_dialog.exec():
                    selected_file = file_dialog.selectedFiles()[0]
                    self.wayside.upload_plc(selected_file)
                else:
                    print("No file selected")

    def run(self):
        self.app.exec()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Application(app)