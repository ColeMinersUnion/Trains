import importlib
import copy

class WaysideShell:
    def __init__(self):
        self.plc = None
    def upload_plc(self, file_name):
        try:
            plc = importlib.import_module(file_name)
            # Now you can use the imported module

        except ImportError:
            print(f"Error: Module '{file_name}' not found.")

    
        blue_plc = getattr(plc, file_name)         
        self.plc = blue_plc()
        self.plc.say_hi()

    def get_blocks(self):
        return self.plc.get_blocks()
    
    def maintenance_blocks(self, blocks):
        return self.plc.update_maintenance(blocks)