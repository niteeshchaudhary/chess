"""
Shared list of available chess algorithms.
This ensures consistency across all files that need algorithm selection.
"""

# Available algorithms - ordered by strength (best first)
# ⭐ = Recommended for best play
ALGORITHMS = [
    "StockfishEngine",           # 🏆 WORLD CHAMPION: Stockfish engine (requires python-chess + Stockfish binary)
    "QuiescenceEngine",          # ⭐ Strongest: Advanced pruning, quiescence search, depth=5
    "PhaseBasedEngine",          # ⭐ Best Balance: Opening book, phase-adaptive, depth=4
    "NeuralPatternEngine",       # ⭐ Strong: Pattern recognition, depth=4
    "AlphaBeta_DP_BinHash",      # ⚡ Fastest Strong: Binary hashing, depth=6
    "HybridMCTSEngine",          # Strong: MCTS + Alpha-Beta hybrid
    "MCTSEngine",                # Different approach: Monte Carlo Tree Search
    "AlphaBeta_DP",              # Good: Alpha-Beta with DP, depth=4
    "MinMax_DP_BinHash",         # Good: MinMax with binary hashing, depth=4
    "AlphaBeta",                 # Basic: Alpha-Beta, depth=3
    "MinMax_DP",                 # Basic: MinMax with DP, depth=4
    "MinMax",                    # Basic: Simple MinMax, depth=3
    "MyBot",                     # Custom bot
    "Greedy",                    # Simple: Material-based
    "RandomMove",                # Random: For testing only
]




