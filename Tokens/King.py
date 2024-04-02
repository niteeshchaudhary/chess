from .Tokens import Tokens


class King(Tokens):

    def __init__(self, x, y, color):
        super().__init__(x, y, color,"King")
        self.moved = 0
        self.icon = "♔" if color == "white" else "♚"

    def possibPositions(self):
        positions = []
        k = 1
        if self.x+k < 8:
            positions.append((self.x+k, self.y))
        if self.x-k > -1:
            positions.append((self.x-k, self.y))
        if self.y+k < 8:
            positions.append((self.x, self.y+k))
        if self.y-k > -1:
            positions.append((self.x, self.y-k))
        if self.x+k < 8 and self.y+k < 8:
            positions.append((self.x+k, self.y+k))
        if self.x-k > -1 and self.y-k > -1:
            positions.append((self.x-k, self.y-k))
        if self.x+k < 8 and self.y-k > -1:
            positions.append((self.x+k, self.y-k))
        if self.x-k > -1 and self.y+k < 8:
            positions.append((self.x-k, self.y+k))

        return positions

    def calcOp(self, entry, board,last_move):
        for j in entry:
            if j and j.color != self.color:
                if type(j) == type(self):
                    pos = j.possibPositions()
                    for p in pos:
                        if (self.x, self.y) == p:
                            return [True, j]
                elif str(type(j)) == "<class 'Tokens.Pawn.Pawn'>":
                    pos = j.diaPos(board)
                    for p in pos:
                        if (self.x, self.y) == p:
                            return [True, j]
                elif str(type(j)) == "<class 'Tokens.Bishop.Bishop'>":
                    pos = j.possibPositionsbyB(board,last_move)
                    for p in pos:
                        if (self.x, self.y) == p:
                            return [True, j]
                elif str(type(j)) == "<class 'Tokens.Queen.Queen'>":
                    pos = j.possibPositionsbyB(board,last_move)
                    for p in pos:
                        if (self.x, self.y) == p:
                            return [True, j]
                elif str(type(j)) == "<class 'Tokens.King.King'>":
                    pos = j.possibPositionsbyB(board,last_move)
                    for p in pos:
                        if (self.x, self.y) == p:
                            return [True, j]
                elif str(type(j)) == "<class 'Tokens.Knight.Knight'>":
                    pos = j.possibPositionsbyB(board,last_move)
                    for p in pos:
                        if (self.x, self.y) == p:
                            return [True, j]
                elif str(type(j)) == "<class 'Tokens.Rook.Rook'>":
                    pos = j.possibPositionsbyB(board,last_move)
                    for p in pos:
                        if (self.x, self.y) == p:
                            return [True, j]
                else:
                    pos = j.possibPositionsbyB(board,last_move)
                    for p in pos:
                        if (self.x, self.y) == p:
                            return [True, j]
        return [False, None]

    def checkOp(self, board, spos,last_move):
        print(board)
        for i in board:
            for j in i:
                print(j)
                if j and j.color!=self.color:
                    if type(j) == type(self):
                        pos = j.possibPositions()
                        for p in pos:
                            if p in spos:
                                spos[spos.index(p)] = '-'
                    elif str(type(j)) == "<class 'Tokens.Pawn.Pawn'>":
                        pos = j.diaPos(board)
                        for p in pos:
                            if p in spos:
                                spos[spos.index(p)] = '-'
                    elif str(type(j)) == "<class 'Tokens.Bishop.Bishop'>":
                        pos = j.possibPositionsbyB(board,last_move)
                        for p in pos:
                            if p in spos:
                                spos[spos.index(p)] = '-'
                    elif str(type(j)) == "<class 'Tokens.Knight.Knight'>":
                        pos = j.possibPositionsbyB(board,last_move)
                        for p in pos:
                            if p in spos:
                                spos[spos.index(p)] = '-'
                    elif str(type(j)) == "<class 'Tokens.Queen.Queen'>":
                        pos = j.possibPositionsbyB(board,last_move)
                        for p in pos:
                            if p in spos:
                                spos[spos.index(p)] = '-'
                    elif str(type(j)) == "<class 'Tokens.King.King'>":
                        pos = j.possibPositionsbyB(board,last_move)
                        for p in pos:
                            if p in spos:
                                spos[spos.index(p)] = '-'
                    elif str(type(j)) == "<class 'Tokens.Rook.Rook'>":
                        pos = j.possibPositionsbyB(board,last_move)
                        for p in pos:
                            if p in spos:
                                spos[spos.index(p)] = '-'
                    else:
                        pos = j.possibPositionsbyB(board,last_move)
                        for p in pos:
                            if p in spos:
                                spos[spos.index(p)] = '-'
        return spos

    def possibPositionsbyB(self, board,last_move):
        if self.isEnable():
            positions = self.possibPositions()
            for x, y in positions:
                if board[y][x] and board[y][x].color == self.color:
                    positions[positions.index((x, y))] = '-'
            if self.moved == 0 and board[self.y][7] and (not board[self.y][4] and not board[self.y][6] \
                    and not board[self.y][5]) and board[self.y][7].moved == 0:
                positions.append((6, self.y))
            if self.moved == 0 and board[self.y][0] and (not board[self.y][1] and not board[self.y][2] \
                    and not board[self.y][3]) and board[self.y][0].moved == 0:
                positions.append((2, self.y))
            return filter(lambda l: l != '-', self.checkOp(board, positions,last_move))
        else:
            return []

    def setPosition(self, pos):
        self.moved=1
        self.x, self.y = pos

    def getPosition(self):
        return [self.x, self.y]
