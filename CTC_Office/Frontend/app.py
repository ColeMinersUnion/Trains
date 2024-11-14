#from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel
from Components.SchedulePreviewer import SchedulePreviewer
from datetime import datetime
import time



class CTCApplication(QMainWindow):
    def __init__(self, Office = None):
        super().__init__()
        self.Office = Office
        self.scheduleWidget = SchedulePreviewer()
        self.button = QPushButton("Move")
        self.layout = QVBoxLayout()
        self.main = QWidget()
        self.button_state = True
        self.addTrain = QLineEdit(parent=self)
        self.submit = QPushButton("Submit")
        self.submit_state = True
        self.clear = QPushButton("Clear")
        self.clear_state = True
        self.breakBlok = QLineEdit(parent=self)
        self.submitBreak = QPushButton("Break Block")
        self.break_state = True
        self.fixBlock = QLineEdit(parent=self)
        self.submitFix =QPushButton("Fix Block")
        self.fix_state = True
        self.Automatic = QLineEdit(parent=self)
        self.Auto = QPushButton("Schedule File")
        self.auto_state = True

        #!TestBench Stuff
        self.switchState = QLabel()
        self.speed = QLabel()
        self.auth = QLabel()

        self.setWindowTitle("CTC Office")
        
        self.button.setCheckable(True)
        self.button.released.connect(self.onClick)
        self.button.setChecked(self.button_state)

        self.submit.setCheckable(True)
        self.submit.released.connect(self.onSubmit)
        self.submit.setChecked(self.submit_state)

        self.clear.setCheckable(True)
        self.clear.released.connect(self.onClear)
        self.clear.setChecked(self.clear_state)

        self.submitBreak.setCheckable(True)
        self.submitBreak.released.connect(self.onBreak)
        self.submitBreak.setChecked(self.break_state)

        self.submitFix.setCheckable(True)
        self.submitFix.released.connect(self.onFix)
        self.submitFix.setChecked(self.fix_state)

        self.Auto.setCheckable(True)
        self.Auto.released.connect(self.onAuto)
        self.Auto.setChecked(self.auto_state)

        lbl = QLabel()
        lbl.setText("Testbench Information")

        lbl1 = QLabel()
        lbl1.setText("Moving Trains and seeing the track Schedule")
        self.layout.addWidget(lbl1)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.scheduleWidget.widget)

        lbl2 = QLabel()
        lbl2.setText("Adding and removing trains")
        self.layout.addWidget(lbl2)
        self.layout.addWidget(self.addTrain)
        self.layout.addWidget(self.submit)
        self.layout.addWidget(self.clear)

        lbl3 = QLabel()
        lbl3.setText("Automatic Mode")
        self.layout.addWidget(lbl3)
        self.layout.addWidget(self.Automatic)
        self.layout.addWidget(self.Auto)

        lbl4 = QLabel()
        lbl4.setText("Breaking the track")
        self.layout.addWidget(lbl4)
        self.layout.addWidget(self.breakBlok)
        self.layout.addWidget(self.submitBreak)

        lbl5 = QLabel()
        lbl5.setText("Fixing the track")
        self.layout.addWidget(lbl5)
        self.layout.addWidget(self.fixBlock)
        self.layout.addWidget(self.submitFix)
        


        self.layout.addWidget(lbl)
        self.layout.addWidget(self.speed)
        self.layout.addWidget(self.auth)
        self.layout.addWidget(self.switchState)

        self.main.setLayout(self.layout)

        self.setCentralWidget(self.main)
    
    def onClick(self):
        id = self.Office.nextID - 1
        #print(id)
        train = self.Office.Schedule.trains[id]
        if(train.move()):
            self.scheduleWidget.update(train.id, str(train.location), train.Next_Stop, datetime.now())

        self.speed.setText(f'Speed: {train.speedy()/1.609344} Mph')
        self.auth.setText(f'Authority {train.auth()/1609.344} Miles')
        if train.Next_Stop == 'Station B':
            self.switchState.setText("Up")
        else:
            self.switchState.setText("Down")

        self.button_state = self.button.isChecked()

    def onSubmit(self):
        txt = self.addTrain.text()
        if(txt == 'Station B' or txt == 'Station C'):
            self.Office.addTrain([txt])
        else:
            self.addTrain.setText("That station Does not exist, try again.")
        self.submit_state = self.submit.isChecked()

    
    def onClear(self):
        self.scheduleWidget.trains = {}
        self.scheduleWidget.clear()
        self.clear_state = self.clear.isChecked()

    def onBreak(self):
        txt = self.breakBlok.text()
        if(self.Office.breakTrack(int(txt))):
            self.breakBlok.setText(f'Block {int(txt)} is now broken. ')
        else:
            self.breakBlok.setText("That block does not exist, try again.")
        self.break_state = self.submitBreak.isChecked()

    
    def onFix(self):
        txt = self.fixBlock.text()
        if(self.Office.fixTrack(int(txt))):
            self.fixBlock.setText(f'Block {int(txt)} is now fixed. ')
        else:
            self.fixBlock.setText("That block does not exist or was not broken, try again.")
        self.fix_state = self.submitBreak.isChecked()
        
    def onAuto(self):
        fn = self.Automatic.text()
        try:
            #print(os.getcwd())
            file = open(fn)
            txt = file.readline()
            self.Office.addTrain([txt])
            self.Automatic.setText(f'File {fn} has been read')
            self.autoMove()
            file.close()
        except:
            self.Automatic.setText(f'File {fn} could not be found')
        self.auto_state = self.Auto.isChecked()


    def autoMove(self):
        id = self.Office.nextID - 1
        train = self.Office.Schedule.trains[id]

        while(train.move()):
            self.scheduleWidget.update(train.id, str(train.location), train.Next_Stop, datetime.now())

            self.speed.setText(f'Speed: {train.speedy()}')
            self.auth.setText(f'Authority {train.auth()}')
            if train.Next_Stop == 'Station B':
                self.switchState.setText("Up")
            else:
                self.switchState.setText("Down")

            time.sleep(train.waitTime(speedUp=True))





        
    
    

         



