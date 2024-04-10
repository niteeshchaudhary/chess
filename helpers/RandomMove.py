
import random
class RandomMove:

    def __init__(self):
        pass

    def choose_piece(self,position):
        options=['queen']*30+['rook']*15+['bishop']*5+['knight']*10
        return random.choice(options)
    
    def generate_moves_dict(self,player,board):
        moves={}
        for i in range(8):
            for j in range(8):
                if board[i][j] and board[i][j].color==player:
                    mv=board[i][j].get_possible_moves(board,(i,j),self.is_check,self)
                    if mv:
                        moves[i*10+j] = mv
        return moves

    
    def getNextMove(self,board,game_obj):
        moves=game_obj.generate_moves_dict("black",board)
        keys=list(moves.keys())
        cur=random.choice(keys)
        next_position=random.choice(moves[cur])
        current_position=[cur//10,cur%10]
        return[current_position,next_position]

