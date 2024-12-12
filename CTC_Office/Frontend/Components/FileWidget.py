from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog
from PyQt6.QtCore import pyqtSignal

class filedialogdemo(QWidget):
    emitFile = pyqtSignal(str)
    def __init__(self, parent = None):
        super(filedialogdemo, self).__init__(parent)
        
        layout = QVBoxLayout()
        self.btn = QPushButton("Select a Schedule")
        self.btn.clicked.connect(self.getfile)
        
        layout.addWidget(self.btn)
        
        self.contents = QTextEdit()
        layout.addWidget(self.contents)
        self.setLayout(layout)
        self.setWindowTitle("File Dialog demo")
        
    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
            '.\\',"Schedule files (*.csv *.xlsx)")
        self.emitFile.emit(fname[0])
        print(fname)

    def update(self, response: str):
        self.contents.setText(response)
        print(response)
		
