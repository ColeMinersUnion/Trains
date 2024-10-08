import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#from WaysideShell import *
#from WaysidePLC import *

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


        layout=QVBoxLayout()
        #this widget will be the console/table of speed/authority/block numbers:
        layout.addWidget(Color('white'))
        #for table:
        
        
        manual_mode_button=QPushButton("Enter Maintenance Mode")
        layout.addWidget(manual_mode_button)
        #action when manual mode button is clicked:
        #manual_mode_button.clicked.connect(self.manual_mode_clicked)

        plc_button=QPushButton("PLC Upload")
        layout.addWidget(plc_button)
        #action when 
        
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
        #def manual_mode_clicked():
            #link to manual mode window
        #def view_sections_clicked():
            #change table
        #def signals_clicked():
            #change table
        #def crossings_clicked():
            #change table

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