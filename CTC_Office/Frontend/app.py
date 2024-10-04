from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class CTCApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CTC Office")
        button = QPushButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)



