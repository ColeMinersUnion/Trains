from PyQt6.QtWidgets import QApplication
import sys
import os
from app import CTCApplication
import importlib

print(os.getcwd())
sys.path.insert(1, os.getcwd() + '/CTC_Office/Backend')
#!sys.path.insert(1, os.getcwd() + '\CTC_Office\Backend')
for i, s in enumerate(sys.path):
    print(f'Path {i}: {s}')

CTC_Module = importlib.import_module('CTC')




Office = CTC_Module.CTC_Office()
Office.addBlueLine()
Office.addTrain(['Station C'])


app = QApplication(sys.argv)

window = CTCApplication(Office)
window.show()

app.exec()