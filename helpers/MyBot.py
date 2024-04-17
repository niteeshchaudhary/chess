import random
from tokens import Queen
from tokens import Rook 
from tokens import Bishop
from tokens import Knight

class MyBot:

    def __init__(self):
        self.name="MyBot"
        self.players={"black":"white","white":"black"}

    def make_move_on_board(self, start, end, board,choice=None):
        piece = board[start[0]][start[1]]
        piece.has_moved = True
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
        if piece.name=="pawn":
            if end[0] == 0 or end[0] == 7:
                if choice=="rook":
                    board[end[0]][end[1]]=Rook(piece.color)
                elif choice=="bishop":
                    board[end[0]][end[1]]=Bishop(piece.color)
                elif choice=="knight":
                    board[end[0]][end[1]]=Knight(piece.color)
                else:
                    board[end[0]][end[1]]=Queen(piece.color)
        
    def choose_piece(self,position):
        pass

    
    def getNextMove(self,board,game_obj,player="black",depth=4):
        move=game_obj.generate_moves_list(player,board)
        random.shuffle(move)
        return move[0]