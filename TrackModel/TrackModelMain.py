from TrackModelFrontend import Map,Testbench
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app=QApplication(sys.argv)
    map=Map()
    testbench=Testbench()
    map.show()
    testbench.show()
    sys.exit(app.exec())

main()