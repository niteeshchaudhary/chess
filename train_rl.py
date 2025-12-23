#!/usr/bin/env python3
"""
Training script for the Reinforcement Learning chess engine.

This script allows you to train the RLEngine through self-play.
The learned weights are saved to helpers/rl_weights.json and will
be automatically loaded when you use RLEngine in your games.

Usage:
    python train_rl.py [--games N] [--resume]

Arguments:
    --games N    Number of games to train (default: 100)
    --resume     Resume training from saved weights (default: True)
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helpers.RLEngine import RLEngine
from helpers.utility import Utility


class TrainingGame:
    """Simplified game class for training."""
    
    def __init__(self):
        from tokens import Rook, Knight, Bishop, Queen, King, Pawn
        self.current_player = "white"
        self.is_check = False
        self.en_passant_target = None
        
    def setup_board(self):
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
    
    def find_king_position(self, color, board):
        from tokens import King
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None
    
    def is_king_under_attack(self, king_position, board):
        opponent_color = "black" if self.current_player == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == opponent_color:
                    possible_moves = piece.get_possible_moves_op(board, (row, col), self.is_check, game=self)
                    if king_position in possible_moves:
                        return True
        return False
    
    def make_move_on_board(self, start, end, board):
        piece = board[start[0]][start[1]]
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
    
    def generate_moves_list(self, player="", board=None):
        player = self.current_player if player == "" else player
        myboard = board if board else self.board
        moves = []
        for i in range(8):
            for j in range(8):
                if myboard[i][j] and myboard[i][j].color == player:
                    for mv in myboard[i][j].get_possible_moves(myboard, (i, j), self.is_check, self):
                        moves.append([(i, j), mv])
        return moves


def train_rl_engine(num_games=100, resume=True):
    """Train the RL engine through self-play."""
    print("=" * 60)
    print("Reinforcement Learning Chess Engine Training")
    print("=" * 60)
    
    # Create RL engine
    engine = RLEngine(load_weights=resume)
    
    print(f"\nStarting training with {num_games} self-play games...")
    print(f"Current games played: {engine.games_played}")
    print(f"Learning rate: {engine.learning_rate}")
    print(f"Exploration rate: {engine.epsilon}")
    print(f"Discount factor: {engine.discount_factor}")
    print()
    
    # Create game object for move generation
    game = TrainingGame()
    
    wins = {"white": 0, "black": 0, "draw": 0}
    
    for game_num in range(num_games):
        # Decay exploration
        engine.epsilon = 0.2 * (1 - game_num / num_games) + 0.05
        
        # Setup game
        board = game.setup_board()
        game.board = board
        current_player = "white"
        game.current_player = current_player
        engine.start_episode()
        
        move_count = 0
        max_moves = 150
        game_over = False
        result = "draw"
        
        while move_count < max_moves and not game_over:
            # Get legal moves
            game.current_player = current_player
            moves = game.generate_moves_list(current_player, board)
            
            if not moves:
                # Game over
                game_over = True
                # Check if checkmate or stalemate
                king_pos = game.find_king_position(current_player, board)
                if king_pos and game.is_king_under_attack(king_pos, board):
                    result = "black" if current_player == "white" else "white"
                else:
                    result = "draw"
                break
            
            # Select and make move
            action = engine.select_action(board, moves, current_player, training=True)
            
            if not action:
                break
            
            # Record state-action
            engine.record_state_action(board, action)
            
            # Make move
            engine.make_move_on_board(action[0], action[1], board)
            
            current_player = engine.players[current_player]
            move_count += 1
        
        # Calculate final reward
        if result == "white":
            final_reward = 1.0
            wins["white"] += 1
        elif result == "black":
            final_reward = -1.0
            wins["black"] += 1
        else:
            final_reward = 0.0
            wins["draw"] += 1
        
        # End episode and learn
        engine.end_episode(final_reward, "white")
        
        # Progress update
        if (game_num + 1) % 10 == 0:
            total = game_num + 1
            print(f"Game {total}/{num_games} | "
                  f"White: {wins['white']} ({100*wins['white']/total:.1f}%) | "
                  f"Black: {wins['black']} ({100*wins['black']/total:.1f}%) | "
                  f"Draw: {wins['draw']} ({100*wins['draw']/total:.1f}%) | "
                  f"TD Error: {engine.avg_td_error:.4f}")
    
    # Final save
    engine._save_weights()
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"Total games trained: {engine.games_played}")
    print(f"Total weight updates: {engine.total_updates}")
    print(f"Final TD error: {engine.avg_td_error:.4f}")
    print(f"\nResults from this session:")
    print(f"  White wins: {wins['white']} ({100*wins['white']/num_games:.1f}%)")
    print(f"  Black wins: {wins['black']} ({100*wins['black']/num_games:.1f}%)")
    print(f"  Draws: {wins['draw']} ({100*wins['draw']/num_games:.1f}%)")
    print(f"\nWeights saved to: {engine.weights_file}")
    print("You can now use RLEngine in your games!")


def main():
    parser = argparse.ArgumentParser(description="Train the RL Chess Engine")
    parser.add_argument("--games", type=int, default=100,
                        help="Number of games to train (default: 100)")
    parser.add_argument("--resume", action="store_true", default=True,
                        help="Resume from saved weights (default: True)")
    parser.add_argument("--fresh", action="store_true",
                        help="Start fresh training (ignore saved weights)")
    
    args = parser.parse_args()
    
    resume = not args.fresh
    train_rl_engine(num_games=args.games, resume=resume)


if __name__ == "__main__":
    main()

