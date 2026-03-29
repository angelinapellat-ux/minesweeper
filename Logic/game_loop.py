import random
from Logic.tile import Tile


# Crée la grille sous forme d'instances de clase dans des listes dans des listes
def grid_setup(grid_size):
    grid = []
    # Crée autant de sous-listes que de lignes dans la grille
    for longitude in range(grid_size):
        grid_line = []
        # Crée autant d'instances de case que de colonnes dans la grille
        for latitude in range(grid_size):
            grid_line += [Tile((longitude, latitude))]
        grid += [grid_line]
    return grid

# Pose au hasard les mines en début de partie
def spawn_mine(grid, first_selection):
    grid_size = len(grid)
    longitude = random.choice(grid)
    latitude = random.choice(longitude)
    test_mine = latitude
    safe_start_zone = [grid[first_selection[0]][first_selection[1]]] + grid[first_selection[0]][first_selection[1]].select_around(grid)
    # Rappelle la fonction s'il y a déjà une mine sur l'emplacement choisi ou si la mine sera placé trop proche de la première sélection
    if test_mine.get_ismine() == True or test_mine in safe_start_zone:
        spawn_mine(grid, first_selection)
        print("spawn_mine rappelé")
    else:
        test_mine.set_mine(grid)
        print(f"mine placé à {test_mine.get_coordinate()}")

# Vérifie si toutes les case sans mines sont découvertes pour déclarer la victoire
def check_victory(grid):
    for longitude in grid:
        for latitude in longitude:
            if latitude.get_ismine() == False and not latitude.get_status() == "Visible":
                return False
    return True

# Affiche la grille ligne par ligne sous forme de symbole
def grid_display(grid):
    for longitude in grid:
        grid_line = []
        for latitude in longitude:
            # L'état de la case et sont contenue sont tout deux affichés pour faciliter la programmation
            if latitude.get_status() == "Hidden":
                symbol = "-"
            elif latitude.get_status() == "Flag":
                symbol = "F"
            elif latitude.get_status() == "Mystery":
                symbol = "?"
            elif latitude.get_status() == "Visible":
                symbol = " "
            elif latitude.get_status() == "Kaboom":
                symbol = "X"
            if latitude.get_ismine() == True:
                symbol += "x"
            else:
                symbol += f"{latitude.get_nbmines()}"
            grid_line += [symbol]
        print(grid_line)

# Demande les coordonnée de la case sélectionnée par le joueur
def input_coordinate():
    longitude = int(input("Longitude: "))
    latitude = int(input("Latitude: "))
    return (longitude-1, latitude-1)

# Demande si la case sélectionnée doit être découverte ou changer d'état
def input_action():
    action = input("Découvrir (D) ; Changer l'état (E) : ")
    return action

# Jeu
def game():
    # Difficulté pas encore implémenté
    difficulty = input("Difficulty: ")
    grid = grid_setup(10)
    nbmines = 6
    grid_display(grid)
    first_selection = input_coordinate()
    # Pose le nombre de mines définie pour la partie
    for loop in range(nbmines):
        spawn_mine(grid, first_selection)
    grid[first_selection[0]][first_selection[1]].discover_tile(grid)
    # Boucle principale du jeu
    while True:
        grid_display(grid)
        result = "Continue"
        selection = input_coordinate()
        action = input_action()
        if action == "D":
            result = grid[selection[0]][selection[1]].discover_tile(grid)
            if result == "Flag":
                print("Un drapeau ne peut pas être découvert, veuillez enlever le drapeau")
            elif result == "Lose":
                print("Perdu")
                grid_display(grid)
                break
            elif check_victory(grid) == True:
                print("Gagnée")
                grid_display(grid)
                break
        elif action == "E":
            grid[selection[0]][selection[1]].set_status()

if __name__ == "__main__":
    game()
