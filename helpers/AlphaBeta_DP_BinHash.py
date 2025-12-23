import random
from tokens import Queen, Rook, Bishop, Knight

class AlphaBeta_DP_BinHash:
    """
    Alpha-Beta Pruning with Zobrist-style Hash Transposition Table.
    
    Uses an efficient integer hash that uniquely identifies positions
    for faster transposition table lookups.
    """

    def __init__(self):
        self.name = "AlphaBeta_DP_BinHash"
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
        self.nodes_searched = 0
        self.tt_hits = 0
        
        # Zobrist-style piece encoding
        self.piece_hash = {
            ("pawn", "white"): 1, ("knight", "white"): 2, ("bishop", "white"): 3,
            ("rook", "white"): 4, ("queen", "white"): 5, ("king", "white"): 6,
            ("pawn", "black"): 7, ("knight", "black"): 8, ("bishop", "black"): 9,
            ("rook", "black"): 10, ("queen", "black"): 11, ("king", "black"): 12,
        }
        
        # Pre-compute random numbers for Zobrist hashing
        random.seed(42)  # Fixed seed for reproducibility
        self.zobrist_table = [
            [[random.getrandbits(64) for _ in range(13)] for _ in range(8)]
            for _ in range(8)
        ]
        random.seed()  # Reset to random

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
        """Generate Zobrist hash for the board position."""
        hash_value = 0
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece:
                    piece_id = self.piece_hash.get((piece.name, piece.color), 0)
                    hash_value ^= self.zobrist_table[i][j][piece_id]
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

    def order_moves(self, moves, board, tt_move=None):
        """Order moves for better pruning. TT move first if available."""
        scored_moves = []
        for move in moves:
            score = 0
            
            # TT move gets highest priority
            if tt_move and move == tt_move:
                score = 1000000
            else:
                start, end = move
                target = board[end[0]][end[1]]
                piece = board[start[0]][start[1]]
                
                if target:
                    score += 10000 + self.score[target.name] - self.score[piece.name] // 100
                
                if piece and piece.name == "pawn" and (end[0] == 0 or end[0] == 7):
                    score += 9000
                
                if 2 <= end[0] <= 5 and 2 <= end[1] <= 5:
                    score += 10
            
            scored_moves.append((score, move))
        
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return [move for _, move in scored_moves]

    def alpha_beta(self, board, game_obj, player, alpha, beta, depth, is_maximizing):
        """Alpha-Beta with Zobrist hash transposition table."""
        self.nodes_searched += 1
        
        # Check transposition table
        board_hash = self.get_board_hash(board)
        tt_key = (board_hash, depth)
        tt_move = None
        
        if tt_key in self.transposition_table:
            entry = self.transposition_table[tt_key]
            self.tt_hits += 1
            tt_move = entry.get('move')
            
            if entry['flag'] == 'exact':
                return entry['move'], entry['score']
            elif entry['flag'] == 'lower' and entry['score'] >= beta:
                return entry['move'], entry['score']
            elif entry['flag'] == 'upper' and entry['score'] <= alpha:
                return entry['move'], entry['score']
        
        moves = game_obj.generate_moves_list(player, board)
        
        # Terminal conditions
        if depth == 0:
            return None, self.evaluate_board(board)
        
        if not moves:
            if is_maximizing:
                return None, -1000000 + (10 - depth) * 100
            else:
                return None, 1000000 - (10 - depth) * 100
        
        moves = self.order_moves(moves, board, tt_move)
        best_move = moves[0]
        original_alpha = alpha
        
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
                    break
            
            # Store in TT
            flag = 'exact'
            if max_score <= original_alpha:
                flag = 'upper'
            elif max_score >= beta:
                flag = 'lower'
            
            self.transposition_table[tt_key] = {
                'score': max_score, 'move': best_move, 'flag': flag
            }
            
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
                    break
            
            # Store in TT
            flag = 'exact'
            if min_score >= beta:
                flag = 'lower'
            elif min_score <= alpha:
                flag = 'upper'
            
            self.transposition_table[tt_key] = {
                'score': min_score, 'move': best_move, 'flag': flag
            }
            
            return best_move, min_score
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get the best move for the given player."""
        # Clear cache when piece count changes
        count = sum(1 for i in range(8) for j in range(8) if board[i][j])
        if self.piece_count != count:
            self.transposition_table = {}
            self.piece_count = count
        
        self.root_player = player
        self.nodes_searched = 0
        self.tt_hits = 0
        
        move, score = self.alpha_beta(
            board, game_obj, player,
            -100000000, 100000000, depth, True
        )
        
        print(f"AlphaBeta_DP_BinHash: {move}, score: {score}, nodes: {self.nodes_searched}, TT hits: {self.tt_hits}")
        return move
