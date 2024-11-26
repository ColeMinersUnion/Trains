import sys
from CTC_Office.Frontend.app import CTCApplication
from PyQt6.QtWidgets import QApplication
from TM_TC_NewArch.TrainWrapper import TrainWrapper

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = CTCApplication()
    
    #Emit Connect Slot

    ex.show()

    sys.exit(app.exec())

