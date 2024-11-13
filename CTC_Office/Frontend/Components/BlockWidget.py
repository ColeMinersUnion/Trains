from PyQt6.QtWidgets import QWidget

"""Block States
0 -> Unoccupied
1 -> Occupied
2 -> 
"""

class Block(QWidget):
    def __init__(self, block_index : int = 0):
        self.Node = block_index
        self.state = 0
