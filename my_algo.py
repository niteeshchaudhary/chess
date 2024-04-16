import helpers as hp

class MyAlgo:
    def __init__(self,name):
        if name=="RandomMove":
            self.hp = hp.RandomMove()
        elif name=="MinMax":
            self.hp = hp.MinMax()
        elif name=="Greedy":
            self.hp = hp.Greedy()
        elif name=="AlphaBeta":
            self.hp = hp.AlphaBeta()
        elif name=="MinMax_DP":
            self.hp = hp.MinMax_DP()

    def get_object(self,name=""):
        if name != "":
            if name=="RandomMove":
                self.hp = hp.RandomMove()
            elif name=="MinMax":
                self.hp = hp.MinMax()
            elif name=="Greedy":
                self.hp = hp.Greedy()
            elif name=="AlphaBeta":
                self.hp = hp.AlphaBeta()
            elif name=="MinMax_DP":
                self.hp = hp.MinMax_DP()

        return self.hp