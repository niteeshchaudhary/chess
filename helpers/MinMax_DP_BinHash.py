import random
from tokens import Queen, Rook, Bishop, Knight

class MinMax_DP_BinHash:
    """
    MinMax algorithm with Zobrist-style hashing for the transposition table.
    
    Uses a more efficient integer-based hash that considers both piece positions
    and piece types, not just occupied squares.
    """

    def __init__(self):
        self.name = "MinMax_DP_BinHash"
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
        
        # Piece type encoding for hashing
        self.piece_hash = {
            ("pawn", "white"): 1, ("knight", "white"): 2, ("bishop", "white"): 3,
            ("rook", "white"): 4, ("queen", "white"): 5, ("king", "white"): 6,
            ("pawn", "black"): 7, ("knight", "black"): 8, ("bishop", "black"): 9,
            ("rook", "black"): 10, ("queen", "black"): 11, ("king", "black"): 12,
        }

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
        Generate a Zobrist-style hash for the board.
        Each piece type/color at each position contributes uniquely to the hash.
        """
        hash_value = 0
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece:
                    square = i * 8 + j
                    piece_id = self.piece_hash.get((piece.name, piece.color), 0)
                    # Combine square and piece_id into hash
                    # Use different bit ranges to avoid collisions
                    hash_value ^= (piece_id << (square % 52)) | (square << 4)
        return hash_value

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
        """MinMax with hash-based transposition table."""
        moves = game_obj.generate_moves_list(player, board)
        
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
            
            self.transposition_table[tt_key] = (best_move, min_score)
            return best_move, min_score
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get the best move for the given player."""
        # Clear cache when piece count changes
        count = sum(1 for i in range(8) for j in range(8) if board[i][j])
        if self.piece_count != count:
            self.transposition_table = {}
            self.piece_count = count
        
        self.root_player = player
        move, score = self.minmax(board, game_obj, player, depth, True)
        print(f"MinMax_DP_BinHash: {move}, score: {score}")
        return move
