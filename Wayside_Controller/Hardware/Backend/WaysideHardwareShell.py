import importlib
import copy


class WaysideShell:
    def __init__(self):
        self.plc = None
        self.region = {"Line": "Green", "Region": (41, 77)}
        self.occupancy = [False for i in range(36)]
        self.authority = [True for i in range(28)]
        self.switch_57 = False
        self.switch_63 = False
        self.maintenance = [False for i in range(36)]
        self.signal_57 = False

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

    def update_plc(self):
        self.plc.update_occupancy(self.occupancy)
        self.plc.update_authority()
        self.authority = copy.deepcopy(self.plc.authority)
        self.switch_57 = copy.deepcopy(self.plc.switch_57)
        self.switch_63 = copy.deepcopy(self.plc.switch_63) 
        self.signal_57 = copy.deepcopy(self.plc.signal_57)

    def suggest_switch(self, switch_suggestion):
        result = self.plc.update_switches(switch_suggestion)
        self.plc.update_authority()
        self.authority = copy.deepcopy(self.plc.authority)
        self.switch_57 = copy.deepcopy(self.plc.switch_57)
        self.switch_63 = copy.deepcopy(self.plc.switch_63) 
        self.signal_57 = copy.deepcopy(self.plc.signal_57)
        return result

    def update(self, tm_occupancy):
        self.occupancy = tm_occupancy

    def maintenance_blocks(self, blocks):
        print(blocks)
