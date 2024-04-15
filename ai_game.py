import tkinter as tk
from tkinter import simpledialog, messagebox
from tokens import Rook,Knight, Bishop, King, Queen,Pawn
from helpers import RandomMove #as MyAlgo
from helpers import MinMax as MyAlgo
import copy
import time
import threading

class AI_Game:
    is_rotation_enabled = False
    
    def __init__(self, master,history_pane,option_pane):

        self.master = master
        self.state=[]
        self.undo=0

        self.myalgo=MyAlgo()

        self.history = open(f"history/history{time.time()}.txt", "w+", encoding="utf-8")


        self.move_history_frame = history_pane

        sq = tk.Label(self.master, text="Y", bg="red", width=2, height=1, relief="sunken", font=("Arial", 46))

        self.column_names={0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}

        self.move_labels = []
        self.move_labels_text = []


        # self.master_win.title("Chess Game")
        self.current_player="white"

        self.current_player_label= tk.Label(self.move_history_frame, text="Player Turn: "+self.current_player, height=1, relief="sunken", font=("Arial", 16), bg="lightblue", bd=0)
        self.current_player_label.pack(pady=20)

        self.current_orientation = 'normal'  # or 'normal' for default, 'rotated' for rotated
        


        # Board and token instances
        self.board = self.setup_board()
        self.board_squares = self.create_board_squares()

        # Game state
        self.en_passant_target = None
        self.is_check = False
        self.is_checkmate = False

        # Place pieces on the board
        self.place_pieces()
        
        for row in range(8):
            for col in range(8):
                self.board_squares[row][col].bind("<Button-1>", lambda event, row=row, col=col: self.on_square_clicked(row, col))

        self.rotate_board()
                
        # Variable to store selected piece position
        self.selected_piece = None

    def ai_choose_piece(self,position):
        piece=self.board[position[0]][position[1]]
        inp=self.myalgo.choose_piece(position)
        if inp == "rook":
            self.board[position[0]][position[1]]=Rook(piece.color)
        elif inp == "bishop":
            self.board[position[0]][position[1]]=Bishop(piece.color)
        elif inp == "knight":
            self.board[position[0]][position[1]]=Knight(piece.color)
        else:
            self.board[position[0]][position[1]]=Queen(piece.color)

        self.board_squares[position[0]][position[1]].config(text=self.board[position[0]][position[1]].get_symbol())

    def choose_piece(self,position):
        piece=self.board[position[0]][position[1]]
        # Function to set the selected inp and close the dialog
        def set_inp(p):
            inp = p
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
            print("You chose:", inp)
            dialog.destroy()

        # Create a dialog box
        dialog = tk.Toplevel(self.master)
        dialog.title("Choose Chess piece")
        buttons_text = ["Rook", "Bishop", "Knight",  "Queen"]
        tk.Button(dialog, text=buttons_text[0],width=10, height=2,  command=lambda: set_inp(buttons_text[0])).pack(padx=5, pady=5)
        tk.Button(dialog, text=buttons_text[1],width=10, height=2,  command=lambda: set_inp(buttons_text[1])).pack(padx=5, pady=5)
        tk.Button(dialog, text=buttons_text[2],width=10, height=2,  command=lambda: set_inp(buttons_text[2])).pack(padx=5, pady=5)
        tk.Button(dialog, text=buttons_text[3],width=10, height=2,  command=lambda: set_inp(buttons_text[3])).pack(padx=5, pady=5)
        self.master.wait_window(dialog)
        

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
                square = tk.Label(self.master, text="", bg=self.get_square_color(row, col), width=2, height=1, relief="sunken", font=("Arial", 46))
                square.grid(row=row, column=col)
                row_squares.append(square)
            squares.append(row_squares)
        return squares
    
    def rotate_board(self):

        for row in range(8):
            for col in range(8):
                square = self.board_squares[row][col]
                square.grid_forget()
                if self.current_orientation == 'normal':
                    square.grid(row=7-row, column=7-col)
                else:
                    square.grid(row=row, column=col)

        if AI_Game.is_rotation_enabled and self.current_orientation== "normal":
            self.current_orientation="rotated"
        else:
            self.current_orientation= "normal"



    def get_square_color(self, row, col):
        if (row + col) % 2 == 0:
            return "white"
        else:
            return "lightgreen"

    def place_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    piece_symbol = piece.get_symbol()
                    self.board_squares[row][col].config(text=piece_symbol)                   

    def on_square_clicked(self, row, col):
        if self.is_checkmate or self.current_player=="black":
            return
        piece = self.board[row][col]

        if piece:
            if self.selected_piece is None:
                if piece.color==self.current_player:
                    # Highlight possible moves for the selected piece
                    possible_moves = piece.get_possible_moves(self.board, (row, col), self.is_check, game=self)
                    self.highlight_possible_moves(possible_moves)
                    self.board_squares[row][col].config(bg="orange")
                    self.selected_piece = (row, col)
                else:
                    self.clear_highlighting()
                    self.board_squares[row][col].config(bg="orange")
                    return

            else:
                # Move the selected piece to the clicked square
                print( "selected: ",self.selected_piece)
                prev_piece = self.board[self.selected_piece[0]][self.selected_piece[1]]
                possible_moves=prev_piece.get_possible_moves(self.board, self.selected_piece, self.is_check, game=self)
                if (row, col) in possible_moves:
                    # moving on oppenents piece
                    print("Move piece")
                    self.clear_highlighting()
                    self.move_piece(self.selected_piece, (row, col))
                    past=self.selected_piece
                    self.selected_piece = None
                    print("currrr",self.current_player)
                    self.board_squares[past[0]][past[1]].config(bg="purple")
                    self.board_squares[row][col].config(bg="#FF00FF") 
                else:
                    print( "choose diff: ",self.selected_piece)
                    if piece.color==self.current_player:
                        print( "choose diff:-> ",piece.color,self.current_player)
                        self.selected_piece = None
                        self.clear_highlighting()
                        self.selected_piece = (row, col)
                        piece = self.board[row][col]
                        possible_moves=piece.get_possible_moves(self.board, self.selected_piece, self.is_check, game=self)
                        self.highlight_possible_moves(possible_moves)
                        self.board_squares[row][col].config(bg="orange")
                        self.selected_piece = (row, col)
                    else:
                        self.clear_highlighting()
                        self.board_squares[row][col].config(bg="orange")
                        return

        else:
            if self.selected_piece:
                piece = self.board[self.selected_piece[0]][self.selected_piece[1]]
                possible_moves=piece.get_possible_moves(self.board, self.selected_piece, self.is_check, game=self)
                if (row, col) in possible_moves:
                    # moving in empty space
                    print("Move piece 000")
                    self.clear_highlighting()
                    self.move_piece(self.selected_piece, (row, col))
                    past=self.selected_piece
                    self.selected_piece = None
                    self.board_squares[past[0]][past[1]].config(bg="purple")
                    self.board_squares[row][col].config(bg="pink")
                    print("currrr yemp",self.current_player)
                    # self.board_squares[past[0]][past[1]].config(bg="purple")
                    # self.board_squares[row][col].config(bg="#FF00FF")
                else:
                    self.clear_highlighting()

    def highlight_possible_moves(self, moves):
        for row in range(8):
            for col in range(8):
                if (row, col) in moves:
                    self.board_squares[row][col].config(bg="yellow")
                else:
                    self.board_squares[row][col].config(bg=self.get_square_color(row, col))


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
                self.history.close()
                for row in range(8):
                    for col in range(8):
                        self.board_squares[row][col].config(state="disable")
                self.is_checkmate = True
                self.board_squares[king_position[0]][king_position[1]].config(bg="red")

    def resign(self):
        self.is_checkmate = True
        for row in range(8):
            for col in range(8):
                self.board_squares[row][col].config(state="disable")
        king_position = self.find_king_position(self.current_player)
        self.board_squares[king_position[0]][king_position[1]].config(bg="red")
                
    
    def find_king_position(self,color,board=[]):
        if len(board)==0:
            board=self.board

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
                
    def draw(self):
        for row in range(8):
            for col in range(8):
                self.board_squares[row][col].config(state="disable")
                self.is_checkmate = True

        king_position = self.find_king_position("black")
        self.board_squares[king_position[0]][king_position[1]].config(bg="#ff00ff")

        king_position = self.find_king_position("white")
        self.board_squares[king_position[0]][king_position[1]].config(bg="#ff00ff")



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
                    # for move in possible_moves:
                    #     backup_board = [row[:] for row in self.board]
                    #     self.make_move_on_board((row, col), move, backup_board)
                    #     if not self.is_king_under_attack(king_position):
                    if len(possible_moves)>0:
                        # print((row, col), piece,possible_moves)    
                        return False

        return True
    
    def is_checkmate_board(self, board,player,is_check):
        king_position=self.find_king_position(player,board)
        # Check if the king has any valid moves
        king = board[king_position[0]][king_position[1]]
        king_moves = king.get_possible_moves(board, king_position,is_check,game=self)

        # Remove any moves that would still leave the king in check
        valid_moves = []
        for move in king_moves:
            backup_board = [row[:] for row in board]
            self.make_move_on_board(king_position, move, backup_board)
            if not self.is_king_under_attack(move):
                valid_moves.append(move)
            
        # Check if any other piece can block or capture the attacking piece
        if valid_moves:
            return False

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == self.current_player:
                    possible_moves = piece.get_possible_moves(self.board, (row, col),is_check,game=self)
                    if len(possible_moves)>0: 
                        return False

    
    def make_move_on_board(self, start, end, board):
        piece = board[start[0]][start[1]]
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
        
    def clear_highlighting(self):
        for row in range(8):
            for col in range(8):
                self.board_squares[row][col].config(bg=self.get_square_color(row, col))
        
    def move_piece(self, start, end):
        if self.current_player!="black":
            self.state.append((copy.deepcopy(self.board),self.current_player,self.en_passant_target,self.is_check,self.is_checkmate,self.move_labels_text[:]))
        print("Move label:",self.move_labels_text)
        if len(self.state) > 6:
            del self.state[0]  # Remove the oldest label from the list

        piece = self.board[start[0]][start[1]]
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        # Update GUI
        self.board_squares[end[0]][end[1]].config(text=piece.get_symbol())
        self.board_squares[start[0]][start[1]].config(text="")
        move=(start, end)
        self.current_player="black" if self.current_player=="white" else "white"
        self.add_move_to_history(move,piece.get_symbol())
        self.make_move(move)
        self.current_player_label.config(text="Player Turn: "+self.current_player)
        if self.current_player=="black":
            self.opponent_turn()
            #opp_thread=threading.Thread(target=self.opponent_turn)
            #opp_thread.start()


    def opponent_turn(self):
        if self.is_checkmate:
            return
        moves=self.generate_moves_dict()
        if len(moves.keys())==0:
            self.draw()
            return
        try:
            print("Moves:",moves)
            current_position,next_position=self.myalgo.getNextMove(self.board,self,"black")
            print("AI: ",current_position,next_position)
            if(next_position in moves[current_position[0]*10+current_position[1]]):
                self.move_piece(current_position,next_position)
                self.board_squares[current_position[0]][current_position[1]].config(bg="purple")
                self.board_squares[next_position[0]][next_position[1]].config(bg="#FF00FF") 
            else:
                self.draw()
        except Exception as e:
            self.history.close()
            self.draw()
            return

        
    def make_move(self, move):
        self.update_game_state()

        if self.is_checkmate:
            print(f"{self.current_player.capitalize()} is in checkmate!")
            # Handle game over
        elif self.is_check:
            print(f"{self.current_player.capitalize()} king is in check!")
            
        # Update en passant target
        if isinstance(move, tuple):
            start_position,position = move
            piece = self.board[position[0]][position[1]]
            # print("_>",piece)
            if isinstance(piece, Pawn):
                # print("...",piece.en_passant_target)
                # print("...",self.en_passant_target,position)
                if(self.en_passant_target==position):
                    self.board[start_position[0]][position[1]]=None
                    self.board_squares[start_position[0]][position[1]].config(text="")
                elif position[0] == 0 or position[0] == 7:
                    if self.current_player=="white":#have already changed the current player
                        self.ai_choose_piece(position)
                    else:
                        self.choose_piece(position)
                    


                # if self.en_passant_target and piece.en_passant_target
                self.en_passant_target = piece.en_passant_target
                piece.en_passant_target=None
                
            elif isinstance(piece, King):
                self.en_passant_target=None
                # Update king's has_moved attribute
                piece.has_moved = True

                # Check for castling move
                row, col = start_position
                # print("K",start_position)
                if position == (row, col + 2):  # Kingside castling
                    # print("Ks",position)
                    rook = self.board[row][7]
                    rook.has_moved = True
                    self.board[row][5] = rook
                    self.board[row][7] = None
                    # Update GUI
                    self.board_squares[row][5].config(text=rook.get_symbol())
                    self.board_squares[row][7].config(text="")
                elif position == (row, col - 2):  # Queenside castling
                    rook = self.board[row][0]
                    rook.has_moved = True
                    self.board[row][3] = rook
                    self.board[row][0] = None
                    # Update GUI
                    self.board_squares[row][3].config(text=rook.get_symbol())
                    self.board_squares[row][0].config(text="")

            elif isinstance(piece, Rook):
                self.en_passant_target=None
                # Update rook's has_moved attribute
                piece.has_moved = True
            else:
                self.en_passant_target=None


        # Check for check and checkmate
        self.update_game_state()

    def add_move_to_history(self, move, symbol):
        start,end=move
        
        move_text=f"{symbol} {self.column_names[start[1]]}{start[0]+1}-{self.column_names[end[1]]}{end[0]+1}"
        self.move_labels_text.append(move_text)
        move_label = tk.Label(self.move_history_frame, text=move_text, height=1, relief="sunken", font=("Arial", 20))
        self.history.write(f"{start[1]},{start[0]},{[end[1]]},{end[0]},{self.current_player},{symbol},{self.board[end[0]][end[1]].__class__.__name__}\n")

        if self.current_player=="white":
            move_label.pack(anchor="w",padx=5)
        else:
            move_label.pack(anchor="e",padx=5)
        self.move_labels.append(move_label)

        if len(self.move_labels) > 15:
            self.move_labels[0].destroy()  # Remove the oldest label from the GUI
            del self.move_labels_text[0]
            del self.move_labels[0]  # Remove the oldest label from the list

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


        

if __name__ == "__main__":
    root = tk.Tk()
    game = AI_Game(root)
    root.mainloop()