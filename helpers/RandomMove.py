import random
from tokens import Queen

class RandomMove:
    """
    Random move selector for chess.
    
    Selects a random legal move. Useful for testing and as a baseline
    opponent for evaluating other algorithms.
    """

    def __init__(self):
        self.name = "RandomMove"

    def choose_piece(self, position):
        """Choose piece for pawn promotion."""
        options = ['queen'] * 30 + ['rook'] * 15 + ['bishop'] * 5 + ['knight'] * 10
        return random.choice(options)
    
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

    def getNextMove(self, board, game_obj, player="black", depth=None):
        """Get a random legal move."""
        moves = game_obj.generate_moves_list(player, board)
        
        if not moves:
            return None
        
        move = random.choice(moves)
        print(f"RandomMove: {move}")
        return move
