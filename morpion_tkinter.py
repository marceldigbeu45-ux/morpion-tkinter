# Morpion - version console et graphique avec tkinter

import random
import tkinter as tk
from tkinter import messagebox


# LOGIQUE DU JEU

# a)
def init_board() -> list[list[str]]:
    # Cree un plateau 3x3 vide.
    return [["", "", ""], ["", "", ""], ["", "", ""]]


# b)
def print_board(board: list[list[str]]) -> None:
    # Affiche les indices de colonnes.
    print("   0   1   2")

    # On parcourt les lignes du plateau.
    for i, row in enumerate(board):
        symbols = [cell if cell != "" else " " for cell in row]
        print(f"{i}  " + " | ".join(symbols))

        # On affiche une separation entre les lignes.
        if i < len(board) - 1:
            print("  ---+---+---")


# c)
def is_free(board: list[list[str]], row: int, col: int) -> bool:
    # Retourne True si la case est vide.
    return board[row][col] == ""


# d)
def make_move(board: list[list[str]], row: int, col: int, player: str) -> None:
    # Place le symbole du joueur si la case est libre.
    if is_free(board, row, col):
        board[row][col] = player


# e)
def check_winner(board: list[list[str]], player: str) -> bool:
    # n represente la taille du plateau.
    n = len(board)

    # Verification des lignes.
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Verification des colonnes.
    for col in range(n):
        if all(board[row][col] == player for row in range(n)):
            return True

    # Verification de la diagonale principale.
    if all(board[i][i] == player for i in range(n)):
        return True

    # Verification de l'autre diagonale.
    if all(board[i][n - 1 - i] == player for i in range(n)):
        return True

    return False


# f)
def is_full(board: list[list[str]]) -> bool:
    # Retourne True si toutes les cases sont occupees.
    return all(cell != "" for row in board for cell in row)


# g)
def get_player_move(board: list[list[str]], player: str) -> tuple[int, int]:
    # On recommence tant que le coup n'est pas valide.
    while True:
        try:
            row = int(input(f"Joueur {player} - ligne (0-2) : "))
            col = int(input(f"Joueur {player} - colonne (0-2) : "))
        except ValueError:
            print("Entre des nombres entiers.")
            continue

        # La case doit exister dans la grille.
        if row not in range(3) or col not in range(3):
            print("Choisis des valeurs entre 0 et 2.")
            continue

        # La case doit etre libre.
        if not is_free(board, row, col):
            print("Cette case est deja occupee.")
            continue

        return row, col


def get_ai_move(board: list[list[str]]) -> tuple[int, int]:
    # L'IA choisit une case libre au hasard.
    free_cells = [(r, c) for r in range(3) for c in range(3) if is_free(board, r, c)]
    return random.choice(free_cells)

#Question 1.2

def play_game() -> None: # On cree un plateau vide.
    board = init_board()

    # X commence.
    current_player = "X"

    # On affiche le plateau.
    print_board(board)

    # Boucle principale.
    while True:
        row, col = get_player_move(board, current_player) #selon les fenêtre vides , le joueur 
        make_move(board, row, col, current_player) #choisit une fenêtre 
        print_board(board)

        if check_winner(board, current_player):
            print(f"Le joueur {current_player} a gagne !")
            return

        if is_full(board):
            print("Egalite !")
            return

        current_player = "O" if current_player == "X" else "X"


def run_console_games() -> None:
    # Permet de relancer plusieurs parties.
    while True:
        play_game()
        replay = input("Voulez-vous rejouer ? (o/n) : ").strip().lower()
        if replay not in ("o", "oui"):
            break


# INTERFACE GRAPHIQUE TKINTER

class MorpionApp:
    # Classe principale du jeu graphique.

    def __init__(self, root: tk.Tk):
# root = fenetre principale tkinter
        self.root = root
        self.root.title("Morpion")
        self.root.configure(bg="#f4f8ff")
        self.root.resizable(False, False)

# Variables du jeu (fenêtre du jeu)
        self.board = init_board()
        self.current_player = "X"
        self.vs_ai = False
        self.human_symbol = "X"
        self.game_over = False

# Couleurs
        self.COLORS = {
            "bg": "#f4f8ff",
            "surface": "#ffffff",
            "border": "#c9d8f0",
            "X": "#1d4ed8",
            "O": "#2563eb",
            "btn": "#dbeafe",
            "btn_hover": "#bfdbfe",
            "text": "#0f172a",
            "muted": "#64748b",
        }

        self._build_ui()

    def _build_ui(self) -> None:
    # Zone du titre
        zone_titre = tk.Frame(self.root, bg=self.COLORS["bg"], pady=16)
        zone_titre.pack(fill="x")

        tk.Label(
            zone_titre,
            text="MORPION",
            font=("Courier New", 24, "bold"),
            fg=self.COLORS["X"],
            bg=self.COLORS["bg"],
        ).pack()

        # Texte du tour
        self.turn_text = self._make_text(self.root, "Tour du joueur X", self.COLORS["X"], 11, padx=0, pady=6)
        self.turn_text.pack()

        # Zone du plateau
        zone_plateau = tk.Frame(self.root, bg=self.COLORS["border"], padx=3, pady=3)
        zone_plateau.pack(padx=20, pady=10)

        # Grille de boutons
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for r in range(3):
            for c in range(3):
                bouton_case = tk.Button(
                    zone_plateau,
                    text="",
                    font=("Courier New", 30, "bold"),
                    width=2,
                    height=1,
                    bg=self.COLORS["surface"],
                    fg=self.COLORS["text"],
                    relief="flat",
                    cursor="hand2",
                    command=lambda r=r, c=c: self._on_click(r, c),
                )
                bouton_case.grid(row=r, column=c, padx=2, pady=2, ipadx=10, ipady=8)
                bouton_case.bind("<Enter>", lambda e, b=bouton_case: self._on_hover(b, True))
                bouton_case.bind("<Leave>", lambda e, b=bouton_case: self._on_hover(b, False))
                self.buttons[r][c] = bouton_case

        # Zone des boutons du bas
        zone_boutons = tk.Frame(self.root, bg=self.COLORS["bg"], pady=10)
        zone_boutons.pack()

        self._make_button(zone_boutons, "Nouvelle partie", self._reset_game).pack(side="left", padx=6)

        self.ai_btn = self._make_button(zone_boutons, "IA : OFF", self._toggle_ai)
        self.ai_btn.pack(side="left", padx=6)

        self.symbol_btn = self._make_button(zone_boutons, "Symbole : X", self._toggle_symbol)
        self.symbol_btn.pack(side="left", padx=6)

        self._make_button(zone_boutons, "Quitter", self.root.quit).pack(side="left", padx=6)

        tk.Frame(self.root, bg=self.COLORS["bg"], height=6).pack()

    def _make_text(
        self,
        parent,
        text: str,
        fg: str,
        size: int,
        weight: str = "bold",
        padx: int = 20,
        pady: int = 0,
    ) -> tk.Label:
        # Petit texte reutilisable
        return tk.Label(
            parent,
            text=text,
            font=("Courier New", size, weight),
            fg=fg,
            bg=self.COLORS["bg"],
            padx=padx,
            pady=pady,
        )

    def _make_button(self, parent, text: str, command) -> tk.Button:
        # Petit bouton reutilisable
        btn = tk.Button(
            parent,
            text=text,
            font=("Courier New", 9, "bold"),
            bg=self.COLORS["btn"],
            fg=self.COLORS["text"],
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2",
            command=command,
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=self.COLORS["btn_hover"]))
        btn.bind("<Leave>", lambda e: btn.configure(bg=self.COLORS["btn"]))
        return btn

    def _on_hover(self, btn: tk.Button, entering: bool) -> None:
        # Change la couleur au survol
        if btn["text"] == "" and not self.game_over:
            color = self.COLORS["btn_hover"] if entering else self.COLORS["surface"]
            btn.configure(bg=color)

    def _on_click(self, row: int, col: int) -> None:
        # Ignore si la partie est finie ou la case prise
        if self.game_over or not is_free(self.board, row, col):
            return

        # En mode IA, seul l'humain peut cliquer
        if self.vs_ai and self.current_player != self.human_symbol:
            return

        self._play_move(row, col, self.current_player)

        if self.game_over:
            return

# Si c'est a l'IA de jouer
        if self.vs_ai and self.current_player != self.human_symbol:
            self.root.after(400, self._ai_turn)

    def _play_move(self, row: int, col: int, player: str) -> None:
# Met a jour le plateau logique
        make_move(self.board, row, col, player)

# Met a jour le bouton visuellement
        btn = self.buttons[row][col]
        btn.configure(
            text=player,
            fg=self.COLORS[player],
            bg=self.COLORS["surface"],
            state="disabled",
        )

# Si le joueur gagne
        if check_winner(self.board, player):
            self.game_over = True
            self._colorer_cases_gagnantes(player)
            self.turn_text.configure(text=f"Joueur {player} a gagne !", fg=self.COLORS[player])
            messagebox.showinfo("Victoire !", f"Le joueur {player} a gagne !")
            return

# Si le plateau est plein
        if is_full(self.board):
            self.game_over = True
            self.turn_text.configure(text="Match nul !", fg=self.COLORS["muted"])
            messagebox.showinfo("Match nul", "Match nul !")
            return

        # Passe au joueur suivant
        self.current_player = "O" if self.current_player == "X" else "X"
        self.turn_text.configure(
            text=f"Tour du joueur {self.current_player}",
            fg=self.COLORS[self.current_player],
        )

    def _ai_turn(self) -> None:
# L'IA joue une case libre au hasard
        if self.game_over:
            return

        if self.current_player == self.human_symbol:
            return

        row, col = get_ai_move(self.board)
        self._play_move(row, col, self.current_player)

    def _colorer_cases_gagnantes(self, player: str) -> None:
        # Colore les 3 cases gagnantes
        n = 3
        color = "#93c5fd" if player == "X" else "#bfdbfe"

        for r, row in enumerate(self.board):
            if all(cell == player for cell in row):
                self._paint_cells([(r, c) for c in range(n)], color)

        for c in range(n):
            if all(self.board[r][c] == player for r in range(n)):
                self._paint_cells([(r, c) for r in range(n)], color)

        if all(self.board[i][i] == player for i in range(n)):
            self._paint_cells([(i, i) for i in range(n)], color)

        if all(self.board[i][n - 1 - i] == player for i in range(n)):
            self._paint_cells([(i, n - 1 - i) for i in range(n)], color)

    def _paint_cells(self, cells: list[tuple[int, int]], color: str) -> None:
 # Colore une liste de cases
        for r, c in cells:
            self.buttons[r][c].configure(bg=color)

    def _reset_game(self) -> None:
# Remet le plateau a zero
        self.board = init_board()
        self.current_player = "X"
        self.game_over = False

        for r in range(3):
            for c in range(3):
                self.buttons[r][c].configure(
                    text="",
                    fg=self.COLORS["text"],
                    bg=self.COLORS["surface"],
                    state="normal",
                )

        self.turn_text.configure(text="Tour du joueur X", fg=self.COLORS["X"])

        # Si l'humain a choisi O, l'IA commence
        if self.vs_ai and self.human_symbol == "O":
            self.root.after(400, self._ai_turn)

    def _toggle_ai(self) -> None:
# Active ou coupe l'IA puis relance une partie
        self.vs_ai = not self.vs_ai
        self.ai_btn.configure(text=f"IA : {'ON' if self.vs_ai else 'OFF'}")
        self._reset_game()

    def _toggle_symbol(self) -> None:
# Change le symbole de l'humain
        self.human_symbol = "O" if self.human_symbol == "X" else "X"
        self.symbol_btn.configure(text=f"Symbole : {self.human_symbol}")
        self._reset_game()

# PROGRAMME PRINCIPAL

if __name__ == "__main__":
    root = tk.Tk()
    app = MorpionApp(root)
    root.mainloop()
