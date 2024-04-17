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

        return self.hp