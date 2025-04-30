from PyQt6.QtWidgets import QListWidget, QWidget, QLabel

class MaintenanceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.lbl = QLabel("Blocks\t")
        self.widget = QListWidget()

    def update(self, blockList: list) -> None:
        self.blocks = blockList
        self.display()
        
    def display(self):
        self.widget.clear()
        for b in self.blocks:
            self.widget.addItems([f'Block: {b[0]}\t {b[1]}'])
            print(f'Train: {b[0]}\tBlock: {b[1]}')