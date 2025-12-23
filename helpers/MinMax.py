import random
from tokens import Queen, Rook, Bishop, Knight

class MinMax:
    """
    MinMax algorithm for chess move selection.
    
    The minimax algorithm recursively evaluates positions by assuming
    both players play optimally - maximizing for us, minimizing for opponent.
    """

    def __init__(self):
        self.name = "MinMax"
        self.players = {"black": "white", "white": "black"}
        # Improved piece values (in centipawns)
        self.score = {
            "pawn": 100,
            "knight": 320,
            "bishop": 330,
            "rook": 500,
            "queen": 900,
            "king": 20000
        }
        # Track the root player for correct evaluation
        self.root_player = None

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
        """
        Evaluate board from the root player's perspective.
        Positive score = good for root player.
        """
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

    def minmax(self, board, game_obj, player, depth=2, is_maximizing=True):
        """
        MinMax search algorithm.
        
        Args:
            board: Current board state
            game_obj: Game object for move generation
            player: Current player to move
            depth: Remaining search depth
            is_maximizing: True if maximizing (root player's turn at this level)
        
        Returns:
            (best_move, score) tuple
        """
        # Generate legal moves
        moves = game_obj.generate_moves_list(player, board)
        
        # Terminal conditions
        if depth == 0:
            return None, self.evaluate_board(board)
        
        if not moves:
            # No moves = checkmate or stalemate
            if is_maximizing:
                return None, -1000000 + (10 - depth) * 100  # Prefer later checkmates
            else:
                return None, 1000000 - (10 - depth) * 100
        
        # Shuffle for variety
        random.shuffle(moves)
        best_move = moves[0]
        
        if is_maximizing:
            max_score = -10000000
            for move in moves:
                # Make move on copy
                next_board = [row[:] for row in board]
                self.make_move_on_board(move[0], move[1], next_board)
                
                # Recurse
                _, score = self.minmax(next_board, game_obj, self.players[player], depth - 1, False)
                
                if score > max_score:
                    max_score = score
                    best_move = move
                    
            return best_move, max_score
        else:
            min_score = 10000000
            for move in moves:
                # Make move on copy
                next_board = [row[:] for row in board]
                self.make_move_on_board(move[0], move[1], next_board)
                
                # Recurse
                _, score = self.minmax(next_board, game_obj, self.players[player], depth - 1, True)
                
                if score < min_score:
                    min_score = score
                    best_move = move
                    
            return best_move, min_score
    
    def getNextMove(self, board, game_obj, player="black", depth=3):
        """Get the best move for the given player."""
        self.root_player = player  # Set root player for evaluation
        move, score = self.minmax(board, game_obj, player, depth, True)
        print(f"MinMax: {move}, score: {score}")
        return move
