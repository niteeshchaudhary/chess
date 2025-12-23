#!/usr/bin/env python3
"""
Chess Arena - Text-based bot vs bot matches.

Usage:
    python arena.py [white_bot] [black_bot]
    
Examples:
    python arena.py AlphaBeta_DP_BinHash MinMax
    python arena.py PhaseBasedEngine QuiescenceEngine
    python arena.py  # Interactive mode - prompts for bot selection

Available Bots:
    - RandomMove
    - Greedy
    - MinMax, MinMax_DP, MinMax_DP_BinHash
    - AlphaBeta, AlphaBeta_DP, AlphaBeta_DP_BinHash
    - PhaseBasedEngine
    - QuiescenceEngine
    - NeuralPatternEngine
    - MCTSEngine, HybridMCTSEngine
    - RLEngine, DeepRLEngine
    - MyBot

Features:
    - Prints board state every minute
    - 5 minute time limit (draw if exceeded)
    - Displays winner and final board state
"""

import sys
import time
import argparse
from tokens import Rook, Knight, Bishop, Queen, King, Pawn
from my_algo import MyAlgo


# Unicode chess pieces for display
PIECE_SYMBOLS = {
    ('king', 'white'): '♔', ('queen', 'white'): '♕', ('rook', 'white'): '♖',
    ('bishop', 'white'): '♗', ('knight', 'white'): '♘', ('pawn', 'white'): '♙',
    ('king', 'black'): '♚', ('queen', 'black'): '♛', ('rook', 'black'): '♜',
    ('bishop', 'black'): '♝', ('knight', 'black'): '♞', ('pawn', 'black'): '♟',
}

# Available bots
AVAILABLE_BOTS = [
    "RandomMove", "Greedy",
    "MinMax", "MinMax_DP", "MinMax_DP_BinHash",
    "AlphaBeta", "AlphaBeta_DP", "AlphaBeta_DP_BinHash",
    "PhaseBasedEngine", "QuiescenceEngine", "NeuralPatternEngine",
    "MCTSEngine", "HybridMCTSEngine",
    "RLEngine", "DeepRLEngine",
    "MyBot"
]


class ArenaGame:
    """Text-based chess game for bot matches."""
    
    def __init__(self):
        self.board = self.setup_board()
        self.current_player = "white"
        self.is_check = False
        self.en_passant_target = None
        self.move_history = []
        self.players_map = {"black": "white", "white": "black"}
        
    def setup_board(self):
        """Initialize the chess board."""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # White pieces (row 0 and 1)
        board[0] = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"),
                    King("white"), Bishop("white"), Knight("white"), Rook("white")]
        board[1] = [Pawn("white") for _ in range(8)]
        
        # Black pieces (row 6 and 7)
        board[7] = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"),
                    King("black"), Bishop("black"), Knight("black"), Rook("black")]
        board[6] = [Pawn("black") for _ in range(8)]
        
        return board
    
    def print_board(self, move_num=None, last_move=None):
        """Print the current board state."""
        print("\n" + "=" * 50)
        if move_num is not None:
            print(f"  Move #{move_num}")
        if last_move:
            print(f"  Last move: {self.format_move(last_move)}")
        print("=" * 50)
        print()
        print("     a   b   c   d   e   f   g   h")
        print("   ┌───┬───┬───┬───┬───┬───┬───┬───┐")
        
        for row in range(7, -1, -1):
            print(f" {row + 1} │", end="")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    symbol = PIECE_SYMBOLS.get((piece.name, piece.color), '?')
                else:
                    # Checkerboard pattern
                    symbol = '·' if (row + col) % 2 == 0 else ' '
                print(f" {symbol} │", end="")
            print(f" {row + 1}")
            
            if row > 0:
                print("   ├───┼───┼───┼───┼───┼───┼───┼───┤")
        
        print("   └───┴───┴───┴───┴───┴───┴───┴───┘")
        print("     a   b   c   d   e   f   g   h")
        print()
    
    def format_move(self, move):
        """Format a move for display."""
        if not move:
            return "None"
        start, end = move
        cols = 'abcdefgh'
        start_sq = f"{cols[start[1]]}{start[0] + 1}"
        end_sq = f"{cols[end[1]]}{end[0] + 1}"
        return f"{start_sq} → {end_sq}"
    
    def find_king_position(self, color, board=None):
        """Find the king's position for a given color."""
        if board is None:
            board = self.board
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None
    
    def is_king_under_attack(self, king_position, board=None):
        """Check if the king at given position is under attack."""
        if board is None:
            board = self.board
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
        """Make a move on the board."""
        piece = board[start[0]][start[1]]
        if piece:
            piece.has_moved = True
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
    
    def generate_moves_list(self, player="", board=None):
        """Generate all legal moves for a player."""
        if player == "":
            player = self.current_player
        if board is None:
            board = self.board
            
        moves = []
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece and piece.color == player:
                    piece_moves = piece.get_possible_moves(board, (i, j), self.is_check, self)
                    for mv in piece_moves:
                        moves.append([(i, j), mv])
        return moves
    
    def generate_moves_dict(self, player="", board=None):
        """Generate moves dictionary for compatibility."""
        if player == "":
            player = self.current_player
        if board is None:
            board = self.board
            
        moves = {}
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece and piece.color == player:
                    mv = piece.get_possible_moves(board, (i, j), self.is_check, self)
                    if mv:
                        moves[i * 10 + j] = mv
        return moves
    
    def is_checkmate(self, player):
        """Check if player is in checkmate."""
        king_pos = self.find_king_position(player)
        if not king_pos:
            return True
        
        # Check if king is under attack
        if not self.is_king_under_attack(king_pos):
            return False
        
        # Check if any move can get out of check
        moves = self.generate_moves_list(player)
        return len(moves) == 0
    
    def is_stalemate(self, player):
        """Check if player is in stalemate."""
        king_pos = self.find_king_position(player)
        if not king_pos:
            return False
        
        # If in check, not stalemate
        if self.is_king_under_attack(king_pos):
            return False
        
        # If no legal moves, stalemate
        moves = self.generate_moves_list(player)
        return len(moves) == 0
    
    def make_move(self, start, end):
        """Execute a move and update game state."""
        piece = self.board[start[0]][start[1]]
        captured = self.board[end[0]][end[1]]
        
        # Make the move
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None
        
        if piece:
            piece.has_moved = True
        
        # Handle pawn promotion
        if piece and piece.name == "pawn":
            if end[0] == 0 or end[0] == 7:
                self.board[end[0]][end[1]] = Queen(piece.color)
            
            # Handle en passant
            if self.en_passant_target == end:
                self.board[start[0]][end[1]] = None
            
            # Set en passant target for double pawn push
            if abs(end[0] - start[0]) == 2:
                self.en_passant_target = ((start[0] + end[0]) // 2, start[1])
            else:
                self.en_passant_target = None
        else:
            self.en_passant_target = None
        
        # Handle castling
        if piece and piece.name == "king":
            if end[1] - start[1] == 2:  # Kingside
                rook = self.board[start[0]][7]
                self.board[start[0]][5] = rook
                self.board[start[0]][7] = None
                if rook:
                    rook.has_moved = True
            elif start[1] - end[1] == 2:  # Queenside
                rook = self.board[start[0]][0]
                self.board[start[0]][3] = rook
                self.board[start[0]][0] = None
                if rook:
                    rook.has_moved = True
        
        # Record move
        self.move_history.append((start, end, piece, captured))
        
        # Switch player
        self.current_player = self.players_map[self.current_player]
        
        # Update check status
        king_pos = self.find_king_position(self.current_player)
        self.is_check = self.is_king_under_attack(king_pos) if king_pos else False
        
        return captured


def run_arena(white_bot_name, black_bot_name, time_limit=300, print_interval=60):
    """
    Run a match between two bots.
    
    Args:
        white_bot_name: Name of the bot playing white
        black_bot_name: Name of the bot playing black
        time_limit: Maximum game time in seconds (default: 300 = 5 minutes)
        print_interval: How often to print board state in seconds (default: 60)
    """
    print("\n" + "=" * 60)
    print("                    CHESS ARENA")
    print("=" * 60)
    print(f"\n  ⚪ White: {white_bot_name}")
    print(f"  ⚫ Black: {black_bot_name}")
    print(f"\n  Time limit: {time_limit // 60} minutes")
    print(f"  Board update interval: {print_interval} seconds")
    print("\n" + "=" * 60)
    
    # Initialize game
    game = ArenaGame()
    
    # Initialize bots
    try:
        white_bot = MyAlgo(white_bot_name).get_object()
        black_bot = MyAlgo(black_bot_name).get_object()
    except Exception as e:
        print(f"\n❌ Error initializing bots: {e}")
        print(f"   Available bots: {', '.join(AVAILABLE_BOTS)}")
        return
    
    bots = {"white": white_bot, "black": black_bot}
    bot_names = {"white": white_bot_name, "black": black_bot_name}
    
    # Game timing
    start_time = time.time()
    last_print_time = start_time
    move_count = 0
    
    # Print initial board
    print("\n📋 Initial Position:")
    game.print_board()
    
    result = None
    winner = None
    
    print("\n🎮 Game Started!\n")
    
    while True:
        current_time = time.time()
        elapsed = current_time - start_time
        
        # Check time limit
        if elapsed > time_limit:
            result = "TIME_LIMIT"
            break
        
        # Print board every interval
        if current_time - last_print_time >= print_interval:
            minutes = int(elapsed) // 60
            seconds = int(elapsed) % 60
            print(f"\n⏱️  Time elapsed: {minutes}m {seconds}s")
            print(f"📊 Moves played: {move_count}")
            print(f"🎯 Current turn: {game.current_player}")
            game.print_board(move_count)
            last_print_time = current_time
        
        # Get current bot
        current_bot = bots[game.current_player]
        current_bot_name = bot_names[game.current_player]
        
        # Check for checkmate/stalemate before move
        if game.is_checkmate(game.current_player):
            result = "CHECKMATE"
            winner = game.players_map[game.current_player]
            break
        
        if game.is_stalemate(game.current_player):
            result = "STALEMATE"
            break
        
        # Get legal moves
        legal_moves = game.generate_moves_list(game.current_player)
        
        if not legal_moves:
            if game.is_check:
                result = "CHECKMATE"
                winner = game.players_map[game.current_player]
            else:
                result = "STALEMATE"
            break
        
        # Get bot's move
        try:
            move_start = time.time()
            move = current_bot.getNextMove(game.board, game, game.current_player)
            move_time = time.time() - move_start
            
            if not move or len(move) != 2:
                print(f"\n❌ {current_bot_name} returned invalid move: {move}")
                result = "INVALID_MOVE"
                winner = game.players_map[game.current_player]
                break
            
            start, end = move[0], move[1]
            
            # Validate move
            valid = False
            for legal_move in legal_moves:
                if legal_move[0] == tuple(start) and legal_move[1] == tuple(end):
                    valid = True
                    break
                if list(legal_move[0]) == list(start) and list(legal_move[1]) == list(end):
                    valid = True
                    break
            
            if not valid:
                print(f"\n❌ {current_bot_name} made illegal move: {game.format_move((start, end))}")
                result = "ILLEGAL_MOVE"
                winner = game.players_map[game.current_player]
                break
            
            # Execute move
            move_count += 1
            captured = game.make_move(tuple(start), tuple(end))
            
            # Print move
            capture_str = " (capture!)" if captured else ""
            check_str = " +" if game.is_check else ""
            print(f"  {move_count:3d}. {current_bot_name}: {game.format_move((start, end))}{capture_str}{check_str} ({move_time:.2f}s)")
            
        except Exception as e:
            print(f"\n❌ {current_bot_name} crashed: {e}")
            result = "CRASH"
            winner = game.players_map[game.current_player]
            break
        
        # Check for 50-move rule (simplified - just 200 moves total)
        if move_count >= 200:
            result = "MOVE_LIMIT"
            break
    
    # Game over
    elapsed = time.time() - start_time
    minutes = int(elapsed) // 60
    seconds = int(elapsed) % 60
    
    print("\n" + "=" * 60)
    print("                    GAME OVER")
    print("=" * 60)
    
    # Print final board
    print("\n📋 Final Position:")
    game.print_board(move_count)
    
    # Print result
    print("\n📊 Game Statistics:")
    print(f"   Total moves: {move_count}")
    print(f"   Total time: {minutes}m {seconds}s")
    print()
    
    if result == "CHECKMATE":
        print(f"🏆 CHECKMATE! Winner: {bot_names[winner]} ({winner})")
    elif result == "STALEMATE":
        print("🤝 DRAW by stalemate!")
    elif result == "TIME_LIMIT":
        print(f"⏰ DRAW - Time limit ({time_limit // 60} minutes) exceeded!")
    elif result == "MOVE_LIMIT":
        print("🤝 DRAW - Move limit (200 moves) reached!")
    elif result == "INVALID_MOVE":
        print(f"❌ {bot_names[game.players_map[winner]]} made invalid move. Winner: {bot_names[winner]}")
    elif result == "ILLEGAL_MOVE":
        print(f"❌ {bot_names[game.players_map[winner]]} made illegal move. Winner: {bot_names[winner]}")
    elif result == "CRASH":
        print(f"💥 {bot_names[game.players_map[winner]]} crashed. Winner: {bot_names[winner]}")
    
    print("\n" + "=" * 60)
    
    return {
        "result": result,
        "winner": bot_names.get(winner) if winner else None,
        "winner_color": winner,
        "moves": move_count,
        "time": elapsed,
        "white": white_bot_name,
        "black": black_bot_name
    }


def select_bot(prompt, default=None):
    """Interactive bot selection."""
    print(f"\n{prompt}")
    print("-" * 40)
    for i, bot in enumerate(AVAILABLE_BOTS, 1):
        default_marker = " (default)" if bot == default else ""
        print(f"  {i:2d}. {bot}{default_marker}")
    print()
    
    while True:
        if default:
            choice = input(f"Enter number or name [{default}]: ").strip()
            if not choice:
                return default
        else:
            choice = input("Enter number or name: ").strip()
        
        # Try as number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(AVAILABLE_BOTS):
                return AVAILABLE_BOTS[idx]
        except ValueError:
            pass
        
        # Try as name
        if choice in AVAILABLE_BOTS:
            return choice
        
        # Try case-insensitive match
        for bot in AVAILABLE_BOTS:
            if bot.lower() == choice.lower():
                return bot
        
        print("❌ Invalid selection. Try again.")


def main():
    parser = argparse.ArgumentParser(
        description="Chess Arena - Bot vs Bot matches",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available bots:
  {', '.join(AVAILABLE_BOTS)}

Examples:
  python arena.py AlphaBeta_DP_BinHash MinMax
  python arena.py PhaseBasedEngine QuiescenceEngine --time 10
  python arena.py  # Interactive mode
"""
    )
    
    parser.add_argument("white_bot", nargs="?", help="Bot to play white")
    parser.add_argument("black_bot", nargs="?", help="Bot to play black")
    parser.add_argument("--time", "-t", type=int, default=5,
                        help="Time limit in minutes (default: 5)")
    parser.add_argument("--interval", "-i", type=int, default=60,
                        help="Board print interval in seconds (default: 60)")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List available bots and exit")
    
    args = parser.parse_args()
    
    if args.list:
        print("\nAvailable bots:")
        for bot in AVAILABLE_BOTS:
            print(f"  - {bot}")
        return
    
    # Interactive mode if no bots specified
    if not args.white_bot:
        print("\n" + "=" * 60)
        print("           CHESS ARENA - Bot Selection")
        print("=" * 60)
        
        white_bot = select_bot("Select WHITE player:", default="AlphaBeta_DP_BinHash")
        black_bot = select_bot("Select BLACK player:", default="MinMax")
    else:
        white_bot = args.white_bot
        black_bot = args.black_bot if args.black_bot else args.white_bot
    
    # Validate bot names
    for bot_name in [white_bot, black_bot]:
        if bot_name not in AVAILABLE_BOTS:
            print(f"\n❌ Unknown bot: {bot_name}")
            print(f"   Available bots: {', '.join(AVAILABLE_BOTS)}")
            return
    
    # Run the match
    result = run_arena(
        white_bot, 
        black_bot, 
        time_limit=args.time * 60,
        print_interval=args.interval
    )
    
    return result


if __name__ == "__main__":
    main()

