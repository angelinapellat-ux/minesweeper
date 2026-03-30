import tkinter as tk
from tkinter import PhotoImage
from Logic.game_loop import spawn_mine, grid_setup

class MinesweeperUI:
    def __init__(self, root, grid, mines):
        self.root = root
        self.grid = grid
        self.mines = mines
        self.buttons = {}
        self.first_click = True

        # Empêche la fenêtre de s'étirer
        self.root.resizable(False, False)

        # Empêche Tkinter d'ajouter des marges autour du contenu
        self.root.grid_propagate(False)
        self.root.pack_propagate(False)

        # Images principales
        self.images = {
            "Hidden": PhotoImage(file="Assets/Images/hidden.png"),
            "Flag": PhotoImage(file="Assets/Images/flag.png"),
            "Mystery": PhotoImage(file="Assets/Images/mystery.png"),
            "Kaboom": PhotoImage(file="Assets/Images/TileExploded.png"),
            "Visible": PhotoImage(file="Assets/Images/revealed.png"),
        }

        # Images des chiffres 
        self.num_images = {
            i: PhotoImage(file=f"Assets/Images/num_{i}.png") for i in range(8)
        }

        self.create_board()

    # Création de la grille
    def create_board(self):
        size = len(self.grid)

        # Configure ligne/colonne
        for i in range(size):
            self.root.grid_columnconfigure(i, weight=0)
            self.root.grid_rowconfigure(i, weight=0)

        for x in range(size):
            for y in range(size):
                btn = tk.Button(
                    self.root,
                    image=self.images["Hidden"],
                    borderwidth=0,
                    highlightthickness=0,
                    command=lambda x=x, y=y: self.on_left_click(x, y)
                )
                btn.bind("<Button-3>", lambda event, x=x, y=y: self.on_right_click(x, y))

                # Marge
                btn.grid(row=y, column=x, padx=0, pady=0, ipadx=0, ipady=0)

                self.buttons[(x, y)] = btn

    # Clic gauche
    def on_left_click(self, x, y):
        tile = self.grid[x][y]

        # Placement des mines au premier clic
        if self.first_click:
            for _ in range(self.mines):
                spawn_mine(self.grid, (x, y))
            self.first_click = False

        result = tile.discover_tile(self.grid)
        self.update_all_buttons()

        # Défaite
        if result == "Lose":
            self.reveal_all()
            self.game_over_popup()
            return

        # Victoire
        if self.check_victory():
            self.victory_popup()

    # Clic droit
    def on_right_click(self, x, y):
        tile = self.grid[x][y]
        tile.set_status()
        self.update_button(x, y)

    # Mise à jour d’un bouton
    def update_button(self, x, y):
        tile = self.grid[x][y]
        btn = self.buttons[(x, y)]
        status = tile.get_status()

        if status in ["Hidden", "Flag", "Mystery", "Kaboom"]:
            btn.config(image=self.images[status])
            return

        if status == "Visible":
            nb = tile.get_nbmines()

            # Case vide
            if nb == 0:
                btn.config(image=self.images["Visible"])
            else:
                # Décalage de 1 car num_0.png correspond visuellement à "1"
                btn.config(image=self.num_images[nb - 1])

    # Mise à jour de toute la grille
    def update_all_buttons(self):
        for (x, y) in self.buttons:
            self.update_button(x, y)

    # Révéler toutes les bombes
    def reveal_all(self):
        for (x, y), btn in self.buttons.items():
            tile = self.grid[x][y]
            if tile.get_ismine():
                btn.config(image=self.images["Kaboom"])

    # Popup Game Over
    def game_over_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        popup.geometry("200x120")
        popup.resizable(False, False)

        tk.Label(popup, text="💥 Game Over !", font=("Arial", 14)).pack(pady=10)

        tk.Button(
            popup,
            text="Rejouer",
            font=("Arial", 12),
            command=lambda: (popup.destroy(), self.restart_game())
        ).pack(pady=5)

        tk.Button(
            popup,
            text="Quitter",
            font=("Arial", 12),
            command=self.root.destroy
        ).pack(pady=5)

    # Popup Victoire
    def victory_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Victoire !")
        popup.geometry("200x120")
        popup.resizable(False, False)

        tk.Label(popup, text="🎉 Victoire !", font=("Arial", 14)).pack(pady=10)

        tk.Button(
            popup,
            text="Rejouer",
            font=("Arial", 12),
            command=lambda: (popup.destroy(), self.restart_game())
        ).pack(pady=5)

        tk.Button(
            popup,
            text="Quitter",
            font=("Arial", 12),
            command=self.root.destroy
        ).pack(pady=5)

    # Vérifie si toutes les cases non-minées sont révélées
    def check_victory(self):
        for row in self.grid:
            for tile in row:
                if not tile.get_ismine() and tile.get_status() != "Visible":
                    return False
        return True

    # Redémarrer une partie
    def restart_game(self):
        size = len(self.grid)
        new_grid = grid_setup(size)

        # Supprimer les anciens boutons
        for btn in self.buttons.values():
            btn.destroy()

        self.grid = new_grid
        self.buttons = {}
        self.first_click = True

        self.create_board()
