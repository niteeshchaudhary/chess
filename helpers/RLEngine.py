"""
RLEngine - Reinforcement Learning based chess engine.

Features:
- TD-Lambda Learning: Temporal difference learning with eligibility traces
- Feature Extraction: Hand-crafted features for board state representation
- Self-Play Training: Learns by playing against itself
- Experience Replay: Stores and replays past experiences for stable learning
- Policy Gradient: Softmax policy for move selection
- Value Network: Neural-inspired value function approximation
- Persistent Learning: Saves and loads learned weights
"""

import random
import math
import time
import os
import json
from tokens import Queen, Rook, Bishop, Knight

class RLEngine:
    
    def __init__(self, load_weights=True):
        self.name = "RLEngine"
        self.players = {"black": "white", "white": "black"}
        
        # Learning parameters
        self.learning_rate = 0.001  # Alpha - step size
        self.discount_factor = 0.99  # Gamma - future reward discount
        self.lambda_trace = 0.7  # Lambda for TD(λ)
        self.epsilon = 0.1  # Exploration rate
        self.temperature = 1.0  # Softmax temperature
        
        # Piece values for features
        self.piece_values = {
            "pawn": 1.0, "knight": 3.2, "bishop": 3.3,
            "rook": 5.0, "queen": 9.0, "king": 0.0
        }
        
        # Feature weights (learnable parameters)
        self.num_features = 100
        self.weights = self._init_weights()
        
        # Eligibility traces for TD(λ)
        self.eligibility_traces = [0.0] * self.num_features
        
        # Experience replay buffer
        self.experience_buffer = []
        self.buffer_size = 10000
        self.batch_size = 32
        
        # Training statistics
        self.games_played = 0
        self.total_updates = 0
        self.avg_td_error = 0.0
        
        # Weight file path
        self.weights_file = os.path.join(
            os.path.dirname(__file__), 
            "rl_weights.json"
        )
        
        # Load pre-trained weights if available
        if load_weights:
            self._load_weights()
        
        # Current episode data
        self.episode_states = []
        self.episode_actions = []
        self.episode_rewards = []
        
    def _init_weights(self):
        """Initialize weights with small random values."""
        weights = {}
        
        # Material features (12 features - 6 piece types x 2 colors)
        for i in range(12):
            weights[f'material_{i}'] = random.gauss(0, 0.1)
        
        # Piece-square features (64 features per piece type, simplified to 8)
        for piece in ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']:
            for zone in range(8):  # 8 board zones
                weights[f'pst_{piece}_{zone}'] = random.gauss(0, 0.1)
        
        # Pawn structure features
        for i in range(8):
            weights[f'pawn_structure_{i}'] = random.gauss(0, 0.1)
        
        # King safety features
        for i in range(6):
            weights[f'king_safety_{i}'] = random.gauss(0, 0.1)
        
        # Mobility features
        for i in range(4):
            weights[f'mobility_{i}'] = random.gauss(0, 0.1)
        
        # Control features
        for i in range(4):
            weights[f'control_{i}'] = random.gauss(0, 0.1)
        
        # Game phase feature
        weights['game_phase'] = random.gauss(0, 0.1)
        
        # Bias term
        weights['bias'] = 0.0
        
        return weights
    
    def _load_weights(self):
        """Load weights from file if exists."""
        try:
            if os.path.exists(self.weights_file):
                with open(self.weights_file, 'r') as f:
                    data = json.load(f)
                    self.weights = data.get('weights', self.weights)
                    self.games_played = data.get('games_played', 0)
                    self.total_updates = data.get('total_updates', 0)
                    print(f"RL: Loaded weights from {self.games_played} games")
        except Exception as e:
            print(f"RL: Could not load weights: {e}")
    
    def _save_weights(self):
        """Save weights to file."""
        try:
            data = {
                'weights': self.weights,
                'games_played': self.games_played,
                'total_updates': self.total_updates
            }
            with open(self.weights_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"RL: Could not save weights: {e}")
    
    def get_zone(self, row, col):
        """Get board zone for simplified PST."""
        # Divide board into 8 zones
        if row < 2:
            return 0 if col < 4 else 1
        elif row < 4:
            return 2 if col < 4 else 3
        elif row < 6:
            return 4 if col < 4 else 5
        else:
            return 6 if col < 4 else 7
    
    def extract_features(self, board, player):
        """Extract features from board position."""
        features = {}
        opponent = self.players[player]
        
        # Initialize feature counts
        piece_counts = {
            "white": {"pawn": 0, "knight": 0, "bishop": 0, "rook": 0, "queen": 0, "king": 0},
            "black": {"pawn": 0, "knight": 0, "bishop": 0, "rook": 0, "queen": 0, "king": 0}
        }
        
        pst_features = {}
        king_positions = {"white": None, "black": None}
        
        # Pawn structure tracking
        pawns_per_file = {"white": [0] * 8, "black": [0] * 8}
        
        # Mobility estimation (simplified)
        mobility = {"white": 0, "black": 0}
        
        # Center control
        center_control = {"white": 0, "black": 0}
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        extended_center = [(2, 2), (2, 3), (2, 4), (2, 5),
                          (3, 2), (3, 5), (4, 2), (4, 5),
                          (5, 2), (5, 3), (5, 4), (5, 5)]
        
        # Scan the board
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    color = piece.color
                    ptype = piece.name
                    
                    # Count pieces
                    piece_counts[color][ptype] += 1
                    
                    # PST features
                    zone = self.get_zone(row, col)
                    key = f'pst_{ptype}_{zone}'
                    if key not in pst_features:
                        pst_features[key] = 0
                    pst_features[key] += 1 if color == player else -1
                    
                    # Track king position
                    if ptype == "king":
                        king_positions[color] = (row, col)
                    
                    # Track pawns per file
                    if ptype == "pawn":
                        pawns_per_file[color][col] += 1
                    
                    # Estimate mobility (piece count based)
                    mobility_value = {"pawn": 1, "knight": 4, "bishop": 5,
                                     "rook": 7, "queen": 13, "king": 2}
                    mobility[color] += mobility_value.get(ptype, 0)
                    
                    # Center control
                    if (row, col) in center_squares:
                        center_control[color] += 2
                    elif (row, col) in extended_center:
                        center_control[color] += 1
        
        # Material features
        for i, (color, pieces) in enumerate(piece_counts.items()):
            for j, (ptype, count) in enumerate(pieces.items()):
                feat_idx = i * 6 + j
                features[f'material_{feat_idx}'] = count * self.piece_values[ptype]
        
        # PST features
        for key, value in pst_features.items():
            features[key] = value
        
        # Pawn structure features
        for i in range(8):
            # Doubled pawns penalty
            white_doubled = max(0, pawns_per_file["white"][i] - 1)
            black_doubled = max(0, pawns_per_file["black"][i] - 1)
            
            if player == "white":
                features[f'pawn_structure_{i}'] = black_doubled - white_doubled
            else:
                features[f'pawn_structure_{i}'] = white_doubled - black_doubled
        
        # King safety features
        for color in ["white", "black"]:
            if king_positions[color]:
                kr, kc = king_positions[color]
                
                # Pawn shield
                pawn_shield = 0
                direction = 1 if color == "white" else -1
                for dc in [-1, 0, 1]:
                    nc = kc + dc
                    nr = kr + direction
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        p = board[nr][nc]
                        if p and p.name == "pawn" and p.color == color:
                            pawn_shield += 1
                
                # King exposure (distance from corner)
                exposure = abs(kc - 3.5) + abs(kr - 3.5)
                
                idx = 0 if color == player else 3
                features[f'king_safety_{idx}'] = pawn_shield
                features[f'king_safety_{idx + 1}'] = exposure / 10.0
                features[f'king_safety_{idx + 2}'] = 1 if kc in [2, 6] else 0  # Castled
        
        # Mobility features
        features['mobility_0'] = mobility[player] / 50.0
        features['mobility_1'] = mobility[opponent] / 50.0
        features['mobility_2'] = (mobility[player] - mobility[opponent]) / 50.0
        features['mobility_3'] = 1.0 if mobility[player] > mobility[opponent] else 0.0
        
        # Control features
        features['control_0'] = center_control[player] / 10.0
        features['control_1'] = center_control[opponent] / 10.0
        features['control_2'] = (center_control[player] - center_control[opponent]) / 10.0
        features['control_3'] = 1.0 if center_control[player] > center_control[opponent] else 0.0
        
        # Game phase (0 = endgame, 1 = opening)
        total_pieces = sum(sum(pieces.values()) for pieces in piece_counts.values())
        features['game_phase'] = total_pieces / 32.0
        
        # Bias
        features['bias'] = 1.0
        
        return features
    
    def evaluate(self, board, player):
        """Evaluate position using learned weights."""
        features = self.extract_features(board, player)
        
        value = 0.0
        for key, feat_value in features.items():
            if key in self.weights:
                value += self.weights[key] * feat_value
        
        # Squash to [-1, 1] using tanh
        return math.tanh(value)
    
    def get_action_values(self, board, moves, player):
        """Get Q-values for all actions using one-step lookahead."""
        action_values = []
        
        for move in moves:
            # Make move on copy
            next_board = [row[:] for row in board]
            self.make_move_on_board(move[0], move[1], next_board)
            
            # Evaluate resulting position (from opponent's view, negated)
            value = -self.evaluate(next_board, self.players[player])
            
            # Add small bonus for captures
            target = board[move[1][0]][move[1][1]]
            if target:
                value += 0.1 * self.piece_values[target.name]
            
            action_values.append(value)
        
        return action_values
    
    def select_action(self, board, moves, player, training=False):
        """Select action using softmax policy with exploration."""
        if not moves:
            return None
        
        action_values = self.get_action_values(board, moves, player)
        
        # Epsilon-greedy exploration during training
        if training and random.random() < self.epsilon:
            return random.choice(moves)
        
        # Softmax selection
        max_val = max(action_values)
        exp_values = [math.exp((v - max_val) / self.temperature) for v in action_values]
        total = sum(exp_values)
        probs = [v / total for v in exp_values]
        
        # Sample from distribution
        r = random.random()
        cumsum = 0
        for i, prob in enumerate(probs):
            cumsum += prob
            if r <= cumsum:
                return moves[i]
        
        return moves[-1]
    
    def td_update(self, state, next_state, reward, done, player):
        """
        Perform TD(λ) update.
        
        TD Error: δ = r + γ * V(s') - V(s)
        Update: w += α * δ * e (eligibility trace)
        """
        # Get current value
        current_value = self.evaluate(state, player)
        
        # Get next value (0 if terminal)
        if done:
            next_value = reward
        else:
            next_value = self.evaluate(next_state, player)
        
        # TD error
        td_error = reward + self.discount_factor * next_value - current_value
        
        # Get features for current state
        features = self.extract_features(state, player)
        
        # Update eligibility traces and weights
        for key in self.weights:
            feat_value = features.get(key, 0.0)
            
            # Update eligibility trace
            if key not in self.__dict__.get('traces', {}):
                if not hasattr(self, 'traces'):
                    self.traces = {}
                self.traces[key] = 0.0
            
            self.traces[key] = self.discount_factor * self.lambda_trace * self.traces.get(key, 0) + feat_value
            
            # Update weight
            gradient = self.learning_rate * td_error * self.traces[key]
            
            # Gradient clipping
            gradient = max(-0.1, min(0.1, gradient))
            
            self.weights[key] += gradient
        
        self.total_updates += 1
        self.avg_td_error = 0.99 * self.avg_td_error + 0.01 * abs(td_error)
        
        return td_error
    
    def store_experience(self, state, action, reward, next_state, done):
        """Store experience in replay buffer."""
        experience = {
            'state': [row[:] for row in state],
            'action': action,
            'reward': reward,
            'next_state': [row[:] for row in next_state] if next_state else None,
            'done': done
        }
        
        self.experience_buffer.append(experience)
        
        # Remove old experiences if buffer is full
        if len(self.experience_buffer) > self.buffer_size:
            self.experience_buffer.pop(0)
    
    def replay_experiences(self, player):
        """Learn from stored experiences (experience replay)."""
        if len(self.experience_buffer) < self.batch_size:
            return
        
        # Sample random batch
        batch = random.sample(self.experience_buffer, self.batch_size)
        
        # Reset traces for batch learning
        self.traces = {}
        
        for exp in batch:
            self.td_update(
                exp['state'],
                exp['next_state'],
                exp['reward'],
                exp['done'],
                player
            )
    
    def start_episode(self):
        """Start a new episode (game)."""
        self.episode_states = []
        self.episode_actions = []
        self.episode_rewards = []
        self.traces = {}  # Reset eligibility traces
    
    def end_episode(self, final_reward, player):
        """End episode and perform final updates."""
        self.games_played += 1
        
        # Assign credit to all moves in the episode
        for i, (state, action) in enumerate(zip(self.episode_states, self.episode_actions)):
            # Discounted reward
            steps_to_end = len(self.episode_states) - i - 1
            discounted_reward = final_reward * (self.discount_factor ** steps_to_end)
            
            # Store experience
            next_state = self.episode_states[i + 1] if i + 1 < len(self.episode_states) else None
            self.store_experience(state, action, discounted_reward, next_state, i == len(self.episode_states) - 1)
        
        # Replay past experiences
        self.replay_experiences(player)
        
        # Save weights periodically
        if self.games_played % 10 == 0:
            self._save_weights()
            print(f"RL: Saved after {self.games_played} games, avg TD error: {self.avg_td_error:.4f}")
    
    def record_state_action(self, state, action):
        """Record state-action pair during episode."""
        self.episode_states.append([row[:] for row in state])
        self.episode_actions.append(action)
    
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
    
    def train_self_play(self, game_obj, num_games=100):
        """
        Train the engine through self-play.
        Call this method to improve the engine.
        """
        print(f"RL: Starting self-play training for {num_games} games...")
        
        original_epsilon = self.epsilon
        
        for game_num in range(num_games):
            # Decay exploration over time
            self.epsilon = original_epsilon * (1 - game_num / num_games)
            
            # Setup new game
            board = self._setup_initial_board()
            current_player = "white"
            self.start_episode()
            
            move_count = 0
            max_moves = 200
            
            while move_count < max_moves:
                # Get legal moves
                try:
                    moves = game_obj.generate_moves_list(current_player, board)
                except:
                    break
                
                if not moves:
                    # Game over
                    if self._is_in_check(board, current_player, game_obj):
                        # Checkmate
                        reward = -1.0 if current_player == "white" else 1.0
                    else:
                        # Stalemate
                        reward = 0.0
                    break
                
                # Select and make move
                action = self.select_action(board, moves, current_player, training=True)
                
                if not action:
                    break
                
                # Record state-action
                self.record_state_action(board, action)
                
                # Make move
                self.make_move_on_board(action[0], action[1], board)
                
                current_player = self.players[current_player]
                move_count += 1
            
            # End of game
            final_reward = self._evaluate_final_position(board)
            self.end_episode(final_reward, "white")
            
            if (game_num + 1) % 10 == 0:
                print(f"RL: Completed {game_num + 1}/{num_games} training games")
        
        self.epsilon = original_epsilon
        self._save_weights()
        print(f"RL: Training complete! Total games played: {self.games_played}")
    
    def _setup_initial_board(self):
        """Setup initial chess position."""
        from tokens import Rook, Knight, Bishop, Queen, King, Pawn
        
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # White pieces
        board[0] = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"),
                    King("white"), Bishop("white"), Knight("white"), Rook("white")]
        board[1] = [Pawn("white") for _ in range(8)]
        
        # Black pieces
        board[7] = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"),
                    King("black"), Bishop("black"), Knight("black"), Rook("black")]
        board[6] = [Pawn("black") for _ in range(8)]
        
        return board
    
    def _is_in_check(self, board, player, game_obj):
        """Check if player is in check (simplified)."""
        # Find king
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.name == "king" and piece.color == player:
                    # Check if any opponent piece can attack king
                    opponent = self.players[player]
                    for r in range(8):
                        for c in range(8):
                            p = board[r][c]
                            if p and p.color == opponent:
                                # Simplified attack check
                                if piece.name in ["queen", "rook", "bishop"]:
                                    return True  # Might be in check
        return False
    
    def _evaluate_final_position(self, board):
        """Evaluate final position for training reward."""
        white_material = 0
        black_material = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    value = self.piece_values[piece.name]
                    if piece.color == "white":
                        white_material += value
                    else:
                        black_material += value
        
        # Normalize to [-1, 1]
        diff = white_material - black_material
        return math.tanh(diff / 10.0)
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get next move using learned policy."""
        try:
            moves = game_obj.generate_moves_list(player, board)
        except:
            return None
        
        if not moves:
            return None
        
        # Use policy with low temperature for exploitation
        old_temp = self.temperature
        self.temperature = 0.5  # Lower temperature = more exploitation
        
        action = self.select_action(board, moves, player, training=False)
        
        self.temperature = old_temp
        
        if action:
            value = self.evaluate(board, player)
            print(f"RL move: {action}, Position value: {value:.3f}, Games trained: {self.games_played}")
            return action
        
        return random.choice(moves) if moves else None


class DeepRLEngine:
    """
    Deep Reinforcement Learning engine using a simple neural network.
    Uses policy gradients (REINFORCE) with baseline.
    """
    
    def __init__(self):
        self.name = "DeepRLEngine"
        self.players = {"black": "white", "white": "black"}
        
        # Network architecture: input -> hidden -> output
        self.input_size = 768  # 64 squares x 12 piece types
        self.hidden_size = 256
        self.output_size = 1  # Value estimate
        
        # Initialize weights
        self.W1 = self._init_layer(self.input_size, self.hidden_size)
        self.b1 = [0.0] * self.hidden_size
        self.W2 = self._init_layer(self.hidden_size, self.output_size)
        self.b2 = [0.0]
        
        # Learning parameters
        self.learning_rate = 0.0001
        self.discount_factor = 0.99
        
        # Episode data
        self.episode_states = []
        self.episode_rewards = []
        self.episode_log_probs = []
        
        # Baseline (average return)
        self.baseline = 0.0
        self.baseline_alpha = 0.01
        
        # Piece encoding
        self.piece_encoding = {
            ("pawn", "white"): 0, ("knight", "white"): 1, ("bishop", "white"): 2,
            ("rook", "white"): 3, ("queen", "white"): 4, ("king", "white"): 5,
            ("pawn", "black"): 6, ("knight", "black"): 7, ("bishop", "black"): 8,
            ("rook", "black"): 9, ("queen", "black"): 10, ("king", "black"): 11
        }
        
        self.piece_values = {
            "pawn": 100, "knight": 320, "bishop": 330,
            "rook": 500, "queen": 900, "king": 20000
        }
    
    def _init_layer(self, input_dim, output_dim):
        """Initialize layer with Xavier initialization."""
        scale = math.sqrt(2.0 / (input_dim + output_dim))
        return [[random.gauss(0, scale) for _ in range(output_dim)] 
                for _ in range(input_dim)]
    
    def encode_board(self, board, player):
        """Encode board as feature vector."""
        features = [0.0] * self.input_size
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    square_idx = row * 8 + col
                    piece_idx = self.piece_encoding.get((piece.name, piece.color), 0)
                    feature_idx = square_idx * 12 + piece_idx
                    features[feature_idx] = 1.0 if piece.color == player else -1.0
        
        return features
    
    def relu(self, x):
        """ReLU activation."""
        return max(0, x)
    
    def forward(self, features):
        """Forward pass through network."""
        # Hidden layer
        hidden = []
        for j in range(self.hidden_size):
            val = self.b1[j]
            for i in range(self.input_size):
                val += features[i] * self.W1[i][j]
            hidden.append(self.relu(val))
        
        # Output layer
        output = self.b2[0]
        for j in range(self.hidden_size):
            output += hidden[j] * self.W2[j][0]
        
        # Tanh activation for value in [-1, 1]
        return math.tanh(output), hidden
    
    def evaluate(self, board, player):
        """Evaluate position."""
        features = self.encode_board(board, player)
        value, _ = self.forward(features)
        return value
    
    def select_action(self, board, moves, player):
        """Select action using policy."""
        if not moves:
            return None, 0
        
        action_values = []
        for move in moves:
            next_board = [row[:] for row in board]
            self.make_move_on_board(move[0], move[1], next_board)
            value = -self.evaluate(next_board, self.players[player])
            
            # Add capture bonus
            target = board[move[1][0]][move[1][1]]
            if target:
                value += 0.1 * self.piece_values[target.name] / 1000
            
            action_values.append(value)
        
        # Softmax
        max_val = max(action_values)
        exp_vals = [math.exp(v - max_val) for v in action_values]
        total = sum(exp_vals)
        probs = [v / total for v in exp_vals]
        
        # Sample
        r = random.random()
        cumsum = 0
        for i, prob in enumerate(probs):
            cumsum += prob
            if r <= cumsum:
                return moves[i], math.log(prob + 1e-10)
        
        return moves[-1], math.log(probs[-1] + 1e-10)
    
    def make_move_on_board(self, start, end, board, choice=None):
        piece = board[start[0]][start[1]]
        if piece:
            piece.has_moved = True
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
        
        if piece and piece.name == "pawn" and (end[0] == 0 or end[0] == 7):
            board[end[0]][end[1]] = Queen(piece.color)
    
    def choose_piece(self, position):
        return 'queen'
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get next move."""
        try:
            moves = game_obj.generate_moves_list(player, board)
        except:
            return None
        
        if not moves:
            return None
        
        action, _ = self.select_action(board, moves, player)
        
        if action:
            value = self.evaluate(board, player)
            print(f"DeepRL move: {action}, Value: {value:.3f}")
            return action
        
        return random.choice(moves)
