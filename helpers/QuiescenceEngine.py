"""
QuiescenceEngine - Advanced chess engine with quiescence search and pruning techniques.

Advanced Features:
- Quiescence Search: Extends search at tactical positions to avoid horizon effect
- Null Move Pruning: Skip turns to quickly identify losing positions
- Late Move Reduction (LMR): Search less promising moves at reduced depth
- Futility Pruning: Skip moves that can't improve position significantly
- Static Exchange Evaluation (SEE): Evaluate capture sequences
- Aspiration Windows: Narrow search windows for faster iterative deepening
- Principal Variation Search (PVS): More efficient alpha-beta variant
"""

import random
import time
from tokens import Queen, Rook, Bishop, Knight

class QuiescenceEngine:

    def __init__(self):
        self.name = "QuiescenceEngine"
        self.players = {"black": "white", "white": "black"}
        
        # Piece values (centipawns)
        self.piece_values = {
            "pawn": 100,
            "knight": 320,
            "bishop": 330,
            "rook": 500,
            "queen": 900,
            "king": 20000
        }
        
        # MVV-LVA table for capture ordering
        self.mvv_lva = {}
        self._init_mvv_lva()
        
        # Transposition table with depth and flag
        self.tt = {}
        self.tt_size = 0
        self.max_tt_size = 500000
        
        # Search statistics
        self.nodes_searched = 0
        self.quiescence_nodes = 0
        self.null_move_cutoffs = 0
        self.lmr_reductions = 0
        
        # Killer moves (2 per ply)
        self.killer_moves = [[None, None] for _ in range(64)]
        
        # History heuristic
        self.history = [[0] * 64 for _ in range(64)]
        
        # Counter moves
        self.counter_moves = {}
        
        # Principal variation
        self.pv_table = {}
        
        # Null move parameters
        self.null_move_reduction = 3
        self.null_move_margin = 120
        
        # LMR parameters
        self.lmr_full_depth_moves = 4
        self.lmr_reduction_limit = 3
        
        # Futility pruning margins
        self.futility_margin = [0, 200, 300, 500]
        
        # Piece-square tables
        self._init_pst()
        
    def _init_mvv_lva(self):
        """Initialize MVV-LVA scoring table."""
        pieces = ["pawn", "knight", "bishop", "rook", "queen", "king"]
        for victim in pieces:
            for attacker in pieces:
                victim_val = self.piece_values[victim]
                attacker_val = self.piece_values[attacker]
                # Higher score = better capture (high value victim, low value attacker)
                self.mvv_lva[(victim, attacker)] = victim_val * 10 - attacker_val
    
    def _init_pst(self):
        """Initialize piece-square tables."""
        # Pawn PST
        self.pawn_pst = [
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [ 50,  50,  50,  50,  50,  50,  50,  50],
            [ 10,  10,  20,  30,  30,  20,  10,  10],
            [  5,   5,  10,  25,  25,  10,   5,   5],
            [  0,   0,   0,  20,  20,   0,   0,   0],
            [  5,  -5, -10,   0,   0, -10,  -5,   5],
            [  5,  10,  10, -20, -20,  10,  10,   5],
            [  0,   0,   0,   0,   0,   0,   0,   0]
        ]
        
        # Knight PST
        self.knight_pst = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20,   0,   0,   0,   0, -20, -40],
            [-30,   0,  10,  15,  15,  10,   0, -30],
            [-30,   5,  15,  20,  20,  15,   5, -30],
            [-30,   0,  15,  20,  20,  15,   0, -30],
            [-30,   5,  10,  15,  15,  10,   5, -30],
            [-40, -20,   0,   5,   5,   0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ]
        
        # Bishop PST
        self.bishop_pst = [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   5,   5,  10,  10,   5,   5, -10],
            [-10,   0,  10,  10,  10,  10,   0, -10],
            [-10,  10,  10,  10,  10,  10,  10, -10],
            [-10,   5,   0,   0,   0,   0,   5, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ]
        
        # Rook PST
        self.rook_pst = [
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [  5,  10,  10,  10,  10,  10,  10,   5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [  0,   0,   0,   5,   5,   0,   0,   0]
        ]
        
        # Queen PST
        self.queen_pst = [
            [-20, -10, -10,  -5,  -5, -10, -10, -20],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10,   0,   5,   5,   5,   5,   0, -10],
            [ -5,   0,   5,   5,   5,   5,   0,  -5],
            [  0,   0,   5,   5,   5,   5,   0,  -5],
            [-10,   5,   5,   5,   5,   5,   0, -10],
            [-10,   0,   5,   0,   0,   0,   0, -10],
            [-20, -10, -10,  -5,  -5, -10, -10, -20]
        ]
        
        # King middle game PST
        self.king_mg_pst = [
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [ 20,  20,   0,   0,   0,   0,  20,  20],
            [ 20,  30,  10,   0,   0,  10,  30,  20]
        ]
        
        # King endgame PST
        self.king_eg_pst = [
            [-50, -40, -30, -20, -20, -30, -40, -50],
            [-30, -20, -10,   0,   0, -10, -20, -30],
            [-30, -10,  20,  30,  30,  20, -10, -30],
            [-30, -10,  30,  40,  40,  30, -10, -30],
            [-30, -10,  30,  40,  40,  30, -10, -30],
            [-30, -10,  20,  30,  30,  20, -10, -30],
            [-30, -30,   0,   0,   0,   0, -30, -30],
            [-50, -30, -30, -30, -30, -30, -30, -50]
        ]
    
    def get_pst_value(self, piece, row, col, is_endgame=False):
        """Get piece-square table value."""
        table_row = row if piece.color == "white" else 7 - row
        
        if piece.name == "pawn":
            return self.pawn_pst[table_row][col]
        elif piece.name == "knight":
            return self.knight_pst[table_row][col]
        elif piece.name == "bishop":
            return self.bishop_pst[table_row][col]
        elif piece.name == "rook":
            return self.rook_pst[table_row][col]
        elif piece.name == "queen":
            return self.queen_pst[table_row][col]
        elif piece.name == "king":
            if is_endgame:
                return self.king_eg_pst[table_row][col]
            return self.king_mg_pst[table_row][col]
        return 0
    
    def is_endgame(self, board):
        """Detect if we're in endgame."""
        queens = 0
        minor_pieces = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    if piece.name == "queen":
                        queens += 1
                    elif piece.name in ["bishop", "knight"]:
                        minor_pieces += 1
        
        return queens == 0 or (queens <= 2 and minor_pieces <= 4)
    
    def evaluate(self, board, player):
        """Static evaluation function."""
        score = 0
        is_eg = self.is_endgame(board)
        
        white_material = 0
        black_material = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    value = self.piece_values[piece.name]
                    pst = self.get_pst_value(piece, row, col, is_eg)
                    
                    if piece.color == "white":
                        white_material += value
                        score += value + pst
                    else:
                        black_material += value
                        score -= value + pst
        
        # Add tempo bonus
        if player == "white":
            score += 10
        else:
            score -= 10
        
        return score if player == "white" else -score
    
    def get_board_hash(self, board):
        """Generate hash for transposition table."""
        h = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    piece_id = {"pawn": 1, "knight": 2, "bishop": 3,
                               "rook": 4, "queen": 5, "king": 6}[piece.name]
                    color_mult = 1 if piece.color == "white" else 7
                    h ^= (piece_id * color_mult) << ((row * 8 + col) % 50)
        return h
    
    def is_capture(self, board, move):
        """Check if move is a capture."""
        return board[move[1][0]][move[1][1]] is not None
    
    def is_promotion(self, board, move):
        """Check if move is a pawn promotion."""
        piece = board[move[0][0]][move[0][1]]
        if piece and piece.name == "pawn":
            return move[1][0] == 0 or move[1][0] == 7
        return False
    
    def gives_check(self, board, move, game_obj, player):
        """Check if move gives check (simplified)."""
        # This is expensive, so we use a simplified version
        piece = board[move[0][0]][move[0][1]]
        if piece and piece.name in ["queen", "rook", "bishop"]:
            return True  # Assume sliding pieces might give check
        return False
    
    def see(self, board, move):
        """Static Exchange Evaluation - evaluate capture sequences."""
        target = board[move[1][0]][move[1][1]]
        attacker = board[move[0][0]][move[0][1]]
        
        if not target:
            return 0
        
        # Simple SEE: just compare piece values
        gain = self.piece_values[target.name]
        risk = self.piece_values[attacker.name]
        
        # Rough estimate: if we're capturing with a less valuable piece, it's good
        if gain >= risk:
            return gain
        
        # Otherwise, assume we might lose our piece
        return gain - risk
    
    def order_moves(self, moves, board, depth, pv_move=None):
        """Order moves for optimal alpha-beta pruning."""
        scored_moves = []
        
        for move in moves:
            score = 0
            start, end = move
            
            # PV move gets highest priority
            if pv_move and move == pv_move:
                score = 100000000
            else:
                attacker = board[start[0]][start[1]]
                victim = board[end[0]][end[1]]
                
                # Captures: use MVV-LVA
                if victim:
                    mvv_lva_key = (victim.name, attacker.name)
                    score = 10000000 + self.mvv_lva.get(mvv_lva_key, 0)
                    
                    # Use SEE for more accurate capture ordering
                    see_score = self.see(board, move)
                    if see_score < 0:
                        score -= 5000000  # Losing capture
                
                # Promotions
                elif attacker.name == "pawn" and (end[0] == 0 or end[0] == 7):
                    score = 9000000
                
                # Killer moves
                elif depth < len(self.killer_moves):
                    if move == self.killer_moves[depth][0]:
                        score = 8000000
                    elif move == self.killer_moves[depth][1]:
                        score = 7000000
                
                # History heuristic
                if score == 0:
                    from_sq = start[0] * 8 + start[1]
                    to_sq = end[0] * 8 + end[1]
                    score = self.history[from_sq][to_sq]
            
            scored_moves.append((score, move))
        
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored_moves]
    
    def get_captures(self, moves, board):
        """Filter only capture moves for quiescence search."""
        captures = []
        for move in moves:
            if board[move[1][0]][move[1][1]] is not None:
                captures.append(move)
        return captures
    
    def quiescence(self, board, game_obj, player, alpha, beta, depth=0):
        """
        Quiescence search - continue searching captures until position is quiet.
        Avoids horizon effect where we stop search just before a winning/losing capture.
        """
        self.quiescence_nodes += 1
        
        # Stand pat - what if we just don't make any capture?
        stand_pat = self.evaluate(board, player)
        
        if stand_pat >= beta:
            return beta
        
        # Delta pruning - if even capturing a queen won't help, give up
        delta = 900  # Queen value
        if stand_pat + delta < alpha:
            return alpha
        
        if alpha < stand_pat:
            alpha = stand_pat
        
        # Limit quiescence depth
        if depth > 8:
            return stand_pat
        
        # Get all moves and filter to captures
        try:
            moves = game_obj.generate_moves_list(player, board)
            captures = self.get_captures(moves, board)
        except:
            return stand_pat
        
        if not captures:
            return stand_pat
        
        # Order captures by SEE
        captures = self.order_moves(captures, board, 0)
        
        for move in captures:
            # SEE pruning - skip clearly losing captures
            if self.see(board, move) < 0:
                continue
            
            next_board = [row[:] for row in board]
            self.make_move_on_board(move[0], move[1], next_board)
            
            score = -self.quiescence(
                next_board, game_obj, self.players[player],
                -beta, -alpha, depth + 1
            )
            
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        
        return alpha
    
    def null_move_allowed(self, board, player):
        """Check if null move pruning is safe."""
        # Don't do null move if we only have pawns and king
        piece_count = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == player:
                    if piece.name not in ["pawn", "king"]:
                        piece_count += 1
        
        return piece_count >= 2
    
    def make_move_on_board(self, start, end, board, choice=None):
        """Make a move on the board."""
        piece = board[start[0]][start[1]]
        if piece:
            piece.has_moved = True
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
        
        if piece and piece.name == "pawn" and (end[0] == 0 or end[0] == 7):
            if choice == "rook":
                board[end[0]][end[1]] = Rook(piece.color)
            elif choice == "bishop":
                board[end[0]][end[1]] = Bishop(piece.color)
            elif choice == "knight":
                board[end[0]][end[1]] = Knight(piece.color)
            else:
                board[end[0]][end[1]] = Queen(piece.color)
    
    def choose_piece(self, position):
        return 'queen'
    
    def pvs(self, board, game_obj, player, alpha, beta, depth, ply, do_null=True):
        """
        Principal Variation Search with advanced pruning techniques.
        """
        self.nodes_searched += 1
        
        # Check transposition table
        board_hash = self.get_board_hash(board)
        tt_entry = self.tt.get(board_hash)
        pv_move = None
        
        if tt_entry and tt_entry['depth'] >= depth:
            if tt_entry['flag'] == 'exact':
                return tt_entry['move'], tt_entry['score']
            elif tt_entry['flag'] == 'lower' and tt_entry['score'] >= beta:
                return tt_entry['move'], tt_entry['score']
            elif tt_entry['flag'] == 'upper' and tt_entry['score'] <= alpha:
                return tt_entry['move'], tt_entry['score']
            pv_move = tt_entry.get('move')
        
        # Quiescence search at leaf nodes
        if depth <= 0:
            return None, self.quiescence(board, game_obj, player, alpha, beta)
        
        # Generate moves
        try:
            moves = game_obj.generate_moves_list(player, board)
        except:
            return None, self.evaluate(board, player)
        
        if not moves:
            # Checkmate or stalemate
            return None, -100000 + ply
        
        # Null move pruning
        if do_null and depth >= 3 and not self.is_endgame(board):
            if self.null_move_allowed(board, player):
                # Skip our turn and see if opponent can still improve
                null_score = -self.pvs(
                    board, game_obj, self.players[player],
                    -beta, -beta + 1, depth - self.null_move_reduction - 1,
                    ply + 1, False
                )[1]
                
                if null_score >= beta:
                    self.null_move_cutoffs += 1
                    return None, beta
        
        # Order moves
        moves = self.order_moves(moves, board, ply, pv_move)
        
        best_move = moves[0]
        best_score = -1000000
        
        # PVS search
        for i, move in enumerate(moves):
            next_board = [row[:] for row in board]
            self.make_move_on_board(move[0], move[1], next_board)
            
            # Late Move Reduction
            reduction = 0
            if (i >= self.lmr_full_depth_moves and 
                depth >= 3 and
                not self.is_capture(board, move) and
                not self.is_promotion(board, move)):
                reduction = 1 + (i // 6)
                reduction = min(reduction, self.lmr_reduction_limit)
                self.lmr_reductions += 1
            
            if i == 0:
                # Search first move with full window
                _, score = self.pvs(
                    next_board, game_obj, self.players[player],
                    -beta, -alpha, depth - 1, ply + 1
                )
                score = -score
            else:
                # Search with reduced depth and null window
                _, score = self.pvs(
                    next_board, game_obj, self.players[player],
                    -alpha - 1, -alpha, depth - 1 - reduction, ply + 1
                )
                score = -score
                
                # Re-search with full window if needed
                if score > alpha and score < beta:
                    _, score = self.pvs(
                        next_board, game_obj, self.players[player],
                        -beta, -alpha, depth - 1, ply + 1
                    )
                    score = -score
            
            if score > best_score:
                best_score = score
                best_move = move
            
            if score > alpha:
                alpha = score
                
                # Update history for non-captures
                if not self.is_capture(board, move):
                    from_sq = move[0][0] * 8 + move[0][1]
                    to_sq = move[1][0] * 8 + move[1][1]
                    self.history[from_sq][to_sq] += depth * depth
            
            if alpha >= beta:
                # Store killer move
                if not self.is_capture(board, move):
                    if move != self.killer_moves[ply][0]:
                        self.killer_moves[ply][1] = self.killer_moves[ply][0]
                        self.killer_moves[ply][0] = move
                break
        
        # Store in transposition table
        if self.tt_size < self.max_tt_size:
            flag = 'exact'
            if best_score <= alpha:
                flag = 'upper'
            elif best_score >= beta:
                flag = 'lower'
            
            self.tt[board_hash] = {
                'depth': depth,
                'score': best_score,
                'flag': flag,
                'move': best_move
            }
            self.tt_size += 1
        
        return best_move, best_score
    
    def iterative_deepening(self, board, game_obj, player, max_depth, time_limit=5.0):
        """Iterative deepening with aspiration windows."""
        start_time = time.time()
        best_move = None
        best_score = 0
        
        # Reset statistics
        self.nodes_searched = 0
        self.quiescence_nodes = 0
        self.null_move_cutoffs = 0
        self.lmr_reductions = 0
        
        for depth in range(1, max_depth + 1):
            # Aspiration window
            if depth >= 4 and best_move:
                delta = 50
                alpha = best_score - delta
                beta = best_score + delta
                
                move, score = self.pvs(board, game_obj, player, alpha, beta, depth, 0)
                
                # Re-search with full window if we fail
                if score <= alpha or score >= beta:
                    move, score = self.pvs(board, game_obj, player, -100000, 100000, depth, 0)
            else:
                move, score = self.pvs(board, game_obj, player, -100000, 100000, depth, 0)
            
            if move:
                best_move = move
                best_score = score
            
            elapsed = time.time() - start_time
            if elapsed > time_limit * 0.7:
                break
        
        print(f"Depth: {depth}, Nodes: {self.nodes_searched}, Q-Nodes: {self.quiescence_nodes}")
        print(f"Null cuts: {self.null_move_cutoffs}, LMR: {self.lmr_reductions}")
        
        return best_move, best_score
    
    def getNextMove(self, board, game_obj, player="black", depth=5):
        """Get the next best move."""
        # Clear old data
        if self.tt_size > self.max_tt_size // 2:
            self.tt = {}
            self.tt_size = 0
        
        # Reduce history values to prevent overflow
        for i in range(64):
            for j in range(64):
                self.history[i][j] //= 2
        
        move, score = self.iterative_deepening(board, game_obj, player, depth, time_limit=4.0)
        
        if move:
            print(f"Best move: {move}, Score: {score}")
            return move
        
        # Fallback
        moves = game_obj.generate_moves_list(player, board)
        if moves:
            return random.choice(moves)
        return None

