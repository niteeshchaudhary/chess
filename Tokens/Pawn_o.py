from .Tokens import Tokens


class Pawn(Tokens):

    def __init__(self, x, y, color):
        super().__init__(x, y, color,"pawn")
        self.ix = x
        self.iy = y
        self.moved = 0
        self.icon = "♙" if color == "white" else "♟"

    def possibPositions(self, board):
        positions = []
        rng = [1]
        ob1 = 0
        if self.iy == self.y:
            rng.append(2)
        for k in rng:
            if self.iy == 1 and self.y+k < 8 and ob1 == 0:
                if board[self.y+k][self.x]:
                    ob1 = 1
                else:
                    positions.append((self.x, self.y+k))
            elif self.iy == 6 and self.y-k > -1 and ob1 == 0:
                if board[self.y - k][self.x]:
                    ob1 = 1
                else:
                    positions.append((self.x, self.y - k))
        return positions

    def diaPos(self,board):
        positions=[]
        if self.iy == 1:
            if self.x+1 < 8 and self.y+1 < 8:
                positions.append((self.x+1, self.y+1))
            if self.x-1 > -1 and self.y+1 < 8:
                positions.append((self.x-1, self.y+1))
        elif self.iy == 6:
            if self.x+1 < 8 and self.y-1 > -1:
                positions.append((self.x+1, self.y-1))
            if self.x-1 > -1 and self.y-1 > -1:
                positions.append((self.x-1, self.y-1))
        return positions

    def diaP(self, board):
        positions=[]
        if self.iy == 1:
            if self.x+1 < 8 and self.y+1 < 8:
                if board[self.y+1][self.x+1] and board[self.y+1][self.x+1].color != self.color:
                    positions.append((self.x+1, self.y+1))
            if self.x-1 > -1 and self.y+1 < 8:
                if board[self.y+1][self.x-1] and board[self.y+1][self.x-1].color != self.color:
                    positions.append((self.x-1, self.y+1))
        elif self.iy == 6:
            if self.x+1 < 8 and self.y-1 > -1:
                if board[self.y-1][self.x+1] and board[self.y-1][self.x+1].color != self.color:
                    positions.append((self.x+1, self.y-1))
            if self.x-1 > -1 and self.y-1 > -1:
                if board[self.y-1][self.x-1] and board[self.y-1][self.x-1].color != self.color:
                    positions.append((self.x-1, self.y-1))
        return positions

    def possibPositionsbyB(self, board,last_move):
        if self.isEnable():
            positions = self.possibPositions(board)
            for x, y in positions:
                if board[y][x] and board[y][x].color == self.color:
                    positions[positions.index((x, y))] = '-'
            positions+=self.diaP(board)
            return filter(lambda l: l != '-', positions)
        else:
            return []

    def setPosition(self, pos):
        self.x, self.y = pos

    def getPosition(self):
        return [self.x, self.y]
