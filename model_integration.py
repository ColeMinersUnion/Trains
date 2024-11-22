from TrackModel.TrackModelMain import Map

from PyQt6.QtWidgets import QApplication

import sys

def main():
    app = QApplication(sys.argv)
    tm_window = Map()   
    tm_signals = tm_window.signals
    sys.exit(app.exec())

if __name__ == "__main__":
    main()