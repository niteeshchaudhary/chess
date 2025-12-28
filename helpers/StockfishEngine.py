"""
StockfishEngine - Wrapper for Stockfish chess engine.

This engine uses the Stockfish UCI engine via python-chess library.
Stockfish is one of the strongest open-source chess engines available.

Requirements:
    pip install python-chess stockfish

Note: Stockfish binary must be installed on the system.
On Linux: sudo apt-get install stockfish
On macOS: brew install stockfish
On Windows: Download from https://stockfishchess.org/download/
"""

import chess
import chess.engine
import os
import subprocess
import sys

# Try to import PhaseBasedEngine for fallback
try:
    from .PhaseBasedEngine import PhaseBasedEngine
    PHASE_BASED_AVAILABLE = True
except ImportError:
    PHASE_BASED_AVAILABLE = False

class StockfishEngine:
    
    def __init__(self):
        self.name = "StockfishEngine"
        self.players = {"black": "white", "white": "black"}
        self.engine = None
        self.stockfish_path = self._find_stockfish()
        self.crash_count = 0  # Track crashes to restart engine
        self.max_crashes_before_restart = 1  # Restart after each crash
        
        # Initialize fallback engine
        self.fallback_engine = None
        if PHASE_BASED_AVAILABLE:
            try:
                self.fallback_engine = PhaseBasedEngine()
                print("[Stockfish] Fallback engine (PhaseBasedEngine) initialized")
            except Exception as e:
                print(f"[WARNING] Failed to initialize fallback engine: {e}")
        
        if not self.stockfish_path:
            print("[WARNING] Stockfish not found. Please install Stockfish:")
            print("  Linux: sudo apt-get install stockfish")
            print("  macOS: brew install stockfish")
            print("  Windows: Download from https://stockfishchess.org/download/")
            print("  Or set STOCKFISH_PATH environment variable")
    
    def _find_stockfish(self):
        """Find Stockfish executable path."""
        # Check environment variable first
        if os.environ.get('STOCKFISH_PATH'):
            path = os.environ.get('STOCKFISH_PATH')
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path
        
        # Common installation paths
        common_paths = [
            '/usr/bin/stockfish',
            '/usr/local/bin/stockfish',
            '/opt/homebrew/bin/stockfish',  # macOS Apple Silicon
            'stockfish',  # In PATH
        ]
        
        for path in common_paths:
            if path == 'stockfish':
                # Check if it's in PATH
                try:
                    result = subprocess.run(['which', 'stockfish'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        return result.stdout.strip()
                except:
                    pass
            else:
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    return path
        
        return None
    
    def _board_to_fen(self, board, player):
        """
        Convert the game board representation to FEN notation.
        
        Board layout in this game:
        - Row 0: Black back rank (rank 8 in FEN)
        - Row 1: Black pawns (rank 7 in FEN)
        - Row 6: White pawns (rank 2 in FEN)
        - Row 7: White back rank (rank 1 in FEN)
        
        FEN notation goes from rank 8 (top) to rank 1 (bottom).
        """
        fen_rows = []
        
        # Convert board array to FEN format
        # FEN format: rank8/rank7/.../rank1 (rank 8 = top, rank 1 = bottom)
        # Board mapping: row 0 = rank 8 (black's back rank), row 7 = rank 1 (white's back rank)
        # Files: col 0 = file a, col 7 = file h (direct mapping)
        for row in range(8):  # Iterate from row 0 (rank 8) to row 7 (rank 1)
            fen_row = ""
            empty_count = 0
            
            for col in range(8):  # Files map directly: col 0 = a, col 7 = h
                piece = board[row][col]
                
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    
                    # Map piece types to FEN notation
                    piece_map = {
                        'Pawn': 'p', 'Knight': 'n', 'Bishop': 'b',
                        'Rook': 'r', 'Queen': 'q', 'King': 'k'
                    }
                    
                    piece_char = piece_map.get(piece.__class__.__name__, '')
                    if piece.color == 'white':
                        piece_char = piece_char.upper()
                    
                    fen_row += piece_char
            
            if empty_count > 0:
                fen_row += str(empty_count)
            
            fen_rows.append(fen_row)
        
        # Join rows: fen_rows[0] = row 0 (rank 8), fen_rows[7] = row 7 (rank 1)
        # FEN format: rank8/rank7/.../rank1
        fen_board = '/'.join(fen_rows)
        
        # Active color (player to move)
        active_color = 'w' if player == 'white' else 'b'
        
        # Castling rights (simplified - assume no castling for now)
        castling = '-'
        
        # En passant (simplified)
        en_passant = '-'
        
        # Halfmove clock and fullmove number (simplified)
        halfmove = '0'
        fullmove = '1'
        
        fen = f"{fen_board} {active_color} {castling} {en_passant} {halfmove} {fullmove}"
        return fen
    
    def _uci_to_coords(self, uci_move):
        """
        Convert UCI move (e.g., 'e2e4') to coordinate tuple ((row, col), (row, col)).
        
        Stockfish uses standard chess notation (rank 1-8, file a-h).
        Our board uses (row 0-7, col 0-7) where:
        - Row 0 = top (black's starting rank)
        - Row 7 = bottom (white's starting rank)
        
        Conversion: (7 - stockfish_rank_index, 7 - stockfish_file_index)
        """
        if len(uci_move) < 4:
            return None
        
        # UCI format: e2e4 (from square to square)
        from_square = uci_move[0:2]
        to_square = uci_move[2:4]
        
        # Convert file (a-h) and rank (1-8) to row (0-7) and col (0-7)
        def square_to_coords(square):
            file_char = square[0]  # a-h
            rank_char = square[1]   # 1-8
            
            # Coordinate mapping:
            # Files (a-h) → columns (0-7): a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7
            # Ranks (1-8) → rows (7-0): rank 1→row 7, rank 2→row 6, ..., rank 8→row 0
            stockfish_col = ord(file_char) - ord('a')  # 0-7 (a=0, h=7)
            stockfish_rank = int(rank_char) - 1  # 0-7 (rank 1=0, rank 8=7)
            
            # Convert rank to row: rank 1→row 7, rank 8→row 0
            # Formula: row = 7 - stockfish_rank
            row = 7 - stockfish_rank
            # Files map directly: a=0, b=1, ..., h=7
            col = stockfish_col
            
            return (row, col)
        
        from_coords = square_to_coords(from_square)
        to_coords = square_to_coords(to_square)
        
        return (from_coords, to_coords)
    
    def _is_engine_alive(self):
        """Check if the engine process is still alive."""
        if self.engine is None:
            return False
        
        try:
            # Try to ping the engine with a simple command
            # If the process is dead, this will raise an exception
            if hasattr(self.engine, 'ping'):
                self.engine.ping()
            # Check if the underlying process exists
            if hasattr(self.engine, 'proc') and self.engine.proc:
                # Check if process is still running
                if hasattr(self.engine.proc, 'poll'):
                    return_code = self.engine.proc.poll()
                    if return_code is not None:
                        # Process has terminated
                        return False
            return True
        except (chess.engine.EngineTerminatedError, 
                chess.engine.EngineError,
                BrokenPipeError,
                OSError,
                AttributeError):
            return False
    
    def _reset_engine(self):
        """Reset the engine connection by closing and clearing it."""
        if self.engine is not None:
            try:
                # Try to quit gracefully
                if self._is_engine_alive():
                    self.engine.quit()
            except:
                # If quit fails, try to kill the process
                try:
                    if hasattr(self.engine, 'proc') and self.engine.proc:
                        self.engine.proc.kill()
                except:
                    pass
            finally:
                self.engine = None
    
    def _get_engine(self):
        """Get or create Stockfish engine connection optimized for fast 2-second responses."""
        # Check if existing engine is still alive
        if self.engine is not None:
            if not self._is_engine_alive():
                print("[WARNING] Engine process is dead, resetting...")
                self._reset_engine()
                self.crash_count += 1
        
        # Create new engine if needed
        if self.engine is None and self.stockfish_path:
            try:
                print("[Stockfish] Starting new engine process...")
                self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
                
                # Small delay to ensure engine is ready
                import time
                time.sleep(0.2)  # Increased delay for stability
                
                # Verify engine is responsive
                try:
                    self.engine.ping()
                except:
                    print("[WARNING] Engine ping failed, but continuing...")
                
                # Configure for STABLE play - reduced resources to prevent crashes
                import multiprocessing
                cpu_count = multiprocessing.cpu_count()
                # Limit threads to prevent crashes (max 2 threads for stability)
                num_threads = min(2, max(1, cpu_count // 4))
                
                # Reduced hash to prevent memory issues
                hash_mb = 64  # Further reduced for stability
                
                # Configure with error handling
                try:
                    # Use minimal configuration to avoid crashes
                    config = {
                        "Threads": num_threads,
                        "Hash": hash_mb,
                    }
                    # Only add Skill Level if supported (some versions don't support it)
                    try:
                        config["Skill Level"] = 20
                    except:
                        pass
                    
                    self.engine.configure(config)
                    print(f"[Stockfish] Configured for STABLE play (2s response):")
                    print(f"  - Threads: {num_threads} (limited for stability)")
                    print(f"  - Hash: {hash_mb} MB (reduced for stability)")
                except Exception as config_error:
                    print(f"[WARNING] Configuration error (using defaults): {config_error}")
                    # Engine might still work with defaults
                    
            except Exception as e:
                print(f"[ERROR] Failed to start Stockfish: {e}")
                self.engine = None
                self.crash_count += 1
                return None
        
        return self.engine
    
    def _use_fallback(self, board, game_obj, player, depth, reason=""):
        """Use PhaseBasedEngine as fallback when Stockfish fails."""
        if self.fallback_engine:
            print(f"[Stockfish] Using fallback engine (PhaseBasedEngine){': ' + reason if reason else ''}")
            try:
                return self.fallback_engine.getNextMove(board, game_obj, player, depth)
            except Exception as e:
                print(f"[ERROR] Fallback engine also failed: {e}")
        
        # Ultimate fallback to random move
        print("[WARNING] All engines failed, using random move")
        moves = game_obj.generate_moves_list(player, board)
        if moves:
            import random
            return random.choice(moves)
        return None
    
    def getNextMove(self, board, game_obj, player="black", depth=4):
        """Get next move from Stockfish."""
        # If engine has crashed too many times, skip it entirely
        if self.crash_count >= 3:
            return self._use_fallback(board, game_obj, player, depth, "Stockfish disabled due to repeated crashes")
        
        engine = self._get_engine()
        
        if not engine:
            # Fallback to PhaseBasedEngine if Stockfish not available
            return self._use_fallback(board, game_obj, player, depth, "Stockfish not available")
        
        try:
            # Verify engine is alive before proceeding
            if not self._is_engine_alive():
                print("[WARNING] Engine is not alive, resetting...")
                self._reset_engine()
                engine = self._get_engine()
                if not engine:
                    return self._use_fallback(board, game_obj, player, depth, "Engine not available")
            
            # Convert board to FEN
            fen = self._board_to_fen(board, player)
            print(f"[Stockfish] Board FEN: {fen}")
            
            # Validate FEN before creating board
            try:
                chess_board = chess.Board(fen)
                
                # Check if there are legal moves
                if chess_board.is_game_over():
                    print(f"[WARNING] Game is over, no moves available")
                    return self._use_fallback(board, game_obj, player, depth, "Game is over")
                    
            except ValueError as ve:
                print(f"[ERROR] Invalid FEN: {fen}, error: {ve}")
                return self._use_fallback(board, game_obj, player, depth, f"Invalid FEN: {ve}")
            
            # Optimized for 2 second response time while maintaining efficiency
            # Reduced time limit slightly to prevent timeouts and crashes
            time_limit = 1.5  # 1.5 seconds per move for fast response and stability
            
            # Get best move from Stockfish with time limit only
            # Using only time limit to prevent crashes
            print(f"[Stockfish] Searching for best move (time limit: {time_limit}s)...")
            
            # Get best move from Stockfish with proper error handling
            # Use only time limit - depth limit can cause crashes
            result = None
            try:
                # Verify engine is still alive before playing
                if not self._is_engine_alive():
                    raise chess.engine.EngineTerminatedError("Engine process is dead")
                
                # Use only time limit to avoid crashes from depth limits
                result = engine.play(
                    chess_board, 
                    chess.engine.Limit(time=time_limit)
                )
            except (chess.engine.EngineTerminatedError, 
                    chess.engine.EngineError,
                    BrokenPipeError,
                    OSError,
                    subprocess.SubprocessError) as play_error:
                error_msg = str(play_error)
                print(f"[ERROR] Engine crashed during play: {play_error}")
                
                # Check for specific crash indicators
                is_crash = any(indicator in error_msg.lower() for indicator in [
                    "exit code", "process died", "unexpectedly", "segmentation",
                    "sigsegv", "engine process died", "-11"
                ])
                
                if is_crash:
                    print(f"[ERROR] Stockfish crash detected (exit code: -11 or similar)")
                
                # Reset engine and increment crash count
                self._reset_engine()
                self.crash_count += 1
                print(f"[Stockfish] Crash count: {self.crash_count}")
                
                # If engine keeps crashing, use fallback immediately
                if self.crash_count >= 3:
                    print("[WARNING] Stockfish crashed too many times, using fallback for rest of game")
                    return self._use_fallback(board, game_obj, player, depth, f"Engine crashed repeatedly: {play_error}")
                
                # Try to recover on next call by recreating engine
                return self._use_fallback(board, game_obj, player, depth, f"Engine crashed: {play_error}")
            
            if result and result.move:
                # Convert UCI move to coordinates
                uci_move = result.move.uci()
                move = self._uci_to_coords(uci_move)
                
                if move:
                    print(f"[Stockfish] Best move: {uci_move} -> {move}")
                    return move
            
            # Fallback if no move returned
            return self._use_fallback(board, game_obj, player, depth, "No move returned from Stockfish")
            
        except (chess.engine.EngineTerminatedError, 
                chess.engine.EngineError,
                BrokenPipeError,
                OSError,
                subprocess.SubprocessError) as e:
            error_msg = str(e)
            print(f"[ERROR] Stockfish engine process error: {e}")
            
            # Check for specific crash indicators
            is_crash = any(indicator in error_msg.lower() for indicator in [
                "exit code", "process died", "unexpectedly", "segmentation",
                "sigsegv", "engine process died", "-11"
            ])
            
            if is_crash:
                print(f"[ERROR] Stockfish crash detected: {error_msg}")
            
            # Reset engine if it's dead
            print("[WARNING] Stockfish engine connection died, resetting engine")
            self._reset_engine()
            self.crash_count += 1
            
            # Fallback to PhaseBasedEngine on any error
            if self.crash_count >= 3:
                return self._use_fallback(board, game_obj, player, depth, f"Engine crashed repeatedly: {error_msg}")
            return self._use_fallback(board, game_obj, player, depth, f"Error: {error_msg}")
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Stockfish unexpected error: {e}")
            import traceback
            traceback.print_exc()
            
            # Reset engine if it's dead (e.g., "engine event loop dead", "exit code")
            is_crash = any(keyword in error_msg.lower() for keyword in [
                "dead", "event loop", "exit code", "process died", 
                "unexpectedly", "segmentation", "sigsegv", "-11"
            ])
            
            if is_crash:
                print("[WARNING] Stockfish engine connection died, resetting engine")
                self._reset_engine()
                self.crash_count += 1
            
            # Fallback to PhaseBasedEngine on any error
            if self.crash_count >= 3:
                return self._use_fallback(board, game_obj, player, depth, f"Engine crashed repeatedly: {error_msg}")
            return self._use_fallback(board, game_obj, player, depth, f"Error: {error_msg}")
    
    def choose_piece(self, position):
        """Choose piece for promotion (always queen for Stockfish)."""
        return 'queen'
    
    def __del__(self):
        """Clean up engine connection."""
        self._reset_engine()

