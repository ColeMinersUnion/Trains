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

       
        self.ui.show()
        self.run()
        

    def run(self):
        self.app.exec()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Application(app)