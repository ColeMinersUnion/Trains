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

    
        blue_plc = getattr(plc, file_name)         
        self.plc = blue_plc()
        self.plc.say_hi()
        return True


    def dispatch(self, speed, authority, switch):
        self.tm.dispatch(speed, authority)
        self.plc.dispatch(switch)


    def get_blocks(self):
        return self.plc.get_blocks()
    
    def set_occupancy(self, occupancy):
        self.plc.update_track(occupancy)
    
    def maintenance_blocks(self, blocks):
        return self.plc.update_maintenance(blocks)