from .Tokens import Tokens


class Bishop(Tokens):

    def __init__(self, x, y, color):
        super().__init__(x, y, color,"bishop")
        self.icon = "♗" if color == "white" else "♝"

    def possibPositions(self, board):
        positions = []
        ob1, ob2, ob3, ob4 = 0, 0, 0, 0
        for k in range(1, 8):
            if self.x + k < 8 and self.y + k < 8 and ob1 == 0:
                if board[self.y + k][self.x + k]:
                    ob1 = 1
                    if board[self.y + k][self.x + k].color != self.color:
                        positions.append((self.x + k, self.y + k))
                else:
                    positions.append((self.x + k, self.y + k))

            if self.x - k > -1 and self.y - k > -1 and ob2 == 0:
                if board[self.y - k][self.x - k]:
                    ob2 = 1
                    if board[self.y - k][self.x - k].color != self.color:
                        positions.append((self.x - k, self.y - k))
                else:
                    positions.append((self.x - k, self.y - k))

            if self.x + k < 8 and self.y - k > -1 and ob3 == 0:
                if board[self.y - k][self.x + k]:
                    ob3 = 1
                    if board[self.y - k][self.x + k].color != self.color:
                        positions.append((self.x + k, self.y - k))
                else:
                    positions.append((self.x + k, self.y - k))

            if self.x - k > -1 and self.y + k < 8 and ob4 == 0:
                if board[self.y + k][self.x - k]:
                    ob4 = 1
                    if board[self.y + k][self.x - k].color != self.color:
                        positions.append((self.x - k, self.y + k))
                else:
                    positions.append((self.x - k, self.y + k))
        return positions

    def possibPositionsbyB(self, board,last_move):
        if self.isEnable():
            positions = self.possibPositions(board)
            for x, y in positions:
                if board[y][x] and board[y][x].color == self.color:
                    positions[positions.index((x, y))] = '-'
            return filter(lambda l:l!='-', positions)
        else:
            return []

    def setPosition(self, pos):
        self.x, self.y = pos

    def getPosition(self):
        return [self.x, self.y]
