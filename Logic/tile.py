

class Tile:
    def __init__(self, coordinate, status="Hidden", ismine=False, nbmines=0):
        self.coordinate = coordinate
        self.status = status
        self.__ismine = ismine
        self.nbmines = nbmines

    def get_coordinate(self):
        return self.coordinate

    def get_longitude(self):
        return self.coordinate[0]
    
    def get_latitude(self):
        return self.coordinate[1]

    def get_status(self):
        return self.status
    
    def get_ismine(self):
        return self.__ismine
    
    def get_nbmines(self):
        return self.nbmines

    def safety_limit(self, coordinate, grid_size):
        if coordinate < 0:
            coordinate = 0
        elif coordinate >= grid_size:
            coordinate = grid_size - 1
        print(coordinate)
        return coordinate
    
    def select_around(self, grid, center, selected_tiles = []):
        grid_size = len(grid)
        for longitude in range(self.safety_limit(self.get_longitude()-1, grid_size), 
                               self.safety_limit(self.get_longitude()+2, grid_size)):
            for latitude in range(self.safety_limit(self.get_latitude()-1, grid_size), 
                                  self.safety_limit(self.get_latitude()+2, grid_size)):
                if center == True or not grid[longitude][latitude] == self:
                    selected_tiles += [grid[longitude][latitude]]
                    for i in selected_tiles:
                        print(i.get_coordinate())
        return selected_tiles

    def set_status(self):
        if self.get_status() == "Hidden":
            self.status == "Flag"
        elif self.get_status() == "Flag":
            self.status == "Mystery"
        elif self.get_status() == "Mystery":
            self.status == "Hidden"

    def reveal_tile(self, lose):
        if lose == True:
            self.status = "Kaboom"
        else:
            self.status = "Visible"

    def set_mine(self, grid):
        self.ismine = True
        tiles_around = self.select_around(grid, False)
        for selected_tile in tiles_around:
            selected_tile.add_mine()

    def add_mine(self):
        self.nbmines += 1
        
    def discover_tile(self, grid):
        if self.get_status() == "Flag":
            return "Flag"
        elif self.get_ismine() == True:
            self.reveal_tile(True)
            return "Lose"
        elif self.get_nbmines() == 0:
            self.reveal_tile(False)
            tiles_around = self.select_around(grid, False)
            for selected_tiles in tiles_around:
                if selected_tiles.get_status() == "Hidden":
                    selected_tiles.discover_tile(grid)
        else:
            self.reveal_tile(False)