import random

class MinMax_DP:

    def __init__(self):
        self.name="MinMax_DP"
        self.players={"black":"white","white":"black"}
        self.score={"pawn":10,"knight":30,"bishop":30,"rook":50,"queen":90,"king":9000}
        self.count=0
        self.mindic={}
        self.maxdic={}

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
        random.shuffle(moves)
        #print(moves)
        

        if depth==0:
            return None,self.evaluate_board(board,player,isMaxplayer)

        if not moves:
            if isMaxplayer:
                return None,-10000000
            else:
                return None,10000000
        
        best_move=random.choice(moves)
        dp_key=[""]*64
        if isMaxplayer:
            maxscore=-10000000
            for child in moves:
                next_board= [row[:] for row in board]
                game_obj.make_move_on_board(child[0],child[1],next_board)
                for i in range(8):
                    for j in range(8):
                        if next_board[i][j]:
                            dp_key[i*8+j]=next_board[i][j].get_symbol()
                dp_key_tup= tuple(dp_key)

                if dp_key_tup in self.maxdic.keys():
                    print(dp_key_tup)
                    myscore=self.maxdic[dp_key_tup]
                else:
                    _,myscore=self.minmax(next_board,game_obj,self.players[player],depth-1,False)
                    self.maxdic[dp_key_tup]=myscore
                if myscore>maxscore:
                    best_move=child
                    maxscore=myscore
            return best_move,maxscore
        else:
            minscore=+1000000
            for child in moves:
                next_board= [row[:] for row in board]
                game_obj.make_move_on_board(child[0],child[1],next_board)
                for i in range(8):
                    for j in range(8):
                        if next_board[i][j]:
                            dp_key[i*8+j]=next_board[i][j].get_symbol()
                dp_key_tup= tuple(dp_key)
                if dp_key_tup in self.mindic.keys():
                    myscore=self.mindic[dp_key_tup]
                else:
                    _,myscore=self.minmax(next_board,game_obj,self.players[player],depth-1,True)
                    self.mindic[dp_key_tup]=myscore
                if myscore<minscore:
                    best_move=child
                    minscore=myscore
            return best_move,minscore
    
    def getNextMove(self,board,game_obj,player="black",depth=4):
        count=0
        for i in range(8):
            for j in range(8):
                if board[i][j]:
                    count+=1
        if self.count!=count:
            self.mindic={}
            self.maxdic={}
            self.count=count
        move,_=self.minmax(board,game_obj,player,depth,True)
        print(move)
        return move