from datetime import datetime
from PyQt6.QtWidgets import QListWidget

class SchedulePreviewer:
    def __init__(self):
        self.trains = {}
        self.display
        self.widget = QListWidget()
    
    def update(self, id : int, block_index : int, next_stop : str, projected_arrival : datetime) -> None:
        self.trains[id] = [block_index, next_stop, projected_arrival] # I love dictionaries
        self.display()

    def display(self):
        for t in self.trains:
            print(f'Train: {self.trains[t]}')
            self.widget.addItems([f'Train: {self.trains[t]}'])

        #self.currentItemChanged.connect(self.index_changed)
        #self.currentTextChanged.connect(self.text_changed)

