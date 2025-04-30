from datetime import datetime
from PyQt6.QtWidgets import QListWidget, QWidget


class SchedulePreviewer(QWidget):
    def __init__(self):
        super().__init__()
        self.trains = {}
        #self.display
        self.widget = QListWidget()
    
    def update(self, id : int, block : str, next_stop : str, projected_arrival : datetime) -> None:
        self.trains[id] = [block, next_stop, projected_arrival.strftime("%H:%M:%S")] # I love dictionaries
        self.display()

    def display(self):
        for t in self.trains:
            print(f'Train: {self.trains[t]}')
            self.widget.addItems([f'Train: {self.trains[t]}'])
    
    def clear(self):
        self.widget.clear()
        
    

        #self.currentItemChanged.connect(self.index_changed)
        #self.currentTextChanged.connect(self.text_changed)

