from tokens import Rook, Knight, Bishop, King, Queen, Pawn
import tkinter as tk

class Game:
    def __init__(self, master):
        self.board = self.setup_board()
        self.master = master
        self.master.title("Chess Game")

        # Board and token instances
        self.board = self.setup_board()
        self.board_squares = self.create_board_squares()

        # Place pieces on the board
        self.place_pieces()
        # Other initialization code...
        
    def setup_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Place white pieces
        board[0] = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")]
        board[1] = [Pawn("white") for _ in range(8)]

        # Place black pieces
        board[7] = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rook("black")]
        board[6] = [Pawn("black") for _ in range(8)]

        return board

    def create_board_squares(self):
        squares = []
        for row in range(8):
            row_squares = []
            for col in range(8):
                square = tk.Label(self.master, text="", bg=self.get_square_color(row, col), width=6, height=3, relief="sunken")
                square.grid(row=row, column=col)
                row_squares.append(square)
            squares.append(row_squares)
        return squares

    def get_square_color(self, row, col):
        if (row + col) % 2 == 0:
            return "white"
        else:
            return "green"

    def place_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    piece_symbol = piece.get_symbol()
                    self.board_squares[row][col].config(text=piece_symbol)


    # def start(self):
    #     # Game loop

    # def get_possible_moves(self, token):
    #     # Call the corresponding token class and get possible moves

    # Other game logic methods...
    
    def make_move(self, move):
        # ... (existing move logic) ...

        if isinstance(move, tuple):
            position, promotion = move
            if promotion == "promote":
                # Prompt the player to choose a promotion piece
                promoted_piece = self.get_promotion_choice()

                # Replace the pawn with the chosen piece
                self.board[position[0]][position[1]] = promoted_piece(self.current_player)

            # ... (remaining move logic) ...

    def get_promotion_choice(self):
        valid_choices = {"q": Queen, "r": Rook, "b": Bishop, "n": Knight}
        choice = input("Promote to (q)ueen, (r)ook, (b)ishop, (n)ight: ").lower()

        while choice not in valid_choices:
            choice = input("Invalid choice. Promote to (q)ueen, (r)ook, (b)ishop, (n)ight: ").lower()

        return valid_choices[choice](self.current_player.color)