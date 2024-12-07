from PyQt6.QtWidgets import QListWidget, QWidget

class OccupancyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.trains = []
        self.widget = QListWidget()

    def update(self, trainList: list) -> None:
        self.trains = trainList
        self.display()
        
    def display(self):
        self.widget.clear()
        for t in self.trains:
            self.widget.addItems([f'Train: {t[0]}\t {t[1]}'])
            print(f'Train: {t[0]}\tBlock: {t[1]}')