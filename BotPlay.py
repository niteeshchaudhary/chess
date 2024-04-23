import tkinter as tk
from tkinter import simpledialog, messagebox
from tokens_2 import Rook,Knight, Bishop, King, Queen,Pawn
from my_algo import MyAlgo
import pyautogui as pg
import copy
import time
import threading
from playGame import Game

move_positions = []

def drag_and_drop(start_x, start_y, end_x, end_y, duration=1):
    pg.moveTo(start_x, start_y)
    pg.mouseDown()
    # time.sleep(5)  # Adjust duration as needed
    pg.moveTo(end_x, end_y)
    pg.mouseUp()


class BotPlay:
    is_rotation_enabled = False
    
    def __init__(self,player,board,move_positions,gm):
        self.gm=gm
        self.state=[]
        self.move_positions = move_positions
        self.undo=0
        start_algo="AlphaBeta"
        self.algorithm=MyAlgo(start_algo)

        self.myalgo=self.algorithm.get_object()

        self.history = open(f"history/history{time.time()}.txt", "w+", encoding="utf-8")


        # Create the dropdown menu
        # dropdown = tk.OptionMenu(option_pane, selected_option, "RandomMove","Greedy", "MinMax","MinMax_DP","MinMax_DP_BinHash","AlphaBeta_DP_BinHash", "AlphaBeta", "AlphaBeta_DP","MyBot", command=self.change_algo)
        # dropdown.pack()

        self.black_time=0
        self.white_time=0
        

        self.column_names={0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}

        self.move_labels = []
        self.move_labels_text = []


        # self.master_win.title("Chess Game")
        self.current_player=player

        # Board and token instances
        self.board = board

        # Game state
        self.en_passant_target = None
        self.is_check = False
        self.is_checkmate = False

        self.time_start=time.time()
        if player=="white":
            self.white_turn(board)
        else:
            self.black_turn() 


    def change_algo(self,algo):
        self.myalgo=self.algorithm.get_object(algo)


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


    def update_game_state(self,board=[]):
        # self.current_player="black" if self.current_player=="white" else "white"
        # Reset state
        if board==[]:
            board=self.board
        self.is_check = False
        self.is_checkmate = False

        # Find the king's position
        king_position = self.find_king_position(self.current_player,board)

        # Check for check
        if self.is_king_under_attack(king_position):
            self.is_check = True

            # Check for checkmate
            if self.is_checkmate_(king_position):
                self.history.close()
                self.is_checkmate = True

    def resign(self):
        self.is_checkmate = True
                
    
    def find_king_position(self,color,board=[]):
        if len(board)==0:
            board=self.board

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
                
    def draw(self):
        self.is_checkmate = True


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
        
        
    def move_piece(self, start, end):
        # if self.current_player!="black":
        #     self.state.append((copy.deepcopy(self.board),self.current_player,self.en_passant_target,self.is_check,self.is_checkmate,self.move_labels_text[:]))
        print("Move label:",self.move_labels_text)
        # if len(self.state) > 6:
        #     del self.state[0]  # Remove the oldest label from the list

        piece = self.board[start[0]][start[1]]
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None
        print(self.move_positions[start[0]][start[1]][0], self.move_positions[start[0]][start[1]][1], self.move_positions[end[0]][end[1]][0], self.move_positions[end[0]][end[1]][1])
        drag_and_drop(self.move_positions[start[0]][start[1]][0], self.move_positions[start[0]][start[1]][1], self.move_positions[end[0]][end[1]][0], self.move_positions[end[0]][end[1]][1])

        # Update GUI
        move=(start, end)
        # self.current_player="black" if self.current_player=="white" else "white"
        self.make_move(move)
        self.white_time+=time.time()-self.time_start
        


    def black_turn(self,board=[]):
        time.sleep(2)
        self.gm.read_board()
        self.black_turn()
        
        if board==[]:
            board=self.board
        print(self.myalgo.name," is playing")
        if self.is_checkmate:
            return
        
        t1=time.time()
        moves=self.generate_moves_dict()
        if len(moves.keys())==0:
            self.draw()
            return
        try:
            print("Moves:",moves)
            current_position,next_position=self.myalgo.getNextMove(board,self,"black")
            print("AI: ",current_position,next_position)
            if(next_position in moves[current_position[0]*10+current_position[1]]):
                self.move_piece(current_position,next_position)
            else:
                self.draw()
        except Exception as e:
            print("Error:",e)
            self.history.close()
            self.draw()
            return
        
        self.black_time+=time.time()-t1
        self.time_start=time.time()

    def white_turn(self,board=[]):
        if board==[]:
            board=self.board
        
        self.update_game_state(board)
        if self.is_checkmate:
            return
        print(self.myalgo.name," is playing")
        t1=time.time()
        moves=self.generate_moves_dict()
        if len(moves.keys())==0:
            self.draw()
            return
        

        current_position,next_position=self.myalgo.getNextMove(board=board,game_obj=self,player="white")
        print("white",current_position,next_position)
        if(next_position in moves[current_position[0]*10+current_position[1]]):
            self.move_piece(current_position,next_position)
        else:
            self.draw()

        time.sleep(6)
        self.board=self.gm.read_board()
        self.white_turn()


        
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
                elif position[0] == 0 or position[0] == 7:
                    self.ai_choose_piece(position)

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
                elif position == (row, col - 2):  # Queenside castling
                    rook = self.board[row][0]
                    rook.has_moved = True
                    self.board[row][3] = rook
                    self.board[row][0] = None
                    # Update GUI

            elif isinstance(piece, Rook):
                self.en_passant_target=None
                # Update rook's has_moved attribute
                piece.has_moved = True
            else:
                self.en_passant_target=None


    def generate_moves_dict(self,player="",board=[]):
        player=self.current_player if player=="" else player
        myboard=self.board if board==[] else board
        moves={}
        print(board,player)
        for i in range(8):
            for j in range(8):
                    
                if myboard[i][j] and myboard[i][j].color==player:
                    print("RR")
                    print(myboard[i][j].color,i,j)
                    mv=myboard[i][j].get_possible_moves(myboard,(i,j),self.is_check,self)
                    print("OO",mv,self.is_check)
                    if mv:
                        moves[i*10+j] = mv
        print(moves)
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

def startGame(ref):
    global move_positions
    ref.destroy()
    gm = Game()
    board, move_positions = gm.play()
    if not board:
        error()
    if board[-1][-1]:
        print("->",board[-1][-1].color)
        game_=BotPlay(board[-1][-1].color,board,move_positions,gm)



def error():
    mn = tk.Tk()
    messagebox.showerror("Error", "We faced issue in detecting grid region selected by you! Please try to select exact grid next time.")
    exit()

def menu():
    mn = tk.Tk()
    mn.geometry('%dx%d+%d+%d' % (300, 50, mn.winfo_screenwidth() // 2, mn.winfo_screenheight() // 2))
    button = tk.Button(mn, text='Play', command=lambda: startGame(mn))
    button.pack(side=tk.TOP, pady=5)
    mn.mainloop()

if __name__ == '__main__':
    menu()
# if __name__ == "__main__":
#     root = tk.Tk()
#     game = BotPlay(root)
#     root.mainloop()