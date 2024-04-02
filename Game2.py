
class Game2:
    def __init__(self):
        self.dcolor = ['white', 'black']
        self.board = []
        self.butones=[]
        self.turn = 0
        self.allwhite=[]
        self.allblack = []

    def initB(self):
        self.board=self.createBoard()

    def createBoard(self):
        board=[]
        rc = [None]*8
        for i in range(8):
            board.append(rc.copy())

        return board

    def printBoard(self):
        for i in self.board:
            for j in i:
                print(" "+j.icon+" " if j else ' . ', end='')
            print()

    def checkCheck(self):
        if self.dcolor[self.turn]=="white":
            for p, i in enumerate(self.allwhite):
                if str(type(i)) == "<class 'King.King'>":
                    ischk, bychk = i.calcOp(self.allblack, self.board)
                    if ischk:
                        return [True, p, bychk]
        elif self.dcolor[self.turn]=="black":
            for p,i in enumerate(self.allblack):
                if str(type(i)) == "<class 'King.King'>":
                    ischk, bychk = i.calcOp(self.allwhite, self.board)
                    if ischk:
                        return [True, p, bychk]
        return [False, -1, None]

    def checkCheckMate(self):
        op, y, bychk = self.checkCheck()
        kng=None
        if op:
            if self.dcolor[self.turn] == "black":
                kng = self.allblack[y]
            elif self.dcolor[self.turn]=="white":
                kng = self.allwhite[y]
            print("Print Check")
            self.butones[kng.y][kng.x].setColor("red")
            cpk = list(kng.possibPositionsbyB(self.board))
            print(cpk)
            if len(cpk)==0:
                tp=self.chkKill(bychk)
                print(tp)
                if not tp[0]:
                    #self.chkBetw(kng,bychk)
                    print("Game Over")

    def chkKill(self, bychk):
        prot=False
        if bychk.color == "black":
            prot, byprot=self.calcOp(self.allwhite, self.board, bychk)
        elif bychk.color == "white":
            prot, byprot = self.calcOp(self.allblack, self.board, bychk)
        return prot,byprot

    def calcOp(self, entry, board,bychk):

        for j in entry:
                if type(j) == "<class 'King.King'>":
                    pos = j.possibPositions()
                    for p in pos:
                        if (bychk.x, bychk.y) == p:
                            return [True, j]
                elif str(type(j)) == "<class 'Pawn.Pawn'>":
                    pos = j.diaPos(board)
                    for p in pos:
                        if (bychk.x, bychk.y) == p:
                            return [True, j]
                else:
                    pos = j.possibPositionsbyB(board)
                    for p in pos:
                        if (bychk.x, bychk.y) == p:
                            return [True, j]

        return [False, None]

    def display(self):
        root = tk.Tk()
        LeftFrame = tk.Frame(root)
        LeftFrame.grid()
        # Create a 2-d list containing 3 rows, 3 columns (using list comprehension)
        self.butones = [[None for i in range(8)] for j in range(8)]

        for i in range(8):
            for j in range(8):
                current_button = Block(LeftFrame,
                                           text=f"{self.board[i][j].icon if self.board[i][j] else '' }",
                                           font=("tahoma", 35, "bold"),
                                           width=3,
                                           height=0,
                                           bg="grey" if(i+j)%2 else "white",
                                           command=lambda i=i, j=j: self.onClick(i, j))
                                        # lambda is passed parameters i and j
                # Grid occurs on a new line
                current_button.grid(row=i + 1, column=j + 1)
                self.butones[i][j] = current_button

        root.mainloop()
    def clearb(self):
        for y_ind in range(8):
            for x_ind in range(8):
                if (self.butones[y_ind][x_ind].getColor() != "red"):
                    self.butones[y_ind][x_ind].resetColor()
                self.butones[y_ind][x_ind].resetParent()

    def onClick(self, i, j):
        #print(f"You pressed button {i},{j}")
        if(self.butones[i][j].getColor()=="lightgreen"):
            par=self.butones[i][j].getParent()
            if self.board[i][j]:
                if self.board[i][j].color=="white":
                    self.allwhite.remove(self.board[i][j])
                elif self.board[i][j].color=="black":
                    self.allblack.remove(self.board[i][j])
            if str(type(self.board[par[0]][par[1]]))=="<class 'King.King'>":
                print("in")
                if j-par[1] == 2:
                    self.board[i][7].setPosition((5, i))
                    self.board[i][7].moved=1
                    self.board[i][5] = self.board[i][7]
                    self.board[i][7] = None
                    self.butones[i][5].setIcon(self.butones[i][7].getIcon())
                    self.butones[i][7].setIcon('')
                    print("in 1")
                elif j - par[1] == -2:
                    self.board[i][0].moved = 1
                    self.board[i][0].setPosition((3, i))
                    self.board[i][3] = self.board[i][0]
                    self.board[i][0] = None
                    self.butones[i][3].setIcon(self.butones[i][0].getIcon())
                    self.butones[i][0].setIcon('')
                    print("in 2")

                self.board[par[0]][par[1]].moved = 1
            elif str(type(self.board[par[0]][par[1]])) == "<class 'Rook.Rook'>":
                self.board[par[0]][par[1]].moved = 1

            self.clearb()
            self.butones[i][j].setColor("orchid1")
            self.butones[par[0]][par[1]].setColor("purple")
            self.board[par[0]][par[1]].setPosition((j, i))
            self.board[i][j] = self.board[par[0]][par[1]]
            self.board[par[0]][par[1]] = None
            self.butones[i][j].setIcon(self.butones[par[0]][par[1]].getIcon())
            self.butones[par[0]][par[1]].setIcon('')
            self.turn=(self.turn+1)%2
            self.checkCheckMate()
            #self.printBoard()
        else:
            self.clearb()
            if self.board[i][j]:
                pmoves = self.board[i][j].possibPositionsbyB(self.board)
                if(self.dcolor[self.turn]==self.board[i][j].color):
                    self.butones[i][j].setColor("lightblue")
                    for m in pmoves:
                        self.butones[m[1]][m[0]].setColor("lightgreen")
                        self.butones[m[1]][m[0]].setParent((i, j))
                else:
                    self.butones[i][j].setColor("firebrick1")
                    for m in pmoves:
                        self.butones[m[1]][m[0]].setColor("coral")


if __name__ == '__main__':
    G=Game2()
    G.initB()
    G.display()