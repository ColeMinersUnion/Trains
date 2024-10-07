import sys
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Wayside UI")

        self.setFixedSize(QSize(800,600)) #fixed size of window

        #toolbar to switch between sections, switches, crossings and have a wayside home button
        toolbar=QToolBar("Wayside Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        #toolbar buttons:
        wayside_controller=QAction("Wayside Controller", self)
        #wayside_controller.triggered.connect(self.wayside_clicked)
        toolbar.addAction(wayside_controller)

        toolbar.addSeparator()
        view_sections=QAction("View Sections", self)
        #view_sections.triggered.connect(self.view_sections_clicked)
        toolbar.addAction(view_sections)

        toolbar.addSeparator()
        signals=QAction("Signals", self)
        #action trigger here to link when button is pressed
        toolbar.addAction(signals)

        toolbar.addSeparator()
        crossings=QAction("Crossings", self)
        #action trigger here to link when button is pressed
        toolbar.addAction(crossings)

        self.setStatusBar(QStatusBar(self))


        layout=QHBoxLayout()
        #this widget will be the console/table of speed/authority/block numbers:
        layout.addWidget(Color('white'))
        #for table:
        #self.table = QtWidgets.QTableView()
        
        maintenance_mode_button=QPushButton("Enter Maintenance Mode")
        layout.addWidget(maintenance_mode_button)
        #action when maintenance mode button is clicked:
        #maintenance_mode_button.clicked.connect(self.maintenance_mode_clicked)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #updating table function here:
        #def table (self, index, role):
            #if role==Qt.ItemDataRole.DisplayRole:

            #return self._data[index.row()][index.column()]
        #def rowCount(self, index):
            #length of outer list
            #return len(self._data)
        #def colCount(self, index):
            #return len(self._data[0])
        #def maintenance_mode_clicked():
            #link to maintenance mode window
        #def view_sections_clicked():
            #link to block sections window
        #def signals_clicked():
            #link to signals window
        #def crossings_clicked():
            #link to crossings window

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