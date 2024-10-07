import sys

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Wayside UI")

        self.setFixedSize(QSize(800,600))

        toolbar=QToolBar("Wayside Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        #toolbar buttons:
        wayside_controller=QAction("Wayside Controller", self)
        #wayside_controller.triggered.connect(self.wayside_clicked)
        toolbar.addAction(wayside_controller)
        #self.setStatusBar(QStatusBar(self))

        toolbar.addSeparator()
        toolbar.addWidget(QLabel("View Sections"))

        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Switches"))

        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Crossings"))

        #view_sections=QToolBar("View Sections", self)
        #self.addToolBar(toolbar)
        #view_sections.triggered.connect(self.sections_clicked)
        #toolbar.addAction(view_sections)
        #self.setStatusBar(QStatusBar(self))

        layout=QHBoxLayout()
        #this widget will be the console/table of speed/authority/block numbers
        layout.addWidget(Color('white'))
        layout.addWidget(QPushButton("Enter Maintenance Mode"))
        
        #maintenance_mode_button=QPushButton("Enter Maintenance Mode")
        
        
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()