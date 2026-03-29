
# Crée une case de la grille pouvant garder ses propres information
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

# S'assure que les coordonnées utilisé ne dépassent pas hors de la grille
    def safety_limit(self, coordinate, grid_size):
        list_coordinates = []
        if not coordinate - 1 < 0:
            list_coordinates += [coordinate - 1]
        list_coordinates += [coordinate]
        if not coordinate + 1 >= grid_size:
            list_coordinates += [coordinate + 1]
        #print(list_coordinates)
        return list_coordinates

# Sélectionne les cases autour de l'instance utilisée pour d'autres modules
    def select_around(self, grid):
        selected_tiles = []
        grid_size = len(grid)
        longitude_coordinates = self.safety_limit(self.get_longitude(), grid_size)
        latitude_coordinates = self.safety_limit(self.get_latitude(), grid_size)
        for longitude in longitude_coordinates:
            for latitude in latitude_coordinates:
                # Récupère toutes les instances de case dans la zone sauf elle-même
                if not grid[longitude][latitude] == self:
                    selected_tiles.append(grid[longitude][latitude])
                    #print(grid[longitude][latitude].get_coordinate())
        return selected_tiles

# Changer l'état des cases cachées entre "Caché", "Drapeau" et "Mystère"
    def set_status(self):
        print(f"Ancien état : {self.get_status()}")
        if self.get_status() == "Hidden":
            self.status = "Flag"
        elif self.get_status() == "Flag":
            self.status = "Mystery"
        elif self.get_status() == "Mystery":
            self.status = "Hidden"
        

# Affiche le contenu de la case
    def reveal_tile(self, lose):
        if lose == True:
            self.status = "Kaboom"
        else:
            self.status = "Visible"

# Pose une mine
    def set_mine(self, grid):
        self.__ismine = True
        #print(f"{self.get_coordinate()} est maintenant une mine")
        # Sélectionne les case autour pour augmenter leur compteur de mines
        tiles_around = self.select_around(grid)
        for selected_tile in tiles_around:
            selected_tile.add_mine()

# Ajoute une mine au compteur de mines autour de l'instance de case
    def add_mine(self):
        self.nbmines += 1

# Révèle le contenue de la case sélectionnée et réagit en conséquence
    def discover_tile(self, grid):
        if self.get_status() == "Flag":
            return "Flag"
        # Renvoie "Perdu" si la case est une mine
        elif self.get_ismine() == True:
            self.reveal_tile(True)
            return "Lose"
        # Si la case n'a pas de mines autour, elle sélectionne les cases autours pour les révéler leur contenue sauf si la case est déjà révélée
        elif self.get_nbmines() == 0:
            self.reveal_tile(False)
            tiles_around = self.select_around(grid)
            for selected_tiles in tiles_around:
                if selected_tiles.get_status() == "Hidden":
                    selected_tiles.discover_tile(grid)
        # Si la case a des mines autour, elle ne fait que se découvrir
        else:
            self.reveal_tile(False)