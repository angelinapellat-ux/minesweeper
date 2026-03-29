import tkinter as tk
from Logic.game_loop import grid_setup
from Graphic.interface import MinesweeperUI
from Logic.difficulty import DIFFICULTY_CONFIG
import math

def start_game(size, mines):
    root = tk.Tk()
    root.title("Démineur")

    tile_size = 32
    root.geometry(f"{size * tile_size}x{size * tile_size}")
    root.resizable(False, False)

    grid = grid_setup(size)
    MinesweeperUI(root, grid, mines)

    root.mainloop()

def menu():
    root = tk.Tk()
    root.title("Choisir la difficulté")
    root.geometry("380x220")
    root.resizable(False, False)

    tk.Label(root, text="Sélectionne une difficulté :", font=("Arial", 14)).pack(pady=20)

    for name, config in DIFFICULTY_CONFIG.items():
        max_tiles = config["MAX_TILES"]
        max_mines = config["MAX_MINES"]

        size = int(math.sqrt(max_tiles))  # conversion 

        tk.Button(
            root,
            text=name,
            font=("Arial", 12),
            width=15,
            command=lambda s=size, m=max_mines: (root.destroy(), start_game(s, m))
        ).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    menu()
