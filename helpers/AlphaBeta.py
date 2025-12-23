import random
from tokens import Queen, Rook, Bishop, Knight

class AlphaBeta:
    """
    Alpha-Beta Pruning algorithm for chess.
    
    Alpha-Beta is an optimization of MinMax that prunes branches which
    cannot possibly affect the final decision, significantly reducing
    the number of positions that need to be evaluated.
    
    - Alpha: Best score the maximizing player can guarantee
    - Beta: Best score the minimizing player can guarantee
    - Prune when beta <= alpha (opponent won't allow this line)
    """

    def __init__(self):
        self.name = "AlphaBeta"
        self.players = {"black": "white", "white": "black"}
        self.score = {
            "pawn": 100,
            "knight": 320,
            "bishop": 330,
            "rook": 500,
            "queen": 900,
            "king": 20000
        }
        self.root_player = None
        self.nodes_searched = 0

    def make_move_on_board(self, start, end, board):
        """Make a move on the board copy."""
        piece = board[start[0]][start[1]]
        if piece:
            piece.has_moved = True
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
        
        # Handle pawn promotion
        if piece and piece.name == "pawn":
            if end[0] == 0 or end[0] == 7:
                board[end[0]][end[1]] = Queen(piece.color)
        
    def choose_piece(self, position):
        """Choose piece for pawn promotion."""
        options = ['queen'] * 50 + ['knight'] * 10
        return random.choice(options)

    def evaluate_board(self, board):
        """Evaluate board from the root player's perspective."""
        score = 0
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece:
                    piece_value = self.score[piece.name]
                    if piece.color == self.root_player:
                        score += piece_value
                    else:
                        score -= piece_value
        return score

    def order_moves(self, moves, board):
        """
        Order moves to improve pruning efficiency.
        Captures and promotions are searched first.
        """
        scored_moves = []
        for move in moves:
            score = 0
            start, end = move
            target = board[end[0]][end[1]]
            piece = board[start[0]][start[1]]
            
            # Prioritize captures (MVV-LVA: Most Valuable Victim - Least Valuable Attacker)
            if target:
                score += 10000 + self.score[target.name] - self.score[piece.name] // 100
            
            # Prioritize promotions
            if piece and piece.name == "pawn" and (end[0] == 0 or end[0] == 7):
                score += 9000
            
            # Slight bonus for center moves
            if 2 <= end[0] <= 5 and 2 <= end[1] <= 5:
                score += 10
            
            scored_moves.append((score, move))
        
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return [move for _, move in scored_moves]

    def alpha_beta(self, board, game_obj, player, alpha, beta, depth, is_maximizing):
        """
        Alpha-Beta search algorithm.
        
        Args:
            board: Current board state
            game_obj: Game object for move generation
            player: Current player to move
            alpha: Best score for maximizing player so far
            beta: Best score for minimizing player so far
            depth: Remaining search depth
            is_maximizing: True if this is a maximizing node
        
        Returns:
            (best_move, score) tuple
        """
        self.nodes_searched += 1
        
        moves = game_obj.generate_moves_list(player, board)
        
        # Terminal conditions
        if depth == 0:
            return None, self.evaluate_board(board)
        
        if not moves:
            if is_maximizing:
                return None, -1000000 + (10 - depth) * 100
            else:
                return None, 1000000 - (10 - depth) * 100
        
        # Order moves for better pruning
        moves = self.order_moves(moves, board)
        best_move = moves[0]
        
        if is_maximizing:
            max_score = -10000000
            for move in moves:
                next_board = [row[:] for row in board]
                self.make_move_on_board(move[0], move[1], next_board)
                
                _, score = self.alpha_beta(
                    next_board, game_obj, self.players[player],
                    alpha, beta, depth - 1, False
                )
                
                if score > max_score:
                    max_score = score
                    best_move = move
                
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # Beta cutoff
                    
            return best_move, max_score
        else:
            min_score = 10000000
            for move in moves:
                next_board = [row[:] for row in board]
                self.make_move_on_board(move[0], move[1], next_board)
                
                _, score = self.alpha_beta(
                    next_board, game_obj, self.players[player],
                    alpha, beta, depth - 1, True
                )
                
                if score < min_score:
                    min_score = score
                    best_move = move
                
                beta = min(beta, score)
                if beta <= alpha:
                    break  # Alpha cutoff
                    
            return best_move, min_score
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get the best move for the given player."""
        self.root_player = player
        self.nodes_searched = 0
        
        move, score = self.alpha_beta(
            board, game_obj, player,
            -100000000, 100000000, depth, True
        )
        
        print(f"AlphaBeta: {move}, score: {score}, nodes: {self.nodes_searched}")
        return move
