from TrackModelFrontend import QApplication,Map,Testbench
import sys

def main():
    app=QApplication(sys.argv)
    map=Map()
    testbench=Testbench()
    map.show()
    testbench.show()
    sys.exit(app.exec())

main()