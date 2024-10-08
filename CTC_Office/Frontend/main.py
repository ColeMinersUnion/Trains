from PyQt6.QtWidgets import QApplication
import sys
import os
from app import CTCApplication
import importlib

print(os.getcwd())
sys.path.insert(1, os.getcwd() + '/CTC_Office/Backend')
for i, s in enumerate(sys.path):
    print(f'Path {i}: {s}')

from CTC import CTC_Office




Office = CTC_Office()
Office.addBlueLine()
Office.addTrain(['Station C'])


app = QApplication(sys.argv)

window = CTCApplication(Office)
window.show()

app.exec()