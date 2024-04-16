
import random
class Greedy:

    def __init__(self):
        self.name="Greedy"
        self.score={"pawn":10,"knight":30,"bishop":30,"rook":50,"queen":90,"king":9000}


    def choose_piece(self,position):
        options=['queen']
        return random.choice(options)
    
    def get_score(self,board,player):
        score=0
        for i in range(8):
            for j in range(8):
                if board[i][j]:
                    if board[i][j].color==player:
                        score+=self.score[board[i][j].name]
                    else:
                        score-=self.score[board[i][j].name]
        return score
    
    def generate_moves_dict(self,player,board):
        moves={}
        for i in range(8):
            for j in range(8):
                if board[i][j] and board[i][j].color==player:
                    mv=board[i][j].get_possible_moves(board,(i,j),self.is_check,self)
                    if mv:
                        moves[i*10+j] = mv
        return moves

    
    def getNextMove(self,board,game_obj,player="black"):
        moves=game_obj.generate_moves_list(player,board)
        random.shuffle(moves)
        best_move=random.choice(moves)
        score=-10000000
        for child in moves:
            next_board= [row[:] for row in board]
            game_obj.make_move_on_board(child[0],child[1],next_board)
            child_score=self.get_score(next_board,player)
            if child_score>score:
                score=child_score
                best_move=child
            
        return best_move

