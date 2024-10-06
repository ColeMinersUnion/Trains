class Train:
    speed = None
    auth = None
    block = None


class Switch:
    number = None
    connections = None
    state = None

class Signal:
    number = None
    state = None

class Crossing:
    number = None
    state = None


class WaysideShell:
    blocks = {}
    switches = []
    crossings = []
    signals = []

    def __init__(self, blk, swc, cro, sig):
        self.blocks = blk
        self.switches = swc
        self.crossings = cro
        self.signals = sig

    def update_blocks():
        

    

    

