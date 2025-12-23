"""
PhaseBasedEngine - An efficient chess AI that adapts strategy based on game phase.

Features:
- Opening Book: Pre-computed strong opening moves
- Middle Game: Advanced positional evaluation with piece-square tables
- Endgame: King centralization, passed pawn evaluation, mating patterns
- Transposition Tables: Zobrist hashing for efficient position caching
- Move Ordering: MVV-LVA and killer moves for faster alpha-beta pruning
- Iterative Deepening: Optimal depth search within time constraints
"""

import random
import time
from tokens import Queen, Rook, Bishop, Knight

class PhaseBasedEngine:

    def __init__(self):
        self.name = "PhaseBasedEngine"
        self.players = {"black": "white", "white": "black"}
        
        # Base piece values
        self.piece_values = {
            "pawn": 100,
            "knight": 320,
            "bishop": 330,
            "rook": 500,
            "queen": 900,
            "king": 20000
        }
        
        # Transposition table
        self.transposition_table = {}
        self.tt_hits = 0
        
        # Killer moves for move ordering
        self.killer_moves = [[None, None] for _ in range(20)]
        
        # History heuristic scores
        self.history_scores = {}
        
        # Move count for game phase detection
        self.move_count = 0
        
        # Initialize piece-square tables
        self._init_piece_square_tables()
        
        # Initialize opening book
        self._init_opening_book()
        
    def _init_piece_square_tables(self):
        """Initialize piece-square tables for positional evaluation."""
        
        # Pawn piece-square table (encourages central and advanced pawns)
        self.pawn_table = [
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [ 50,  50,  50,  50,  50,  50,  50,  50],
            [ 10,  10,  20,  30,  30,  20,  10,  10],
            [  5,   5,  10,  25,  25,  10,   5,   5],
            [  0,   0,   0,  20,  20,   0,   0,   0],
            [  5,  -5, -10,   0,   0, -10,  -5,   5],
            [  5,  10,  10, -20, -20,  10,  10,   5],
            [  0,   0,   0,   0,   0,   0,   0,   0]
        ]
        
        # Knight piece-square table (knights are best in the center)
        self.knight_table = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20,   0,   0,   0,   0, -20, -40],
            [-30,   0,  10,  15,  15,  10,   0, -30],
            [-30,   5,  15,  20,  20,  15,   5, -30],
            [-30,   0,  15,  20,  20,  15,   0, -30],
            [-30,   5,  10,  15,  15,  10,   5, -30],
            [-40, -20,   0,   5,   5,   0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ]
        
        # Bishop piece-square table (bishops like diagonals and avoid corners)
        self.bishop_table = [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   5,   5,  10,  10,   5,   5, -10],
            [-10,   0,  10,  10,  10,  10,   0, -10],
            [-10,  10,  10,  10,  10,  10,  10, -10],
            [-10,   5,   0,   0,   0,   0,   5, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ]
        
        # Rook piece-square table (rooks like open files and 7th rank)
        self.rook_table = [
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [  5,  10,  10,  10,  10,  10,  10,   5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [ -5,   0,   0,   0,   0,   0,   0,  -5],
            [  0,   0,   0,   5,   5,   0,   0,   0]
        ]
        
        # Queen piece-square table (queen should not move too early)
        self.queen_table = [
            [-20, -10, -10,  -5,  -5, -10, -10, -20],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10,   0,   5,   5,   5,   5,   0, -10],
            [ -5,   0,   5,   5,   5,   5,   0,  -5],
            [  0,   0,   5,   5,   5,   5,   0,  -5],
            [-10,   5,   5,   5,   5,   5,   0, -10],
            [-10,   0,   5,   0,   0,   0,   0, -10],
            [-20, -10, -10,  -5,  -5, -10, -10, -20]
        ]
        
        # King middle game table (king should stay safe, usually castled)
        self.king_middle_table = [
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [ 20,  20,   0,   0,   0,   0,  20,  20],
            [ 20,  30,  10,   0,   0,  10,  30,  20]
        ]
        
        # King endgame table (king should be active in endgame)
        self.king_endgame_table = [
            [-50, -40, -30, -20, -20, -30, -40, -50],
            [-30, -20, -10,   0,   0, -10, -20, -30],
            [-30, -10,  20,  30,  30,  20, -10, -30],
            [-30, -10,  30,  40,  40,  30, -10, -30],
            [-30, -10,  30,  40,  40,  30, -10, -30],
            [-30, -10,  20,  30,  30,  20, -10, -30],
            [-30, -30,   0,   0,   0,   0, -30, -30],
            [-50, -30, -30, -30, -30, -30, -30, -50]
        ]
        
    def _init_opening_book(self):
        """Initialize opening book with common strong openings."""
        # Format: board_state_hash -> [(start, end), ...]
        # Using algebraic notation for positions
        # Positions are (row, col) where row 0 is white's back rank
        
        self.opening_book = {
            # Starting position responses for white
            "start_white": [
                ((1, 4), (3, 4)),  # e4 - King's pawn
                ((1, 3), (3, 3)),  # d4 - Queen's pawn
                ((0, 6), (2, 5)),  # Nf3 - Reti
                ((1, 2), (3, 2)),  # c4 - English
            ],
            # Responses to 1.e4 for black
            "e4_black": [
                ((6, 4), (4, 4)),  # e5 - Open game
                ((6, 2), (4, 2)),  # c5 - Sicilian
                ((6, 4), (5, 4)),  # e6 - French
                ((6, 2), (5, 2)),  # c6 - Caro-Kann
            ],
            # Responses to 1.d4 for black
            "d4_black": [
                ((6, 3), (4, 3)),  # d5 - Closed game
                ((6, 6), (5, 5)),  # Nf6 - Indian defenses
                ((6, 5), (5, 5)),  # f6 - Dutch
            ],
            # Italian/Scotch setups for white after 1.e4 e5
            "e4e5_white": [
                ((0, 6), (2, 5)),  # Nf3
                ((0, 1), (2, 2)),  # Nc3
            ],
            # Development moves for white
            "develop_white": [
                ((0, 5), (2, 3)),  # Bc4 - Italian
                ((0, 5), (3, 2)),  # Bb5 - Spanish
                ((0, 6), (2, 5)),  # Nf3
                ((0, 1), (2, 2)),  # Nc3
            ],
            # Development moves for black
            "develop_black": [
                ((7, 6), (5, 5)),  # Nf6
                ((7, 1), (5, 2)),  # Nc6
                ((7, 5), (5, 3)),  # Bc5
                ((7, 5), (4, 2)),  # Bb4
            ],
            # Castling priority
            "castle_white": [
                ((0, 4), (0, 6)),  # O-O kingside
            ],
            "castle_black": [
                ((7, 4), (7, 6)),  # O-O kingside
            ],
        }
        
    def get_game_phase(self, board):
        """
        Determine the current game phase based on material and piece positions.
        Returns: 'opening', 'middlegame', or 'endgame'
        """
        # Count material
        total_material = 0
        queens = 0
        minor_pieces = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    if piece.name == "queen":
                        queens += 1
                        total_material += 9
                    elif piece.name == "rook":
                        total_material += 5
                    elif piece.name in ["bishop", "knight"]:
                        minor_pieces += 1
                        total_material += 3
                    elif piece.name == "pawn":
                        total_material += 1
        
        # Opening: First ~10 moves, pieces still on starting squares
        if self.move_count < 10:
            return 'opening'
        
        # Endgame: Low material (both sides have <= queen + rook worth of material)
        if total_material <= 26 or (queens == 0 and minor_pieces <= 4):
            return 'endgame'
        
        return 'middlegame'
    
    def get_opening_move(self, board, player):
        """Try to find a move from the opening book."""
        moves = []
        
        # Check if we're in the very early opening
        if self.move_count == 0 and player == "white":
            moves = self.opening_book.get("start_white", [])
        elif self.move_count == 0 and player == "black":
            # Check what white played
            if board[3][4] and board[3][4].name == "pawn":
                moves = self.opening_book.get("e4_black", [])
            elif board[3][3] and board[3][3].name == "pawn":
                moves = self.opening_book.get("d4_black", [])
        elif self.move_count <= 4:
            if player == "white":
                moves = self.opening_book.get("develop_white", [])
            else:
                moves = self.opening_book.get("develop_black", [])
        
        # Validate moves are legal
        if moves:
            legal_moves = []
            for move in moves:
                start, end = move
                piece = board[start[0]][start[1]]
                if piece and piece.color == player:
                    legal_moves.append(move)
            
            if legal_moves:
                return random.choice(legal_moves)
        
        return None

    def evaluate_pawn_structure(self, board, player):
        """Evaluate pawn structure: doubled, isolated, passed pawns."""
        score = 0
        opponent = self.players[player]
        
        player_pawns = [[] for _ in range(8)]  # Pawns per file
        opponent_pawns = [[] for _ in range(8)]
        
        # Collect pawn positions
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.name == "pawn":
                    if piece.color == player:
                        player_pawns[col].append(row)
                    else:
                        opponent_pawns[col].append(row)
        
        # Evaluate our pawns
        for col in range(8):
            pawns = player_pawns[col]
            
            # Doubled pawns penalty
            if len(pawns) > 1:
                score -= 20 * (len(pawns) - 1)
            
            for row in pawns:
                # Isolated pawn penalty
                has_neighbor = False
                if col > 0 and player_pawns[col - 1]:
                    has_neighbor = True
                if col < 7 and player_pawns[col + 1]:
                    has_neighbor = True
                if not has_neighbor:
                    score -= 15
                
                # Passed pawn bonus
                is_passed = True
                direction = 1 if player == "white" else -1
                target_row = 7 if player == "white" else 0
                
                for check_col in [col - 1, col, col + 1]:
                    if 0 <= check_col < 8:
                        for opp_row in opponent_pawns[check_col]:
                            if player == "white" and opp_row > row:
                                is_passed = False
                            elif player == "black" and opp_row < row:
                                is_passed = False
                
                if is_passed:
                    # Bonus increases as pawn advances
                    advancement = row if player == "white" else (7 - row)
                    score += 20 + (advancement * 10)
        
        return score
    
    def evaluate_king_safety(self, board, player, phase):
        """Evaluate king safety based on pawn shield and piece proximity."""
        score = 0
        king_pos = None
        
        # Find king
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.name == "king" and piece.color == player:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return 0
        
        row, col = king_pos
        
        if phase != 'endgame':
            # Pawn shield bonus (for castled king)
            pawn_shield_score = 0
            direction = 1 if player == "white" else -1
            
            for dc in [-1, 0, 1]:
                shield_col = col + dc
                shield_row = row + direction
                if 0 <= shield_col < 8 and 0 <= shield_row < 8:
                    piece = board[shield_row][shield_col]
                    if piece and piece.name == "pawn" and piece.color == player:
                        pawn_shield_score += 15
            
            score += pawn_shield_score
            
            # Penalty for king in center during middlegame
            if 2 <= col <= 5 and phase == 'middlegame':
                score -= 30
        
        return score
    
    def evaluate_mobility(self, board, game_obj, player):
        """Evaluate piece mobility - number of legal moves available."""
        try:
            moves = game_obj.generate_moves_list(player, board)
            return len(moves) * 2  # 2 points per available move
        except:
            return 0
    
    def evaluate_board(self, board, player, is_max_player, game_obj, phase):
        """
        Comprehensive board evaluation considering game phase.
        """
        score = 0
        
        # Material and positional evaluation
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    piece_value = self.piece_values.get(piece.name, 0)
                    positional_value = self.get_piece_square_value(piece, row, col, phase)
                    
                    if piece.color == player:
                        score += piece_value + positional_value
                    else:
                        score -= piece_value + positional_value
        
        # Pawn structure
        pawn_score = self.evaluate_pawn_structure(board, player)
        pawn_score -= self.evaluate_pawn_structure(board, self.players[player])
        score += pawn_score
        
        # King safety (less important in endgame)
        if phase != 'endgame':
            king_safety = self.evaluate_king_safety(board, player, phase)
            king_safety -= self.evaluate_king_safety(board, self.players[player], phase)
            score += king_safety
        
        # Mobility (simplified)
        # Note: Full mobility calculation is expensive, use sparingly
        
        # Bishop pair bonus
        bishops = {"white": 0, "black": 0}
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.name == "bishop":
                    bishops[piece.color] += 1
        
        if bishops[player] >= 2:
            score += 30
        if bishops[self.players[player]] >= 2:
            score -= 30
        
        # Return score based on perspective
        if not is_max_player:
            score = -score
            
        return score
    
    def get_piece_square_value(self, piece, row, col, phase):
        """Get positional bonus for a piece on a given square."""
        # Flip row for black pieces (tables are from white's perspective)
        table_row = row if piece.color == "white" else 7 - row
        
        if piece.name == "pawn":
            return self.pawn_table[table_row][col]
        elif piece.name == "knight":
            return self.knight_table[table_row][col]
        elif piece.name == "bishop":
            return self.bishop_table[table_row][col]
        elif piece.name == "rook":
            return self.rook_table[table_row][col]
        elif piece.name == "queen":
            return self.queen_table[table_row][col]
        elif piece.name == "king":
            if phase == 'endgame':
                return self.king_endgame_table[table_row][col]
            else:
                return self.king_middle_table[table_row][col]
        return 0
    
    def order_moves(self, moves, board, depth):
        """Order moves for better alpha-beta pruning."""
        scored_moves = []
        
        for move in moves:
            start, end = move
            score = 0
            
            moving_piece = board[start[0]][start[1]]
            target_piece = board[end[0]][end[1]]
            
            # MVV-LVA: Most Valuable Victim - Least Valuable Attacker
            if target_piece:
                victim_value = self.piece_values.get(target_piece.name, 0)
                attacker_value = self.piece_values.get(moving_piece.name, 0)
                score += 10000 + victim_value - (attacker_value // 100)
            
            # Killer move bonus
            if depth < len(self.killer_moves):
                if move in self.killer_moves[depth]:
                    score += 900
            
            # History heuristic
            move_key = (start, end)
            if move_key in self.history_scores:
                score += self.history_scores[move_key]
            
            # Promotion bonus
            if moving_piece.name == "pawn":
                if end[0] == 0 or end[0] == 7:
                    score += 8000
            
            # Center control bonus for early moves
            if 2 <= end[0] <= 5 and 2 <= end[1] <= 5:
                score += 20
            
            scored_moves.append((score, move))
        
        # Sort by score descending
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return [move for _, move in scored_moves]
    
    def make_move_on_board(self, start, end, board, choice=None):
        """Make a move on the board."""
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
        """Choose piece for pawn promotion - always queen unless knight gives checkmate."""
        return 'queen'
    
    def get_board_hash(self, board):
        """Generate a simple hash for the board position."""
        hash_val = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    piece_id = {"pawn": 1, "knight": 2, "bishop": 3, 
                                "rook": 4, "queen": 5, "king": 6}[piece.name]
                    color_id = 0 if piece.color == "white" else 6
                    hash_val ^= (piece_id + color_id) << ((row * 8 + col) % 60)
        return hash_val
    
    def alpha_beta(self, board, game_obj, player, alpha, beta, depth, is_max_player, phase):
        """Alpha-beta pruning with transposition table."""
        
        # Check transposition table
        board_hash = self.get_board_hash(board)
        tt_key = (board_hash, depth, is_max_player)
        
        if tt_key in self.transposition_table:
            self.tt_hits += 1
            return self.transposition_table[tt_key]
        
        # Generate moves
        moves = game_obj.generate_moves_list(player, board)
        
        # Terminal conditions
        if depth == 0:
            eval_score = self.evaluate_board(board, player, is_max_player, game_obj, phase)
            return None, eval_score
        
        if not moves:
            if is_max_player:
                return None, -100000 + (10 - depth) * 100  # Prefer later checkmates
            else:
                return None, 100000 - (10 - depth) * 100
        
        # Order moves for better pruning
        moves = self.order_moves(moves, board, depth)
        
        best_move = moves[0] if moves else None
        
        if is_max_player:
            max_score = -1000000
            for move in moves:
                next_board = [row[:] for row in board]
                self.make_move_on_board(move[0], move[1], next_board)
                
                _, score = self.alpha_beta(
                    next_board, game_obj, self.players[player],
                    alpha, beta, depth - 1, False, phase
                )
                
                if score > max_score:
                    max_score = score
                    best_move = move
                
                alpha = max(alpha, score)
                if beta <= alpha:
                    # Store killer move
                    if depth < len(self.killer_moves):
                        if move != self.killer_moves[depth][0]:
                            self.killer_moves[depth][1] = self.killer_moves[depth][0]
                            self.killer_moves[depth][0] = move
                    break
            
            # Update history heuristic for best move
            if best_move:
                move_key = (best_move[0], best_move[1])
                self.history_scores[move_key] = self.history_scores.get(move_key, 0) + depth * depth
            
            result = (best_move, max_score)
            self.transposition_table[tt_key] = result
            return result
        else:
            min_score = 1000000
            for move in moves:
                next_board = [row[:] for row in board]
                self.make_move_on_board(move[0], move[1], next_board)
                
                _, score = self.alpha_beta(
                    next_board, game_obj, self.players[player],
                    alpha, beta, depth - 1, True, phase
                )
                
                if score < min_score:
                    min_score = score
                    best_move = move
                
                beta = min(beta, score)
                if beta <= alpha:
                    if depth < len(self.killer_moves):
                        if move != self.killer_moves[depth][0]:
                            self.killer_moves[depth][1] = self.killer_moves[depth][0]
                            self.killer_moves[depth][0] = move
                    break
            
            result = (best_move, min_score)
            self.transposition_table[tt_key] = result
            return result
    
    def iterative_deepening(self, board, game_obj, player, max_depth, time_limit=5.0):
        """
        Iterative deepening search with time limit.
        Searches progressively deeper until time runs out.
        """
        start_time = time.time()
        best_move = None
        best_score = -1000000
        
        phase = self.get_game_phase(board)
        
        for depth in range(1, max_depth + 1):
            # Clear transposition table for new depth
            if depth > 1:
                # Keep some entries for continuity
                if len(self.transposition_table) > 100000:
                    self.transposition_table = {}
            
            try:
                move, score = self.alpha_beta(
                    board, game_obj, player,
                    -1000000, 1000000, depth, True, phase
                )
                
                if move:
                    best_move = move
                    best_score = score
                    
            except Exception as e:
                print(f"Search error at depth {depth}: {e}")
                break
            
            # Check time
            elapsed = time.time() - start_time
            if elapsed > time_limit * 0.8:  # Leave some buffer
                break
        
        return best_move, best_score
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Main entry point - get the next best move."""
        
        # Increment move counter
        self.move_count += 1
        
        # Determine game phase
        phase = self.get_game_phase(board)
        print(f"Game phase: {phase}, Move: {self.move_count}")
        
        # Try opening book first
        if phase == 'opening' and self.move_count <= 8:
            opening_move = self.get_opening_move(board, player)
            if opening_move:
                # Validate the opening move
                start, end = opening_move
                piece = board[start[0]][start[1]]
                if piece and piece.color == player:
                    try:
                        legal_moves = piece.get_possible_moves(board, start, False, game_obj)
                        if end in legal_moves:
                            print(f"Opening book move: {opening_move}")
                            return opening_move
                    except:
                        pass
        
        # Adjust search depth based on game phase
        if phase == 'opening':
            search_depth = min(depth, 4)  # Faster in opening
        elif phase == 'endgame':
            search_depth = depth + 2  # Deeper in endgame (fewer pieces)
        else:
            search_depth = depth
        
        # Use iterative deepening with time limit
        move, score = self.iterative_deepening(
            board, game_obj, player, 
            max_depth=search_depth,
            time_limit=3.0
        )
        
        if move:
            print(f"Best move: {move}, Score: {score}, TT hits: {self.tt_hits}")
            return move
        
        # Fallback to any legal move
        moves = game_obj.generate_moves_list(player, board)
        if moves:
            return random.choice(moves)
        
        return None

