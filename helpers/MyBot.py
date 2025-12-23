import random
from tokens import Queen, Rook, Bishop, Knight

class MyBot:
    """
    Custom bot template.
    
    This is a template class that you can customize with your own
    chess playing logic. Currently implements a simple random move
    with slight preference for captures.
    """

    def __init__(self):
        self.name = "MyBot"
        self.players = {"black": "white", "white": "black"}
        self.piece_values = {
            "pawn": 100,
            "knight": 320,
            "bishop": 330,
            "rook": 500,
            "queen": 900,
            "king": 20000
        }

    def make_move_on_board(self, start, end, board, choice=None):
        """Make a move on a board copy."""
        piece = board[start[0]][start[1]]
        if piece:
            piece.has_moved = True
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
        
        # Handle pawn promotion
        if piece and piece.name == "pawn":
            if end[0] == 0 or end[0] == 7:
                if choice == "rook":
                    board[end[0]][end[1]] = Rook(piece.color)
                elif choice == "bishop":
                    board[end[0]][end[1]] = Bishop(piece.color)
                elif choice == "knight":
                    board[end[0]][end[1]] = Knight(piece.color)
                else:
                    board[end[0]][end[1]] = Queen(piece.color)
        
    def choose_piece(self, position):
        """Choose piece for pawn promotion."""
        return 'queen'

    def score_move(self, board, move):
        """Score a move - higher is better."""
        start, end = move
        score = 0
        
        piece = board[start[0]][start[1]]
        target = board[end[0]][end[1]]
        
        # Captures are good
        if target:
            # MVV-LVA: capture valuable pieces with less valuable ones
            score += self.piece_values[target.name] * 10
            score -= self.piece_values[piece.name]
        
        # Center control is good
        if 2 <= end[0] <= 5 and 2 <= end[1] <= 5:
            score += 20
        
        # Promotions are very good
        if piece.name == "pawn" and (end[0] == 0 or end[0] == 7):
            score += 800
        
        # Developing pieces is good
        if not getattr(piece, 'has_moved', True):
            if piece.name in ['knight', 'bishop']:
                score += 30
        
        return score
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get a move using simple heuristics."""
        moves = game_obj.generate_moves_list(player, board)
        
        if not moves:
            return None
        
        # Score all moves
        scored_moves = [(self.score_move(board, move), move) for move in moves]
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        
        # Pick from top moves with some randomness
        top_moves = scored_moves[:max(3, len(scored_moves) // 3)]
        _, best_move = random.choice(top_moves)
        
        print(f"MyBot: {best_move}")
        return best_move
