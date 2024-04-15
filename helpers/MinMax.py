import random

class MinMax:

    def __init__(self):
        self.players={"black":"white","white":"black"}
        self.score={"pawn":10,"knight":30,"bishop":30,"rook":50,"queen":90,"king":9000}

    def make_move_on_board(self, start, end, board):
        piece = board[start[0]][start[1]]
        piece.has_moved = True
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
        
    def choose_piece(self,position):
        options=['queen']*50+['knight']*10
        return random.choice(options)


    def evaluate_board(self,board,player,isMaxplayer):
        score=0
        if isMaxplayer:
            for i in range(8):
                for j in range(8):
                    if board[i][j]:
                        if board[i][j].color==player:
                            score+=self.score[board[i][j].name]
                        else:
                            score-=self.score[board[i][j].name]
                    
        else:
            for i in range(8):
                for j in range(8):
                    if board[i][j]:
                        if board[i][j].color==player:
                            score-=self.score[board[i][j].name]
                        else:
                            score+=self.score[board[i][j].name]
        
        return score

    def minmax(self,board,game_obj,player,depth=2,isMaxplayer=True):

        moves=game_obj.generate_moves_list(player,board)
        #print(moves)
        

        if depth==0:
            return None,self.evaluate_board(board,player,isMaxplayer)

        if not moves:
            if isMaxplayer:
                return None,-10000000
            else:
                return None,10000000
        
        best_move=random.choice(moves)
        
        if isMaxplayer:
            maxscore=-10000000
            for child in moves:
                next_board= [row[:] for row in board]
                game_obj.make_move_on_board(child[0],child[1],next_board)
                _,myscore=self.minmax(next_board,game_obj,self.players[player],depth-1,False)
                if myscore>maxscore:
                    best_move=child
                    maxscore=myscore
            return best_move,maxscore
        else:
            minscore=+1000000
            for child in moves:
                next_board= [row[:] for row in board]
                game_obj.make_move_on_board(child[0],child[1],next_board)
                _,myscore=self.minmax(next_board,game_obj,self.players[player],depth-1,True)
                if myscore<minscore:
                    best_move=child
                    minscore=myscore
            return best_move,minscore
    
    def getNextMove(self,board,game_obj,player="black",depth=4):
        move,_=self.minmax(board,game_obj,player,depth,True)
        print(move)
        return move