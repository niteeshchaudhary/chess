import helpers as hp

class MyAlgo:
    def __init__(self, name):
        self.hp = self._create_algo(name)

    def _create_algo(self, name):
        """Factory method to create algorithm instances."""
        algos = {
            # Basic algorithms
            "RandomMove": hp.RandomMove,
            "Greedy": hp.Greedy,
            
            # MinMax family
            "MinMax": hp.MinMax,
            "MinMax_DP": hp.MinMax_DP,
            "MinMax_DP_BinHash": hp.MinMax_DP_BinHash,
            
            # Alpha-Beta family
            "AlphaBeta": hp.AlphaBeta,
            "AlphaBeta_DP": hp.AlphaBeta_DP,
            "AlphaBeta_DP_BinHash": hp.AlphaBeta_DP_BinHash,
            
            # Advanced engines
            "MyBot": hp.MyBot,
            "PhaseBasedEngine": hp.PhaseBasedEngine,
            "QuiescenceEngine": hp.QuiescenceEngine,
            "NeuralPatternEngine": hp.NeuralPatternEngine,
            "MCTSEngine": hp.MCTSEngine,
            "HybridMCTSEngine": hp.HybridMCTSEngine,
            
            # Reinforcement Learning engines
            "RLEngine": hp.RLEngine,
            "DeepRLEngine": hp.DeepRLEngine,
        }
        if name in algos:
            return algos[name]()
        return hp.RandomMove()  # Default fallback

    def get_object(self, name=""):
        if name != "":
            self.hp = self._create_algo(name)
        return self.hp