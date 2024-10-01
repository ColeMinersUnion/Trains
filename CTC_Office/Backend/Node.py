class Node: #Also known as a track block
    def __init__(self, index : float = 0.0, line: str = "", section: str = "", block_length : int = 0, block_grade : int = 0, speed_limit : int = 0, infrastructure : str = "", elevation : int = 0, cumulative_elevation : int = 0, connections: list = []):
        self.index = int(index) #!Block number
        self.infrastructure = infrastructure
        self.connections = connections
        self.line = line
        self.section = section
        self.block_length = block_length
        self.block_grade = block_grade
        self.speed_limit = speed_limit
        self.elevation = elevation
        self.cumaltive_elevation = cumulative_elevation

    def __init__(self, blockDictionary : dict = {}):
        print("Dict Constructor")
        self.section = blockDictionary["Section"]
        self.index = int(blockDictionary["Block Number"])
        self.block_length = blockDictionary["Block Length (m)"]
        self.block_grade = blockDictionary["Block Grade (%)"]
        self.speed_limit = blockDictionary["Speed Limit (Km/Hr)"]
        self.infrastructure = blockDictionary["Infrastructure"]
        self.elevation = blockDictionary["ELEVATION (M)"]
        self.cumaltive_elevation = blockDictionary["CUMALTIVE ELEVATION (M)"]
        self.connections = []
        

    
    def __str__(self) -> str:
        return f"Block #{self.index} is a {self.infrastructure}. It is part of section {self.section}, it is {self.block_length} meters long with a {self.block_grade}% grade. " \
        f"The elevation is {self.elevation} with cum. elevation {self.cumaltive_elevation} and a speed limit of {self.speed_limit}"
    
    def pointsTo(self, blocks : list = []):
        self.connections.extend(blocks)
    
