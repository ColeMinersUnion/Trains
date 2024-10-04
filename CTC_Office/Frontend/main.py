from PyQt6.QtWidgets import QApplication
import sys
from app import CTCApplication

app = QApplication(sys.argv)

window = CTCApplication()
window.show()

app.exec()