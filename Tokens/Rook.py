from .Tokens import Tokens


class Rook(Tokens):

    def __init__(self, x, y, color):
        super().__init__(x, y, color,"rook")
        self.moved = 0
        self.icon = "♖" if color == "white" else "♜"

    def possibPositions(self, board):
        positions = []
        ob1, ob2, ob3, ob4 = 0, 0, 0, 0
        for k in range(1, 8):
            if self.x+k < 8 and ob1 == 0:
                if board[self.y][self.x+k]:
                    ob1=1
                    if board[self.y][self.x+k].color != self.color:
                        positions.append((self.x+k, self.y))
                else:
                    positions.append((self.x + k, self.y))
            if self.x-k > -1 and ob2 == 0:
                if board[self.y][self.x - k]:
                    ob2 = 1
                    if board[self.y][self.x - k].color != self.color:
                        positions.append((self.x-k, self.y))
                else:
                    positions.append((self.x - k, self.y))
            if self.y+k < 8 and ob3 == 0:
                if board[self.y+k][self.x]:
                    ob3 = 1
                    if board[self.y+k][self.x].color != self.color:
                        positions.append((self.x, self.y+k))
                else:
                    positions.append((self.x, self.y+k))
            if self.y-k > -1 and ob4 == 0:
                if board[self.y-k][self.x]:
                    ob4 = 1
                    if board[self.y-k][self.x].color != self.color:
                        positions.append((self.x, self.y-k))
                else:
                    positions.append((self.x, self.y-k))
        return list(set(positions))

    def possibPositionsbyB(self, board,last_move):
        if self.isEnable():
            positions = self.possibPositions(board)
            for x, y in positions:
                if board[y][x] and board[y][x].color == self.color:
                    positions[positions.index((x, y))] = '-'
            return filter(lambda l: l != '-', positions)
        else:
            return []

    def setPosition(self, pos):
        self.x, self.y = pos

    def getPosition(self):
        return [self.x, self.y]
