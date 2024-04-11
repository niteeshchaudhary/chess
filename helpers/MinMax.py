from tokens import Rook,Knight, Bishop, King, Queen,Pawn
import random

class MinMax:

    def __init__(self):
        pass

    def choose_piece(self,position):
        options=['queen']*50+['knight']*10
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
    
    def generate_moves_list(self,player,board):
        moves=[]
        for i in range(8):
            for j in range(8):
                if board[i][j] and board[i][j].color==player:
                    for mv in board[i][j].get_possible_moves(board,(i,j),self.is_check,self):
                        moves.append([(i,j),mv])

        return moves

    def minimax(self, depth, is_maximizing):
        if depth == 0 or self.board.is_checkmate():
            return -self.evaluate_board()

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def calculate_best_move(self, depth):
        best_move = None
        best_value = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            board_value = self.minimax(depth - 1, False)
            self.board.pop()
            if board_value > best_value:
                best_value = board_value
                best_move = move
        return best_move
    
    def make_move_on_board(self, start, end, board):
        piece = board[start[0]][start[1]]
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None

    def evaluate_board(self):
        
        return 0
    
    def getNextMove(self,board,game_obj):
        moves=game_obj.generate_moves_dict("black",board)
        mv_score={}
        max_score=-1000000
        move_max=None
        print(moves)
        for k,v in moves.items():
            start_p=(k//10,k%10)
            for next_move in v:
                mv_score[(start_p,next_move)]=0
                #max
                if board[next_move[0]][next_move[1]] and board[next_move[0]][next_move[1]].color=="white":
                    if board[next_move[0]][next_move[1]].name=="queen":
                        mv_score[(start_p,next_move)]+=10
                    elif board[next_move[0]][next_move[1]].name=="rook":
                        mv_score[(start_p,next_move)]+=7
                    elif board[next_move[0]][next_move[1]].name=="bishop":
                        mv_score[(start_p,next_move)]+=5
                    elif board[next_move[0]][next_move[1]].name=="knight":
                        mv_score[(start_p,next_move)]+=3
                    else:
                        mv_score[(start_p,next_move)]+=1

                next_board=[row[:] for row in board]
                self.make_move_on_board(start_p,next_move,next_board)
                next_board_2=[row[:] for row in next_board]
                opp_moves=game_obj.generate_moves_dict("white",next_board)
                for k_,v_ in opp_moves.items():
                    for mv in v_: #min
                        if next_board[mv[0]][mv[1]] and next_board[mv[0]][mv[1]].color=="black":
                            if next_board[mv[0]][mv[1]].name=="queen":
                                mv_score[(start_p,next_move)]-=10
                            elif next_board[mv[0]][mv[1]].name=="rook":
                                mv_score[(start_p,next_move)]-=7
                            elif next_board[mv[0]][mv[1]].name=="bishop":
                                mv_score[(start_p,next_move)]-=5
                            elif next_board[mv[0]][mv[1]].name=="knight":
                                mv_score[(start_p,next_move)]-=3
                            else:
                                mv_score[(start_p,next_move)]-=1
                    
        if mv_score[(start_p,next_move)]>max_score:
            move_max=(start_p,next_move)
            max_score=mv_score[(start_p,next_move)]
    

        return move_max


            
                        





        