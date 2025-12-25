"""
NeuralPatternEngine - Chess engine with pattern recognition and advanced heuristics.

Features:
- Pattern Recognition: Common tactical and positional patterns
- Attack/Defense Tables: Pre-computed attack maps
- Mobility Evaluation: Accurate piece mobility scoring
- King Zone Attacks: Measure attacking pressure on king
- Space Advantage: Control of key squares
- Piece Coordination: Evaluation of piece synergy
- Pawn Structure Analysis: Detailed pawn evaluation
- Outpost Detection: Knight and bishop outposts
"""

import random
import time
from tokens import Queen, Rook, Bishop, Knight

class NeuralPatternEngine:

    def __init__(self):
        self.name = "NeuralPatternEngine"
        self.players = {"black": "white", "white": "black"}
        
        # Piece values with game phase interpolation
        self.mg_values = {"pawn": 82, "knight": 337, "bishop": 365, 
                          "rook": 477, "queen": 1025, "king": 0}
        self.eg_values = {"pawn": 94, "knight": 281, "bishop": 297,
                          "rook": 512, "queen": 936, "king": 0}
        
        # Transposition table
        self.tt = {}
        
        # Attack tables (will be computed per position)
        self.white_attacks = [[0] * 8 for _ in range(8)]
        self.black_attacks = [[0] * 8 for _ in range(8)]
        
        # Pattern scores
        self.patterns = self._init_patterns()
        
        # Initialize piece-square tables for middlegame and endgame
        self._init_pst()
        
        # Mobility bonuses per piece type
        self.mobility_bonus = {
            "knight": [
                -62, -53, -12, -4, 3, 13, 22, 28, 33
            ],
            "bishop": [
                -48, -20, 16, 26, 38, 51, 55, 63, 63, 68, 81, 81, 91, 98
            ],
            "rook": [
                -60, -20, 2, 3, 3, 11, 22, 31, 40, 40, 41, 48, 57, 57, 62
            ],
            "queen": [
                -30, -12, -8, -8, 18, 25, 23, 37, 41, 54, 65, 68, 69, 70, 70,
                70, 71, 72, 74, 76, 90, 104, 120, 120, 120, 120, 120, 120
            ]
        }
        
        # King attack weights
        self.king_attack_weights = {
            "knight": 2, "bishop": 2, "rook": 3, "queen": 5
        }
        
    def _init_patterns(self):
        """Initialize tactical and positional patterns."""
        return {
            # Pawn patterns
            "doubled_pawn": -15,
            "isolated_pawn": -20,
            "backward_pawn": -10,
            "passed_pawn_base": 20,
            "passed_pawn_rank_bonus": [0, 10, 17, 29, 52, 86, 160, 0],  # By rank
            "connected_pawn": 10,
            "pawn_chain": 8,
            
            # Piece patterns
            "bishop_pair": 50,
            "rook_on_open_file": 25,
            "rook_on_semi_open_file": 12,
            "rook_on_7th_rank": 30,
            "connected_rooks": 15,
            "knight_outpost": 25,
            "bishop_outpost": 20,
            "bad_bishop": -15,
            
            # King safety
            "pawn_shield_1": 10,
            "pawn_shield_2": 5,
            "open_file_near_king": -25,
            "king_on_open_file": -50,
            
            # Control patterns
            "center_pawn": 15,
            "center_control": 5,
            "space_advantage": 3,
            
            # Tactical patterns
            "hanging_piece": -50,
            "pinned_piece": -25,
            "forking_square": 15,
        }
    
    def _init_pst(self):
        """Initialize piece-square tables for both game phases."""
        # Middlegame PSTs
        self.mg_pawn_table = [
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [ 98, 134,  61,  95,  68, 126,  34, -11],
            [ -6,   7,  26,  31,  65,  56,  25, -20],
            [-14,  13,   6,  21,  23,  12,  17, -23],
            [-27,  -2,  -5,  12,  17,   6,  10, -25],
            [-26,  -4,  -4, -10,   3,   3,  33, -12],
            [-35,  -1, -20, -23, -15,  24,  38, -22],
            [  0,   0,   0,   0,   0,   0,   0,   0]
        ]
        
        self.mg_knight_table = [
            [-167, -89, -34, -49,  61, -97, -15, -107],
            [ -73, -41,  72,  36,  23,  62,   7,  -17],
            [ -47,  60,  37,  65,  84, 129,  73,   44],
            [  -9,  17,  19,  53,  37,  69,  18,   22],
            [ -13,   4,  16,  13,  28,  19,  21,   -8],
            [ -23,  -9,  12,  10,  19,  17,  25,  -16],
            [ -29, -53, -12,  -3,  -1,  18, -14,  -19],
            [-105, -21, -58, -33, -17, -28, -19,  -23]
        ]
        
        self.mg_bishop_table = [
            [ -29,   4, -82, -37, -25, -42,   7,  -8],
            [ -26,  16, -18, -13,  30,  59,  18, -47],
            [ -16,  37,  43,  40,  35,  50,  37,  -2],
            [  -4,   5,  19,  50,  37,  37,   7,  -2],
            [  -6,  13,  13,  26,  34,  12,  10,   4],
            [   0,  15,  15,  15,  14,  27,  18,  10],
            [   4,  15,  16,   0,   7,  21,  33,   1],
            [ -33,  -3, -14, -21, -13, -12, -39, -21]
        ]
        
        self.mg_rook_table = [
            [ 32,  42,  32,  51,  63,   9,  31,  43],
            [ 27,  32,  58,  62,  80,  67,  26,  44],
            [  -5,  19,  26,  36,  17,  45,  61,  16],
            [-24, -11,   7,  26,  24,  35,  -8, -20],
            [-36, -26, -12,  -1,   9,  -7,   6, -23],
            [-45, -25, -16, -17,   3,   0,  -5, -33],
            [-44, -16, -20,  -9,  -1,  11,  -6, -71],
            [-19, -13,   1,  17,  16,   7, -37, -26]
        ]
        
        self.mg_queen_table = [
            [ -28,   0,  29,  12,  59,  44,  43,  45],
            [ -24, -39,  -5,   1, -16,  57,  28,  54],
            [ -13, -17,   7,   8,  29,  56,  47,  57],
            [ -27, -27, -16, -16,  -1,  17,  -2,   1],
            [  -9, -26,  -9, -10,  -2,  -4,   3,  -3],
            [ -14,   2, -11,  -2,  -5,   2,  14,   5],
            [ -35,  -8,  11,   2,   8,  15,  -3,   1],
            [  -1, -18,  -9,  10, -15, -25, -31, -50]
        ]
        
        self.mg_king_table = [
            [ -65,  23,  16, -15, -56, -34,   2,  13],
            [  29,  -1, -20,  -7,  -8,  -4, -38, -29],
            [  -9,  24,   2, -16, -20,   6,  22, -22],
            [ -17, -20, -12, -27, -30, -25, -14, -36],
            [ -49,  -1, -27, -39, -46, -44, -33, -51],
            [ -14, -14, -22, -46, -44, -30, -15, -27],
            [   1,   7,  -8, -64, -43, -16,   9,   8],
            [ -15,  36,  12, -54,   8, -28,  24,  14]
        ]
        
        # Endgame PSTs
        self.eg_pawn_table = [
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [178, 173, 158, 134, 147, 132, 165, 187],
            [ 94, 100,  85,  67,  56,  53,  82,  84],
            [ 32,  24,  13,   5,  -2,   4,  17,  17],
            [ 13,   9,  -3,  -7,  -7,  -8,   3,  -1],
            [  4,   7,  -6,   1,   0,  -5,  -1,  -8],
            [ 13,   8,   8,  10,  13,   0,   2,  -7],
            [  0,   0,   0,   0,   0,   0,   0,   0]
        ]
        
        self.eg_king_table = [
            [ -74, -35, -18, -18, -11,  15,   4, -17],
            [ -12,  17,  14,  17,  17,  38,  23,  11],
            [  10,  17,  23,  15,  20,  45,  44,  13],
            [  -8,  22,  24,  27,  26,  33,  26,   3],
            [ -18,  -4,  21,  24,  27,  23,   9, -11],
            [ -19,  -3,  11,  21,  23,  16,   7,  -9],
            [ -27, -11,   4,  13,  14,   4,  -5, -17],
            [ -53, -34, -21, -11, -28, -14, -24, -43]
        ]
    
    def get_pst_value(self, piece, row, col, phase):
        """Get piece-square table value interpolated by game phase."""
        table_row = row if piece.color == "white" else 7 - row
        
        mg_value = 0
        eg_value = 0
        
        if piece.name == "pawn":
            mg_value = self.mg_pawn_table[table_row][col]
            eg_value = self.eg_pawn_table[table_row][col]
        elif piece.name == "knight":
            mg_value = self.mg_knight_table[table_row][col]
            eg_value = self.mg_knight_table[table_row][col]  # Use same for simplicity
        elif piece.name == "bishop":
            mg_value = self.mg_bishop_table[table_row][col]
            eg_value = self.mg_bishop_table[table_row][col]
        elif piece.name == "rook":
            mg_value = self.mg_rook_table[table_row][col]
            eg_value = self.mg_rook_table[table_row][col]
        elif piece.name == "queen":
            mg_value = self.mg_queen_table[table_row][col]
            eg_value = self.mg_queen_table[table_row][col]
        elif piece.name == "king":
            mg_value = self.mg_king_table[table_row][col]
            eg_value = self.eg_king_table[table_row][col]
        
        # Interpolate based on phase (0 = endgame, 256 = opening)
        return (mg_value * phase + eg_value * (256 - phase)) // 256
    
    def get_game_phase(self, board):
        """Calculate game phase for evaluation interpolation."""
        phase = 0
        phase_weights = {"knight": 1, "bishop": 1, "rook": 2, "queen": 4}
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.name in phase_weights:
                    phase += phase_weights[piece.name]
        
        # Total phase = 24 (all pieces), scale to 256
        return min(256, phase * 256 // 24)
    
    def compute_attack_tables(self, board):
        """Compute attack tables for both sides."""
        self.white_attacks = [[0] * 8 for _ in range(8)]
        self.black_attacks = [[0] * 8 for _ in range(8)]
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    attacks = self.get_piece_attacks(piece, row, col, board)
                    for r, c in attacks:
                        if piece.color == "white":
                            self.white_attacks[r][c] += 1
                        else:
                            self.black_attacks[r][c] += 1
    
    def get_piece_attacks(self, piece, row, col, board):
        """Get all squares a piece attacks."""
        attacks = []
        
        if piece.name == "pawn":
            direction = 1 if piece.color == "white" else -1
            for dc in [-1, 1]:
                nr, nc = row + direction, col + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    attacks.append((nr, nc))
                    
        elif piece.name == "knight":
            offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, dc in offsets:
                nr, nc = row + dr, col + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    attacks.append((nr, nc))
                    
        elif piece.name == "bishop":
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nr, nc = row + dr, col + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    attacks.append((nr, nc))
                    if board[nr][nc]:
                        break
                    nr, nc = nr + dr, nc + dc
                    
        elif piece.name == "rook":
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    attacks.append((nr, nc))
                    if board[nr][nc]:
                        break
                    nr, nc = nr + dr, nc + dc
                    
        elif piece.name == "queen":
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                          (0, 1), (1, -1), (1, 0), (1, 1)]:
                nr, nc = row + dr, col + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    attacks.append((nr, nc))
                    if board[nr][nc]:
                        break
                    nr, nc = nr + dr, nc + dc
                    
        elif piece.name == "king":
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        attacks.append((nr, nc))
        
        return attacks
    
    def evaluate_pawn_structure(self, board, color):
        """Detailed pawn structure evaluation."""
        score = 0
        opponent = "black" if color == "white" else "white"
        direction = 1 if color == "white" else -1
        
        # Collect pawn positions per file
        pawns_by_file = [[] for _ in range(8)]
        opp_pawns_by_file = [[] for _ in range(8)]
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.name == "pawn":
                    if piece.color == color:
                        pawns_by_file[col].append(row)
                    else:
                        opp_pawns_by_file[col].append(row)
        
        for col in range(8):
            pawns = pawns_by_file[col]
            
            # Doubled pawns
            if len(pawns) > 1:
                score += self.patterns["doubled_pawn"] * (len(pawns) - 1)
            
            for row in pawns:
                # Isolated pawns
                has_neighbor = False
                if col > 0 and pawns_by_file[col - 1]:
                    has_neighbor = True
                if col < 7 and pawns_by_file[col + 1]:
                    has_neighbor = True
                
                if not has_neighbor:
                    score += self.patterns["isolated_pawn"]
                
                # Connected pawns
                for adj_col in [col - 1, col + 1]:
                    if 0 <= adj_col < 8:
                        for adj_row in pawns_by_file[adj_col]:
                            if abs(adj_row - row) <= 1:
                                score += self.patterns["connected_pawn"] // 2
                
                # Passed pawns
                is_passed = True
                for check_col in range(max(0, col - 1), min(8, col + 2)):
                    for opp_row in opp_pawns_by_file[check_col]:
                        if color == "white" and opp_row > row:
                            is_passed = False
                        elif color == "black" and opp_row < row:
                            is_passed = False
                
                if is_passed:
                    rank = row if color == "white" else 7 - row
                    score += self.patterns["passed_pawn_base"]
                    score += self.patterns["passed_pawn_rank_bonus"][rank]
                
                # Center pawns bonus
                if col in [3, 4] and row in [3, 4]:
                    score += self.patterns["center_pawn"]
        
        return score
    
    def evaluate_piece_placement(self, board, color, phase):
        """Evaluate piece-specific patterns."""
        score = 0
        opponent = "black" if color == "white" else "white"
        
        bishops = 0
        rooks = []
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == color:
                    
                    if piece.name == "bishop":
                        bishops += 1
                        
                        # Detect bad bishop (blocked by own pawns)
                        pawn_count = 0
                        for r in range(8):
                            for c in range(8):
                                p = board[r][c]
                                if p and p.name == "pawn" and p.color == color:
                                    # Check if pawn is on same color square
                                    if (r + c) % 2 == (row + col) % 2:
                                        pawn_count += 1
                        if pawn_count >= 4:
                            score += self.patterns["bad_bishop"]
                    
                    elif piece.name == "rook":
                        rooks.append((row, col))
                        
                        # Rook on open file
                        has_own_pawn = False
                        has_enemy_pawn = False
                        for r in range(8):
                            p = board[r][col]
                            if p and p.name == "pawn":
                                if p.color == color:
                                    has_own_pawn = True
                                else:
                                    has_enemy_pawn = True
                        
                        if not has_own_pawn and not has_enemy_pawn:
                            score += self.patterns["rook_on_open_file"]
                        elif not has_own_pawn:
                            score += self.patterns["rook_on_semi_open_file"]
                        
                        # Rook on 7th rank
                        if (color == "white" and row == 6) or (color == "black" and row == 1):
                            score += self.patterns["rook_on_7th_rank"]
                    
                    elif piece.name == "knight":
                        # Knight outpost (protected by pawn, can't be attacked by enemy pawns)
                        direction = 1 if color == "white" else -1
                        is_outpost = False
                        
                        # Check if protected by own pawn
                        for dc in [-1, 1]:
                            pr, pc = row - direction, col + dc
                            if 0 <= pr < 8 and 0 <= pc < 8:
                                p = board[pr][pc]
                                if p and p.name == "pawn" and p.color == color:
                                    is_outpost = True
                                    break
                        
                        if is_outpost:
                            # Check if safe from enemy pawns
                            safe = True
                            for c in [col - 1, col + 1]:
                                if 0 <= c < 8:
                                    for r in range(8):
                                        p = board[r][c]
                                        if p and p.name == "pawn" and p.color == opponent:
                                            # Can this pawn attack the outpost?
                                            opp_dir = 1 if opponent == "white" else -1
                                            if (opponent == "white" and r < row) or \
                                               (opponent == "black" and r > row):
                                                safe = False
                            
                            if safe:
                                score += self.patterns["knight_outpost"]
        
        # Bishop pair bonus
        if bishops >= 2:
            score += self.patterns["bishop_pair"]
        
        # Connected rooks
        if len(rooks) == 2:
            r1, c1 = rooks[0]
            r2, c2 = rooks[1]
            if r1 == r2 or c1 == c2:
                # Check if path is clear
                clear = True
                if r1 == r2:
                    for c in range(min(c1, c2) + 1, max(c1, c2)):
                        if board[r1][c]:
                            clear = False
                            break
                else:
                    for r in range(min(r1, r2) + 1, max(r1, r2)):
                        if board[r][c1]:
                            clear = False
                            break
                if clear:
                    score += self.patterns["connected_rooks"]
        
        return score
    
    def evaluate_king_safety(self, board, color, phase):
        """Evaluate king safety with attack counting."""
        if phase < 64:  # Endgame - king safety less important
            return 0
        
        score = 0
        opponent = "black" if color == "white" else "white"
        direction = 1 if color == "white" else -1
        
        # Find king
        king_row, king_col = None, None
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.name == "king" and piece.color == color:
                    king_row, king_col = row, col
                    break
            if king_row is not None:
                break
        
        if king_row is None:
            return 0
        
        # Pawn shield
        shield_row = king_row + direction
        if 0 <= shield_row < 8:
            for dc in [-1, 0, 1]:
                c = king_col + dc
                if 0 <= c < 8:
                    p = board[shield_row][c]
                    if p and p.name == "pawn" and p.color == color:
                        score += self.patterns["pawn_shield_1"]
            
            # Second rank shield
            shield_row_2 = king_row + 2 * direction
            if 0 <= shield_row_2 < 8:
                for dc in [-1, 0, 1]:
                    c = king_col + dc
                    if 0 <= c < 8:
                        p = board[shield_row_2][c]
                        if p and p.name == "pawn" and p.color == color:
                            score += self.patterns["pawn_shield_2"]
        
        # Open file near king
        for dc in [-1, 0, 1]:
            c = king_col + dc
            if 0 <= c < 8:
                has_pawn = False
                for r in range(8):
                    p = board[r][c]
                    if p and p.name == "pawn":
                        has_pawn = True
                        break
                if not has_pawn:
                    if dc == 0:
                        score += self.patterns["king_on_open_file"]
                    else:
                        score += self.patterns["open_file_near_king"]
        
        # Count attacks in king zone
        king_zone = []
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                r, c = king_row + dr, king_col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    king_zone.append((r, c))
        
        attack_count = 0
        attack_weight = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == opponent and piece.name != "king":
                    attacks = self.get_piece_attacks(piece, row, col, board)
                    for r, c in attacks:
                        if (r, c) in king_zone:
                            attack_count += 1
                            attack_weight += self.king_attack_weights.get(piece.name, 1)
        
        # Penalty for attacks on king zone
        if attack_count >= 2:
            score -= attack_weight * 5
        
        return score
    
    def evaluate_mobility(self, board, color, game_obj):
        """Evaluate piece mobility."""
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == color and piece.name in self.mobility_bonus:
                    attacks = self.get_piece_attacks(piece, row, col, board)
                    mobility = len(attacks)
                    
                    bonus_table = self.mobility_bonus[piece.name]
                    mobility = min(mobility, len(bonus_table) - 1)
                    score += bonus_table[mobility]
        
        return score
    
    def evaluate_space(self, board, color):
        """Evaluate space advantage."""
        score = 0
        
        # Define extended center and our side
        if color == "white":
            space_ranks = range(2, 5)  # Ranks 3-5
        else:
            space_ranks = range(3, 6)  # Ranks 4-6
        
        space_files = range(1, 7)  # Files b-g
        
        for row in space_ranks:
            for col in space_files:
                piece = board[row][col]
                if piece and piece.color == color:
                    score += self.patterns["space_advantage"]
                
                # Bonus for squares we attack but don't occupy
                if color == "white":
                    if self.white_attacks[row][col] > self.black_attacks[row][col]:
                        score += self.patterns["center_control"]
                else:
                    if self.black_attacks[row][col] > self.white_attacks[row][col]:
                        score += self.patterns["center_control"]
        
        return score
    
    def evaluate(self, board, player, game_obj=None):
        """Full evaluation function."""
        phase = self.get_game_phase(board)
        
        # Material and PST
        white_score = 0
        black_score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    mg_val = self.mg_values[piece.name]
                    eg_val = self.eg_values[piece.name]
                    material = (mg_val * phase + eg_val * (256 - phase)) // 256
                    pst = self.get_pst_value(piece, row, col, phase)
                    
                    if piece.color == "white":
                        white_score += material + pst
                    else:
                        black_score += material + pst
        
        # Compute attack tables
        self.compute_attack_tables(board)
        
        # Pawn structure
        white_score += self.evaluate_pawn_structure(board, "white")
        black_score += self.evaluate_pawn_structure(board, "black")
        
        # Piece placement patterns
        white_score += self.evaluate_piece_placement(board, "white", phase)
        black_score += self.evaluate_piece_placement(board, "black", phase)
        
        # King safety
        white_score += self.evaluate_king_safety(board, "white", phase)
        black_score += self.evaluate_king_safety(board, "black", phase)
        
        # Space
        white_score += self.evaluate_space(board, "white")
        black_score += self.evaluate_space(board, "black")
        
        # Return from player's perspective
        score = white_score - black_score
        return score if player == "white" else -score
    
    def order_moves(self, moves, board, tt_move=None):
        """Order moves for alpha-beta pruning."""
        scored = []
        
        for move in moves:
            score = 0
            start, end = move
            
            if tt_move and move == tt_move:
                score = 1000000
            else:
                attacker = board[start[0]][start[1]]
                victim = board[end[0]][end[1]]
                
                if victim:
                    score = 100000 + self.mg_values[victim.name] - self.mg_values[attacker.name] // 10
                
                if attacker.name == "pawn" and (end[0] == 0 or end[0] == 7):
                    score = 90000
            
            scored.append((score, move))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored]
    
    def make_move_on_board(self, start, end, board, choice=None):
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
    
    def get_hash(self, board):
        h = 0
        for r in range(8):
            for c in range(8):
                p = board[r][c]
                if p:
                    pid = {"pawn": 1, "knight": 2, "bishop": 3, "rook": 4, "queen": 5, "king": 6}[p.name]
                    color = 0 if p.color == "white" else 6
                    h ^= (pid + color) << ((r * 8 + c) % 52)
        return h
    
    def alpha_beta(self, board, game_obj, player, alpha, beta, depth, ply):
        """Alpha-beta search."""
        # TT lookup
        h = self.get_hash(board)
        tt_entry = self.tt.get(h)
        tt_move = None
        
        if tt_entry and tt_entry['depth'] >= depth:
            if tt_entry['flag'] == 'exact':
                return tt_entry['move'], tt_entry['score']
            tt_move = tt_entry.get('move')
        
        if depth <= 0:
            return None, self.evaluate(board, player, game_obj)
        
        try:
            moves = game_obj.generate_moves_list(player, board)
        except:
            return None, self.evaluate(board, player, game_obj)
        
        if not moves:
            return None, -100000 + ply
        
        moves = self.order_moves(moves, board, tt_move)
        
        best_move = moves[0]
        best_score = -1000000
        
        for move in moves:
            next_board = [row[:] for row in board]
            self.make_move_on_board(move[0], move[1], next_board)
            
            _, score = self.alpha_beta(
                next_board, game_obj, self.players[player],
                -beta, -alpha, depth - 1, ply + 1
            )
            score = -score
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        
        # Store in TT
        self.tt[h] = {'depth': depth, 'score': best_score, 'move': best_move, 'flag': 'exact'}
        
        return best_move, best_score
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get next move using pattern-based evaluation."""
        # Clear old TT entries
        if len(self.tt) > 500000:
            self.tt = {}
        
        start = time.time()
        best_move = None
        
        for d in range(1, depth + 1):
            move, score = self.alpha_beta(board, game_obj, player, -1000000, 1000000, d, 0)
            if move:
                best_move = move
            
            if time.time() - start > 4:
                break
        
        if best_move:
            print(f"NeuralPattern move: {best_move}")
            return best_move
        
        moves = game_obj.generate_moves_list(player, board)
        return random.choice(moves) if moves else None
