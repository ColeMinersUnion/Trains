from PyQt6.QtWidgets import QApplication
import sys
import os
from app import CTCApplication
import importlib



app = QApplication(sys.argv)

window = CTCApplication()
window.show()

app.exec()