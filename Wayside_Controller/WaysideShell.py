import importlib
import copy
from application import CTC
from application import TrackModel

class WaysideShell:
    def __init__(self):
        self.plc = None
        self.ctc = CTC()
        self.tm = TrackModel()

    def upload_plc(self, file_name):
        try:
            plc = importlib.import_module(file_name)

        except ImportError:
            print(f"Error: Module '{file_name}' not found.")
            return False

    
        input_plc = getattr(plc, file_name)         
        self.plc = input_plc()
        self.plc.say_hi()
        return True

    