#Used as the iterator along a route
from TrainSchedule import TrainSchedule
from Node import Node

class Train:
    def __init__(self):
        self.location = None
        self.id = None
        self.stops = []
        self.schedule = None
    