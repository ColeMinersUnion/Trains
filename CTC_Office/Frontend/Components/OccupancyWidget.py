from PyQt6.QtWidgets import QListWidget, QWidget

class OccupancyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.trains = []
        self.widget = QListWidget()

    def update(self, trainList: list) -> None:
        self.trains = trainList
        
    def display(self):
        self.widget.clear()
        for t in self.trains:
            self.widget.addItems([f'Train: {t.id}\tBlock: {t.block}'])
            print(f'Train: {t.id}\tBlock: {t.block}')