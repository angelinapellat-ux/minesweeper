import tkinter as tk
from tkinter import PhotoImage

class MinesweeperUI:
    def __init__(self, root, grid):
        self.root = root
        self.grid = grid
        self.buttons = {}

        # Chargement des images
        self.images = {
            "hidden": PhotoImage(file="assets/Images/hidden.png"),
            "flag": PhotoImage(file="assets/Images/flag.png"),
            "bomb": PhotoImage(file="assets/Images/bomb.png"),
            "revealed": PhotoImage(file="assets/Images/revealed.png"),
        }

        # Images pour les chiffres
        self.num_images = {
            i: PhotoImage(file=f"assets/num_{i}.png") for i in range(9)
        }

        self.create_board()

    #Grille
    def create_board(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                btn = tk.Button(
                    self.root,
                    image=self.images["hidden"],
                    borderwidth=0,
                    command=lambda x=x, y=y: self.on_left_click(x, y)
                )

                # Clic droit
                btn.bind("<Button-3>", lambda event, x=x, y=y: self.on_right_click(x, y))

                btn.grid(row=y, column=x)
                self.buttons[(x, y)] = btn

    #Click gauche
    def on_left_click(self, x, y):
        tile = self.grid[x][y]
        result = tile.discover_tile(self.grid)

        self.update_button(x, y)

        if result == "Lose":
            self.reveal_all()

    #Click droit
    def on_right_click(self, x, y):
        tile = self.grid[x][y]
        tile.set_status()
        self.update_button(x, y)

    #Mise a jour du bouton
    def update_button(self, x, y):
        tile = self.grid[x][y]
        btn = self.buttons[(x, y)]
        status = tile.get_status()

        if status == "Hidden":
            btn.config(image=self.images["hidden"])

        elif status == "Flag":
            btn.config(image=self.images["flag"])

        elif status == "Mystery":
            btn.config(image=self.images["hidden"])  # tu peux mettre un PNG "?" si tu veux

        elif status == "Visible":
            nb = tile.get_nbmines()
            btn.config(image=self.num_images[nb])

        elif status == "Kaboom":
            btn.config(image=self.images["bomb"])

    #réveler les bombes
    def reveal_all(self):
        for (x, y), btn in self.buttons.items():
            tile = self.grid[x][y]
            if tile.get_ismine():
                btn.config(image=self.images["bomb"])

