import random
from tokens import Queen, Rook, Bishop, Knight

class Greedy:
    """
    Greedy algorithm for chess.
    
    Evaluates all possible moves and selects the one that results
    in the best immediate material advantage. Does not look ahead.
    
    Fast but shortsighted - good for testing or as a baseline.
    """

    def __init__(self):
        self.name = "Greedy"
        self.score = {
            "pawn": 100,
            "knight": 320,
            "bishop": 330,
            "rook": 500,
            "queen": 900,
            "king": 20000
        }
        
        # Piece-square bonus for center control
        self.center_bonus = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 10, 10, 5, 0, 0],
            [0, 0, 10, 20, 20, 10, 0, 0],
            [0, 0, 10, 20, 20, 10, 0, 0],
            [0, 0, 5, 10, 10, 5, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def choose_piece(self, position):
        """Choose piece for pawn promotion."""
        return 'queen'  # Always promote to queen

    def make_move_on_board(self, start, end, board):
        """Make a move on a board copy."""
        piece = board[start[0]][start[1]]
        if piece:
            piece.has_moved = True
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
        
        # Handle pawn promotion
        if piece and piece.name == "pawn":
            if end[0] == 0 or end[0] == 7:
                board[end[0]][end[1]] = Queen(piece.color)
    
    def get_score(self, board, player):
        """
        Evaluate board from player's perspective.
        Includes material and basic positional bonuses.
        """
        score = 0
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece:
                    # Material value
                    piece_value = self.score[piece.name]
                    
                    # Add center bonus for non-king pieces
                    if piece.name != "king":
                        piece_value += self.center_bonus[i][j]
                    
                    if piece.color == player:
                        score += piece_value
                    else:
                        score -= piece_value
        return score
    
    def evaluate_move(self, board, move, player):
        """Evaluate a single move and return its score."""
        next_board = [row[:] for row in board]
        self.make_move_on_board(move[0], move[1], next_board)
        return self.get_score(next_board, player)
    
    def getNextMove(self, board, game_obj, player="black", depth=None):
        """Get the greedily best move."""
        moves = game_obj.generate_moves_list(player, board)
        
        if not moves:
            return None
        
        # Shuffle for variety when moves are equal
        random.shuffle(moves)
        
        best_move = moves[0]
        best_score = -10000000
        
        for move in moves:
            move_score = self.evaluate_move(board, move, player)
            
            if move_score > best_score:
                best_score = move_score
                best_move = move
        
        print(f"Greedy: {best_move}, score: {best_score}")
        return best_move
