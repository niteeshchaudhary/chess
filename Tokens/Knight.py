from .Tokens import Tokens


class Knight(Tokens):

    def __init__(self, x, y, color):
        super().__init__(x, y, color,"knight")
        self.icon = "♘" if color == "white" else "♞"

    def possibPositions(self):
        positions = []
        for k in [1, 2]:
            if self.x+k < 8 and self.y+3-k < 8:
                positions.append((self.x+k, self.y+3-k))
            if self.x-k > -1 and self.y+3-k < 8:
                positions.append((self.x-k, self.y+3-k))
            if self.x+k < 8 and self.y-3+k > -1:
                positions.append((self.x+k, self.y-3+k))
            if self.x-k > -1 and self.y-3+k > -1:
                positions.append((self.x-k, self.y-3+k))
        return positions

    def possibPositionsbyB(self, board,last_move):
        if self.isEnable():
            positions = self.possibPositions()
            for x, y in positions:
                if board[y][x] and board[y][x].color == self.color:
                    positions[positions.index((x, y))] = '-'
            return filter(lambda l: l != '-', positions)
        else:
            return []

    def setPosition(self,pos):
        self.x, self.y = pos

    def getPosition(self):
        return [self.x, self.y]
