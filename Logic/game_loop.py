import random
from tile import Tile


def grid_setup(grid_size):
    grid = []
    for longitude in range(grid_size):
        grid_line = []
        for latitude in range(grid_size):
            grid_line += [Tile((longitude, latitude))]
        grid += [grid_line]
    return grid

def spawn_mine(grid, first_selection):
    grid_size = len(grid)
    longitude = random.randint(0, grid_size)
    latitude = random.randint(0, grid_size)
    test_mine = grid[longitude][latitude]
    if test_mine.get_ismine() == True or test_mine in grid[first_selection[0]][first_selection[1]].select_around(grid, True):
        spawn_mine(grid, first_selection)
    else:
        test_mine.set_mine(grid)

def check_victory(grid):
    for longitude in grid:
        for latitude in grid[longitude]:
            if grid[longitude][latitude].get_ismine() == False and not grid[longitude][latitude].get_status() == "Visible":
                return False
    return True


def grid_display(grid):
    for longitude in grid:
        print("grid_line")

def input_coordinate():
    longitude = int(input("Longitude: "))
    latitude = int(input("Latitude: "))
    return (longitude, latitude)


def game_loop():
    difficulty = input("Difficulty: ")
    grid = grid_setup(3)
    nbmines = 2
    first_selection = input_coordinate()
    for loop in range(nbmines):
        spawn_mine(grid, first_selection)
    while True:
        result = "Continue"
        selection = input_coordinate()
        result = grid[selection[0]][selection[1]].discover_tile()
        if result == "Perdu":
            print("Perdu")
        elif check_victory(grid) == True:
            print("Gagnée")


grid = grid_setup(3)
grid_display(grid)