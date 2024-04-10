from tokens import Rook,Knight, Bishop, King, Queen,Pawn

class MinMax:

    def __init__(self):
        pass

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

    def evaluate_board(self):
        
        return 0
    
    def getNextMove(self,board):
        keys=board.keys()
        random.choose