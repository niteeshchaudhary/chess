import helpers as hp

class MyAlgo:
    def __init__(self,name):
        if name=="RandomMove":
            self.hp = hp.RandomMove()
        elif name=="Greedy":
            self.hp = hp.Greedy()
        elif name=="MinMax":
            self.hp = hp.MinMax()
        elif name=="AlphaBeta":
            self.hp = hp.AlphaBeta()
        elif name=="MinMax_DP":
            self.hp = hp.MinMax_DP()
        elif name=="MinMax_DP_BinHash":
            self.hp = hp.MinMax_DP_BinHash()
        elif name=="AlphaBeta_DP_BinHash":
            self.hp = hp.AlphaBeta_DP_BinHash()
        elif name=="AlphaBeta_DP":
            self.hp = hp.AlphaBeta_DP()
        elif name=="MyBot":
            self.hp = hp.MyBot()
        elif name=="PhaseBasedEngine":
            self.hp = hp.PhaseBasedEngine()
        elif name=="QuiescenceEngine":
            self.hp = hp.QuiescenceEngine()
        elif name=="NeuralPatternEngine":
            self.hp = hp.NeuralPatternEngine()
        elif name=="MCTSEngine":
            self.hp = hp.MCTSEngine()
        elif name=="HybridMCTSEngine":
            self.hp = hp.HybridMCTSEngine()
        elif name=="RLEngine":
            self.hp = hp.RLEngine()
        elif name=="DeepRLEngine":
            self.hp = hp.DeepRLEngine()

    def get_object(self,name=""):
        if name != "":
            if name=="RandomMove":
                self.hp = hp.RandomMove()
            elif name=="Greedy":
                self.hp = hp.Greedy()
            elif name=="MinMax":
                self.hp = hp.MinMax()
            elif name=="AlphaBeta":
                self.hp = hp.AlphaBeta()
            elif name=="MinMax_DP":
                self.hp = hp.MinMax_DP()
            elif name=="MinMax_DP_BinHash":
                self.hp = hp.MinMax_DP_BinHash()
            elif name=="AlphaBeta_DP_BinHash":
                self.hp = hp.AlphaBeta_DP_BinHash()
            elif name=="AlphaBeta_DP":
                self.hp = hp.AlphaBeta_DP()
            elif name=="MyBot":
                self.hp = hp.MyBot()
            elif name=="PhaseBasedEngine":
                self.hp = hp.PhaseBasedEngine()
            elif name=="QuiescenceEngine":
                self.hp = hp.QuiescenceEngine()
            elif name=="NeuralPatternEngine":
                self.hp = hp.NeuralPatternEngine()
            elif name=="MCTSEngine":
                self.hp = hp.MCTSEngine()
            elif name=="HybridMCTSEngine":
                self.hp = hp.HybridMCTSEngine()
            elif name=="RLEngine":
                self.hp = hp.RLEngine()
            elif name=="DeepRLEngine":
                self.hp = hp.DeepRLEngine()

        return self.hp