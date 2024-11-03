from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import * 
import importlib
import copy

class Application(object):
    def __init__(self, app):
        self.app = app


        self.ui = uic.loadUi('Wayside_Controller/Hardware/Frontend/app.ui')



        self.ui.show()
        self.run()
    def run(self):
        self.app.exec()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Application(app)