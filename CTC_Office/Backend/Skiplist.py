class Skiplist:
    def __init__(self, graph = None, skips: dict = None):
        self.graph = graph #This will be a graph, it's the list I'm skipping over. 
        self.skips = skips #This is the dictionary of skips

    def skipRoute(self, start: int, end: int) -> list:
        #* Things that shouldn't happen
        if end >= len(self.skips):
            print("End is out of range")
            return []
        if start >= len(self.skips):
            print("Start is out of range")
            return []
        if start < 0:
            print("Start is below of range")
            return []
        if end < 0:
            print("End is below of range")
            return []
        #* Things that should happen
        rt = []
        for i in range(start, end+1):
            if i in self.skips:
                rt.extend(self.skips[i])
        return rt

if __name__ == '__main__':
    from Default import greenSkips
    from GetGreen import Green
    skips = Skiplist(Green(), greenSkips())
    print(skips.skipRoute(0, 0))   

