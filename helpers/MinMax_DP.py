import random
from tokens import Queen, Rook, Bishop, Knight

class MinMax_DP:
    """
    MinMax algorithm with Dynamic Programming (memoization).
    
    Uses a transposition table to cache evaluated positions,
    avoiding redundant calculations for positions reached via different move orders.
    """

    def __init__(self):
        self.name = "MinMax_DP"
        self.players = {"black": "white", "white": "black"}
        self.score = {
            "pawn": 100,
            "knight": 320,
            "bishop": 330,
            "rook": 500,
            "queen": 900,
            "king": 20000
        }
        self.piece_count = 0
        self.transposition_table = {}
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

    def get_board_hash(self, board):
        """
        Generate a unique hash for the board position.
        Uses piece symbols to distinguish between piece types and colors.
        """
        # Create a tuple of all pieces on the board
        board_state = []
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece:
                    # Include piece type, color, and position
                    board_state.append((i, j, piece.name, piece.color))
                else:
                    board_state.append((i, j, None, None))
        return tuple(board_state)

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

    def minmax(self, board, game_obj, player, depth=2, is_maximizing=True):
        """MinMax with transposition table lookup."""
        # Generate moves first (needed for terminal check)
        moves = game_obj.generate_moves_list(player, board)
        
        # Terminal conditions
        if depth == 0:
            return None, self.evaluate_board(board)
        
        if not moves:
            if is_maximizing:
                return None, -1000000 + (10 - depth) * 100
            else:
                return None, 1000000 - (10 - depth) * 100
        
        # Check transposition table
        board_hash = self.get_board_hash(board)
        tt_key = (board_hash, depth, is_maximizing)
        
        if tt_key in self.transposition_table:
            return self.transposition_table[tt_key]
        
        random.shuffle(moves)
        best_move = moves[0]
        
        if is_maximizing:
            max_score = -10000000
            for move in moves:
                next_board = [row[:] for row in board]
                self.make_move_on_board(move[0], move[1], next_board)
                
                _, score = self.minmax(next_board, game_obj, self.players[player], depth - 1, False)
                
                if score > max_score:
                    max_score = score
                    best_move = move
            
            # Cache result
            self.transposition_table[tt_key] = (best_move, max_score)
            return best_move, max_score
        else:
            min_score = 10000000
            for move in moves:
                next_board = [row[:] for row in board]
                self.make_move_on_board(move[0], move[1], next_board)
                
                _, score = self.minmax(next_board, game_obj, self.players[player], depth - 1, True)
                
                if score < min_score:
                    min_score = score
                    best_move = move
            
            # Cache result
            self.transposition_table[tt_key] = (best_move, min_score)
            return best_move, min_score
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get the best move for the given player."""
        # Clear cache when piece count changes (captures occurred)
        count = sum(1 for i in range(8) for j in range(8) if board[i][j])
        if self.piece_count != count:
            self.transposition_table = {}
            self.piece_count = count
        
        self.root_player = player
        move, score = self.minmax(board, game_obj, player, depth, True)
        print(f"MinMax_DP: {move}, score: {score}, cache size: {len(self.transposition_table)}")
        return move
