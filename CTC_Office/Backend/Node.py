class Node: #Also known as a track block
    def __init__(self, index : int = 0, line: str = "", section: str = "", block_length : int = 0, block_grade : int = 0, speed_limit : int = 0, infrastructure : str = "", elevation : int = 0, cumulative_elevation : int = 0, connections: list = []):
        self.index = index #!Block number
        self.infrastructure = infrastructure
        self.connections = connections
        self.line = line
        self.section = section
        self.block_length = block_length
        self.block_grade = block_grade
        self.speed_limit = speed_limit
        self.elevation = elevation
        self.cumulative_elevation = cumulative_elevation

    
    def __str__(self) -> str:
        return f"Block #{self.index} is a {self.block_type}"
    
    def pointsTo(self, blocks : list = []):
        self.connections.extend(blocks)
    
