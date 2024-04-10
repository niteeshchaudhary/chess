import tkinter as tk
from tkinter import simpledialog, messagebox
from tokens import Rook,Knight, Bishop, King, Queen,Pawn
from helpers import RandomMove as MyAlgo
import copy
import time

class Utility:
    
    def __init__(self, master,history_pane,option_pane):

       
        self.state=[]

        self.myalgo=MyAlgo()

        # self.master_win.title("Chess Game")
        self.current_player="white"

        # Board and token instances
        self.board = self.setup_board()

        # Game state
        self.en_passant_target = None
        self.is_check = False
        self.is_checkmate = False

        self.selected_piece = None

    def choose_piece(self,position,inp):
        piece=self.board[position[0]][position[1]]
        # Function to set the selected inp and close the dialog
        inp = inp.lower()  # Convert input to lowercase for case-insensitive comparison
        if inp == "rook":
            self.board[position[0]][position[1]]=Rook(piece.color)
        elif inp == "bishop":
            self.board[position[0]][position[1]]=Bishop(piece.color)
        elif inp == "knight":
            self.board[position[0]][position[1]]=Knight(piece.color)
        else:
            self.board[position[0]][position[1]]=Queen(piece.color)

        self.board_squares[position[0]][position[1]].config(text=self.board[position[0]][position[1]].get_symbol())

    def update_game_state(self):
        # self.current_player="black" if self.current_player=="white" else "white"
        # Reset state
        self.is_check = False
        self.is_checkmate = False

        # Find the king's position
        king_position = self.find_king_position(self.current_player)

        # Check for check
        if self.is_king_under_attack(king_position):
            self.is_check = True
            self.board_squares[king_position[0]][king_position[1]].config(bg="blue")

            # Check for checkmate
            if self.is_checkmate_(king_position):
                self.is_checkmate = True


    def resign(self):
        self.is_checkmate = True
                

    def find_king_position(self,color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)


    def is_king_under_attack(self, king_position,board=[]):
        opponent_color = "white" if self.current_player == "black" else "black"
        myboard=self.board if board==[] else board
        # print("King : ",opponent_color)
        for row in range(8):
            for col in range(8):
                piece = myboard[row][col]
                if piece and piece.color == opponent_color: #and not isinstance(piece, King):
                    possible_moves = piece.get_possible_moves_op(myboard, (row, col),self.is_check,game=self)
                    if king_position in possible_moves:
                        return True

        return False

    def is_checkmate_(self, king_position):
        # Check if the king has any valid moves
        king = self.board[king_position[0]][king_position[1]]
        king_moves = king.get_possible_moves(self.board, king_position,self.is_check,game=self)

        # Remove any moves that would still leave the king in check
        valid_moves = []
        for move in king_moves:
            backup_board = [row[:] for row in self.board]
            self.make_move_on_board(king_position, move, backup_board)
            if not self.is_king_under_attack(move):
                valid_moves.append(move)
            
        # Check if any other piece can block or capture the attacking piece
        if valid_moves:
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == self.current_player:
                    possible_moves = piece.get_possible_moves(self.board, (row, col),self.is_check,game=self)
                    if len(possible_moves)>0:
  
                        return False

        return True
    
    def make_move_on_board(self, start, end, board):
        piece = board[start[0]][start[1]]
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None    


    def generate_moves_dict(self,player="",board=[]):
        player=self.current_player if player=="" else player
        myboard=self.board if board==[] else board
        moves={}
        for i in range(8):
            for j in range(8):
                if myboard[i][j] and myboard[i][j].color==player:
                    mv=myboard[i][j].get_possible_moves(myboard,(i,j),self.is_check,self)
                    if mv:
                        moves[i*10+j] = mv
        return moves

    def generate_moves_list(self,player="",board=[]):
        player=self.current_player if player=="" else player
        myboard=self.board if board==[] else board
        moves=[]
        for i in range(8):
            for j in range(8):
                if myboard[i][j] and myboard[i][j].color==player:
                    for mv in myboard[i][j].get_possible_moves(myboard,(i,j),self.is_check,self):
                        moves.append([(i,j),mv])

        return moves


        