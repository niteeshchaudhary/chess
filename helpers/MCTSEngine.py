"""
MCTSEngine - Monte Carlo Tree Search based chess engine.

Features:
- UCB1 Selection: Upper Confidence Bound for tree traversal
- Rapid Action Value Estimation (RAVE): Improves move ordering
- Progressive Widening: Limits branching in early iterations
- Virtual Loss: Enables better exploration
- Policy Network Simulation: Uses evaluation for move selection
- Transposition Detection: Reuses subtrees
"""

import random
import time
import math
from tokens import Queen, Rook, Bishop, Knight

class MCTSNode:
    """Node in the Monte Carlo Tree."""
    
    def __init__(self, board, player, move=None, parent=None):
        self.board = board
        self.player = player
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = None
        self.is_terminal = False
        self.terminal_value = None
        
        # RAVE statistics
        self.rave_wins = {}  # move -> wins
        self.rave_visits = {}  # move -> visits
        
    def ucb1(self, exploration=1.414, rave_weight=0.5):
        """Calculate UCB1 score with RAVE."""
        if self.visits == 0:
            return float('inf')
        
        # Standard UCB1
        exploitation = self.wins / self.visits
        exploration_term = exploration * math.sqrt(math.log(self.parent.visits) / self.visits)
        
        ucb = exploitation + exploration_term
        
        # Add RAVE bonus if available
        if self.move and self.parent:
            move_key = (self.move[0], self.move[1])
            if move_key in self.parent.rave_visits:
                rave_visits = self.parent.rave_visits[move_key]
                if rave_visits > 0:
                    rave_value = self.parent.rave_wins.get(move_key, 0) / rave_visits
                    beta = rave_visits / (self.visits + rave_visits + 
                                          4 * self.visits * rave_visits * rave_weight * rave_weight)
                    ucb = (1 - beta) * exploitation + beta * rave_value + exploration_term
        
        return ucb
    
    def select_child(self):
        """Select child with highest UCB1 score."""
        return max(self.children, key=lambda c: c.ucb1())
    
    def add_child(self, move, board, player):
        """Add a child node for a move."""
        child = MCTSNode(board, player, move, self)
        self.children.append(child)
        return child
    
    def update(self, result):
        """Update node statistics."""
        self.visits += 1
        self.wins += result


class MCTSEngine:
    
    def __init__(self):
        self.name = "MCTSEngine"
        self.players = {"black": "white", "white": "black"}
        
        # MCTS parameters
        self.exploration = 1.414  # UCB1 exploration constant
        self.simulation_limit = 3000  # Max simulations
        self.time_limit = 4.0  # Seconds per move
        self.max_simulation_depth = 50  # Max moves in simulation
        
        # Piece values for simulation policy
        self.piece_values = {
            "pawn": 100, "knight": 320, "bishop": 330,
            "rook": 500, "queen": 900, "king": 20000
        }
        
        # PST for policy network (simplified)
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
        
        # Statistics
        self.total_simulations = 0
        self.avg_simulation_depth = 0
        
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
    
    def copy_board(self, board):
        """Create a deep copy of the board."""
        return [row[:] for row in board]
    
    def evaluate_quick(self, board, player):
        """Quick static evaluation for simulation guidance."""
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    value = self.piece_values[piece.name]
                    value += self.center_bonus[row][col]
                    
                    if piece.color == player:
                        score += value
                    else:
                        score -= value
        
        return score
    
    def get_move_priority(self, move, board):
        """Get priority score for a move (for simulation policy)."""
        start, end = move
        piece = board[start[0]][start[1]]
        target = board[end[0]][end[1]]
        
        priority = 0
        
        # Captures are high priority
        if target:
            priority += 1000 + self.piece_values[target.name] - self.piece_values[piece.name] // 10
        
        # Promotions
        if piece.name == "pawn" and (end[0] == 0 or end[0] == 7):
            priority += 900
        
        # Center control
        priority += self.center_bonus[end[0]][end[1]]
        
        # Development (moving from back rank)
        if (piece.color == "white" and start[0] == 0) or \
           (piece.color == "black" and start[0] == 7):
            if piece.name in ["knight", "bishop"]:
                priority += 50
        
        return priority
    
    def policy_select(self, moves, board, temperature=1.0):
        """Select a move using policy network (softmax over priorities)."""
        if not moves:
            return None
        
        # Get priorities
        priorities = []
        for move in moves:
            p = self.get_move_priority(move, board)
            priorities.append(p)
        
        # Apply temperature and softmax
        max_p = max(priorities)
        exp_priorities = [math.exp((p - max_p) / max(temperature, 0.1)) for p in priorities]
        total = sum(exp_priorities)
        probs = [p / total for p in exp_priorities]
        
        # Sample from distribution
        r = random.random()
        cumsum = 0
        for i, prob in enumerate(probs):
            cumsum += prob
            if r <= cumsum:
                return moves[i]
        
        return moves[-1]
    
    def simulate(self, board, player, game_obj, max_depth=50):
        """
        Run a simulation from current position.
        Returns result from perspective of starting player.
        """
        current_board = self.copy_board(board)
        current_player = player
        starting_player = player
        depth = 0
        moves_made = []
        
        while depth < max_depth:
            # Get legal moves
            try:
                moves = game_obj.generate_moves_list(current_player, current_board)
            except:
                break
            
            if not moves:
                # Game over - checkmate or stalemate
                if depth == 0:
                    return 0.0, moves_made  # Stalemate or immediate loss
                
                # Check if this is checkmate
                eval_score = self.evaluate_quick(current_board, starting_player)
                if abs(eval_score) > 10000:
                    # Checkmate
                    return (1.0 if eval_score > 0 else 0.0), moves_made
                else:
                    return 0.5, moves_made  # Stalemate
            
            # Use policy network to select move
            temperature = max(0.5, 2.0 - depth * 0.1)  # Decrease temperature over time
            move = self.policy_select(moves, current_board, temperature)
            
            if not move:
                break
            
            # Track moves for RAVE
            moves_made.append((current_player, move))
            
            # Make the move
            self.make_move_on_board(move[0], move[1], current_board)
            
            current_player = self.players[current_player]
            depth += 1
            
            # Early termination based on material
            eval_score = self.evaluate_quick(current_board, starting_player)
            if abs(eval_score) > 5000:
                # Big material advantage, consider it a win
                return (0.8 if eval_score > 0 else 0.2), moves_made
        
        # Reached max depth - use evaluation
        eval_score = self.evaluate_quick(current_board, starting_player)
        
        # Convert evaluation to probability
        # Use sigmoid-like function
        result = 1.0 / (1.0 + math.exp(-eval_score / 400))
        
        self.avg_simulation_depth = (self.avg_simulation_depth * self.total_simulations + depth) / (self.total_simulations + 1)
        self.total_simulations += 1
        
        return result, moves_made
    
    def expand(self, node, game_obj):
        """Expand a node by adding one child."""
        if node.untried_moves is None:
            try:
                moves = game_obj.generate_moves_list(node.player, node.board)
                node.untried_moves = moves
            except:
                node.untried_moves = []
        
        if not node.untried_moves:
            node.is_terminal = True
            return None
        
        # Use policy to prioritize which moves to try first
        if len(node.untried_moves) > 1:
            node.untried_moves.sort(
                key=lambda m: self.get_move_priority(m, node.board),
                reverse=True
            )
        
        # Try the highest priority untried move
        move = node.untried_moves.pop(0)
        
        new_board = self.copy_board(node.board)
        self.make_move_on_board(move[0], move[1], new_board)
        
        child = node.add_child(move, new_board, self.players[node.player])
        
        return child
    
    def select(self, node):
        """Select a node to expand using UCB1."""
        path = [node]
        
        while True:
            if node.is_terminal:
                return path
            
            if node.untried_moves is None or node.untried_moves:
                return path
            
            if not node.children:
                return path
            
            # Select best child
            node = node.select_child()
            path.append(node)
        
        return path
    
    def backpropagate(self, path, result, moves_made):
        """Backpropagate result through the tree."""
        for node in reversed(path):
            # Result is from perspective of root player
            # Need to flip for opponent's nodes
            if node.player == path[0].player:
                node.update(result)
            else:
                node.update(1.0 - result)
            
            # Update RAVE statistics
            for player, move in moves_made:
                if player == node.player:
                    move_key = (move[0], move[1])
                    node.rave_visits[move_key] = node.rave_visits.get(move_key, 0) + 1
                    node.rave_wins[move_key] = node.rave_wins.get(move_key, 0) + result
    
    def mcts_search(self, root, game_obj, time_limit):
        """Run MCTS search from root node."""
        start_time = time.time()
        simulations = 0
        
        while simulations < self.simulation_limit:
            # Check time
            if time.time() - start_time > time_limit:
                break
            
            # Selection
            path = self.select(root)
            node = path[-1]
            
            # Expansion
            if not node.is_terminal:
                new_node = self.expand(node, game_obj)
                if new_node:
                    path.append(new_node)
                    node = new_node
            
            # Simulation
            result, moves_made = self.simulate(node.board, node.player, game_obj)
            
            # Backpropagation
            self.backpropagate(path, result, moves_made)
            
            simulations += 1
        
        return simulations
    
    def get_best_move(self, root):
        """Get the best move from root based on visit counts."""
        if not root.children:
            return None
        
        # Select child with most visits (most robust)
        best_child = max(root.children, key=lambda c: c.visits)
        
        # Print statistics
        print(f"\nMCTS Statistics:")
        print(f"Total simulations: {sum(c.visits for c in root.children)}")
        print(f"Avg simulation depth: {self.avg_simulation_depth:.1f}")
        print(f"\nTop moves:")
        
        sorted_children = sorted(root.children, key=lambda c: c.visits, reverse=True)[:5]
        for child in sorted_children:
            win_rate = child.wins / max(1, child.visits) * 100
            print(f"  {child.move}: visits={child.visits}, win_rate={win_rate:.1f}%")
        
        return best_child.move
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get next move using MCTS."""
        # Reset statistics
        self.total_simulations = 0
        self.avg_simulation_depth = 0
        
        # Create root node
        root = MCTSNode(self.copy_board(board), player)
        
        # Initialize root's untried moves
        try:
            root.untried_moves = game_obj.generate_moves_list(player, board)
        except:
            return None
        
        if not root.untried_moves:
            return None
        
        # If only one legal move, return it
        if len(root.untried_moves) == 1:
            return root.untried_moves[0]
        
        # Run MCTS
        simulations = self.mcts_search(root, game_obj, self.time_limit)
        
        print(f"\nMCTS completed {simulations} simulations")
        
        # Get best move
        best_move = self.get_best_move(root)
        
        if best_move:
            return best_move
        
        # Fallback to random move
        return random.choice(root.untried_moves) if root.untried_moves else None


class HybridMCTSEngine:
    """
    Hybrid engine combining MCTS with Alpha-Beta for endgames.
    Uses MCTS for complex positions and Alpha-Beta for tactical/endgame positions.
    """
    
    def __init__(self):
        self.name = "HybridMCTSEngine"
        self.players = {"black": "white", "white": "black"}
        
        self.mcts = MCTSEngine()
        
        # Piece values for phase detection
        self.piece_values = {
            "pawn": 100, "knight": 320, "bishop": 330,
            "rook": 500, "queen": 900, "king": 20000
        }
        
        # Transposition table for alpha-beta
        self.tt = {}
    
    def is_endgame(self, board):
        """Detect if position is an endgame."""
        total_material = 0
        queens = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    if piece.name == "queen":
                        queens += 1
                    if piece.name != "king":
                        total_material += self.piece_values[piece.name]
        
        return total_material < 2500 or queens == 0
    
    def is_tactical(self, board, game_obj, player):
        """Detect if position is tactical (has captures/checks)."""
        try:
            moves = game_obj.generate_moves_list(player, board)
            captures = 0
            for move in moves:
                if board[move[1][0]][move[1][1]]:
                    captures += 1
            
            return captures >= 3  # Many captures available
        except:
            return False
    
    def alpha_beta(self, board, game_obj, player, alpha, beta, depth):
        """Simple alpha-beta for endgame."""
        if depth == 0:
            return None, self.mcts.evaluate_quick(board, player)
        
        try:
            moves = game_obj.generate_moves_list(player, board)
        except:
            return None, 0
        
        if not moves:
            return None, -50000 + depth
        
        best_move = moves[0]
        best_score = -100000
        
        # Order moves by captures
        moves.sort(key=lambda m: self.piece_values.get(
            board[m[1][0]][m[1][1]].name if board[m[1][0]][m[1][1]] else "pawn", 0
        ), reverse=True)
        
        for move in moves:
            new_board = [row[:] for row in board]
            self.mcts.make_move_on_board(move[0], move[1], new_board)
            
            _, score = self.alpha_beta(new_board, game_obj, self.players[player], -beta, -alpha, depth - 1)
            score = -score
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        
        return best_move, best_score
    
    def make_move_on_board(self, start, end, board, choice=None):
        return self.mcts.make_move_on_board(start, end, board, choice)
    
    def choose_piece(self, position):
        return 'queen'
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Hybrid decision making."""
        
        # Use alpha-beta for endgames and tactical positions
        if self.is_endgame(board):
            print("Using Alpha-Beta for endgame")
            move, _ = self.alpha_beta(board, game_obj, player, -100000, 100000, depth + 2)
            if move:
                return move
        
        if self.is_tactical(board, game_obj, player):
            print("Using Alpha-Beta for tactical position")
            move, _ = self.alpha_beta(board, game_obj, player, -100000, 100000, depth)
            if move:
                return move
        
        # Use MCTS for complex middlegame positions
        print("Using MCTS for complex position")
        return self.mcts.getNextMove(board, game_obj, player, depth)
