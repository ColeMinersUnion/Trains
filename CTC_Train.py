import sys
from CTC_Office.Frontend.app import CTCApplication
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot
from TM_TC_NewArch.TrainWrapper import Train

trains = []

@pyqtSlot(list)
def trainFactory(routeInfo: list):
    trains.append(Train(routeInfo))
    trains[-1].train_model_view.show()
    trains[-1].train_controller_view.show()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = CTCApplication()
    
    
    #Emit Connect Slot
    ex.handleNewGreenTrain.connect(trainFactory)

    ex.show()

    sys.exit(app.exec())

