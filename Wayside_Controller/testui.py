import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # Adds a title
        self.setWindowTitle("Wayside Controller")
        #Set vertical layout
        self.setLayout(qtw.QVBoxLayout())

        # Create a label
        my_label = qtw.QLabel("Upload PLC")
        self.layout().addWidget(my_label)
        self.show()
    
app = qtw.QApplication([])
mw = MainWindow()

app.exec_()