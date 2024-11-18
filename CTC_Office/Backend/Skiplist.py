#Enforcing a default route. ALternative to route from 

class Skiplist:
    def __init__(self, graph = None, skips: dict = None):
        self.graph = graph #This will be a graph, it's the list I'm skipping over. 
        self.skips = skips #This is the dictionary of skips

    def skipRoute(self, start: int, end: int) -> list:
        #* Things that shouldn't happen
        if(start == end):
            return []
        if end >= len(self.skips):
            return []
        if start >= len(self.skips):
            return []
        if start < 0:
            return []
        if end < 0:
            return []
        #* Things that should happen
        rt = []
        for i in range(start, end):
            if i in self.skips:
                rt.extend(self.skips[i])
        return rt
    
    
