import tkinter as tk
from Tokens.Bishop import Bishop
from Tokens.Rook import Rook
from Tokens.Knight import Knight
from Tokens.King import King
from Tokens.Queen import Queen
from Tokens.Pawn import Pawn
from Block import Block
from Tokens.GameState import GameState
import time


history = open(f"history/history{time.time()}.txt", "w+", encoding="utf-8")

class Game:

    def __init__(self):
        self.dcolor = ['white', 'black']
        self.board = []
        self.buttons = []
        self.turn = 0
        self.all_white = []
        self.all_black = []
        self.last_move="None"
        self.start_box=""
        self.end_box=""
        self.check=False
        self.check_mate=False

    def initB(self):
        self.board = self.createBoard()

    def createBoard(self):
        rb = [Rook(0,0,self.dcolor[1]),Knight(1,0,self.dcolor[1]),Bishop(2,0,self.dcolor[1]), 
              Queen(3,0,self.dcolor[1]),King(4,0,self.dcolor[1]),Bishop(5,0,self.dcolor[1]), 
              Knight(6,0,self.dcolor[1]),Rook(7,0,self.dcolor[1])]
        rbp = [Pawn(0, 1, self.dcolor[1]),Pawn(1, 1, self.dcolor[1]),Pawn(2, 1, self.dcolor[1]), 
               Pawn(3, 1, self.dcolor[1]),Pawn(4, 1, self.dcolor[1]),Pawn(5, 1, self.dcolor[1]), 
               Pawn(6, 1, self.dcolor[1]),Pawn(7, 1, self.dcolor[1])]
        rw = [Rook(0, 7, self.dcolor[0]), Knight(1, 7, self.dcolor[0]), Bishop(2, 7, self.dcolor[0]),
              Queen(3, 7, self.dcolor[0]), King(4, 7, self.dcolor[0]), Bishop(5, 7, self.dcolor[0]),
              Knight(6, 7, self.dcolor[0]), Rook(7, 7, self.dcolor[0])]
        rwp = [Pawn(0, 6, self.dcolor[0]), Pawn(1, 6, self.dcolor[0]), Pawn(2, 6, self.dcolor[0]), 
               Pawn(3, 6, self.dcolor[0]), Pawn(4, 6, self.dcolor[0]), Pawn(5, 6, self.dcolor[0]),
              Pawn(6, 6, self.dcolor[0]), Pawn(7, 6, self.dcolor[0])]
        rc = [None]*8
        board = [rb,rbp]
        for i in range(4):
            board.append(rc.copy())
        board.append(rwp)
        board.append(rw)
        self.all_black = rb.copy()+rbp.copy()
        self.all_white = rw.copy() + rwp.copy()
        return board

    def printBoard(self):
        for i in self.board:
            for j in i:
                print(" "+j.icon+" " if j else ' . ', end='')
            print()

    def checkCheck(self):
        if self.dcolor[self.turn]=="white":
            for p, i in enumerate(self.all_white):
                i.setEnable(True)
                if str(type(i)) == "<class 'Tokens.King.King'>":
                    ischk, bychk = i.calcOp(self.all_black, self.board,self.last_move)
                    if ischk:
                        for ele in self.all_white:
                            if str(type(ele)) != "<class 'Tokens.King.King'>":
                                ele.setEnable(False)
                                print(ele)
                        self.check=True
                        GameState.check=True
                        return [True, p, bychk]

        elif self.dcolor[self.turn]=="black":
            for p, i in enumerate(self.all_black):
                i.setEnable(True)
                if str(type(i)) == "<class 'Tokens.King.King'>":
                    ischk, bychk = i.calcOp(self.all_white, self.board,self.last_move)
                    if ischk:
                        for ele in self.all_black:
                            if str(type(ele)) != "<class 'Tokens.King.King'>":
                                ele.setEnable(False)
                                print(ele)
                        self.check=True
                        GameState.check=True
                        return [True, p, bychk]
        self.check=False
        GameState.check=False
        return [False, -1, None]

    def checkCheckMate(self):
        op, y, bychk = self.checkCheck()
        kng=None
        if op:
            if self.dcolor[self.turn] == "black":
                kng = self.all_black[y]
            elif self.dcolor[self.turn]=="white":
                kng = self.all_white[y]
            print("Print Check")
            self.buttons[kng.y][kng.x].setColor("red")
            cpk = list(kng.possibPositionsbyB(self.board,self.last_move))
            print(cpk)
            if len(cpk)==0:
                tp=self.chkKill(bychk)
                print(tp)
                if not tp[0]:
                    #self.chkBetw(kng,bychk)
                    GameState.check_mate=True
                    self.check_mate=True
                    print("Game Over")

    def chkKill(self, bychk):
        prot=False
        if bychk.color == "black":
            prot, byprot=self.calcOp(self.all_white, self.board, bychk)
        elif bychk.color == "white":
            prot, byprot = self.calcOp(self.all_black, self.board, bychk)
        return prot, byprot

    def calcOp(self, entry, board,bychk):

        for j in entry:
                if type(j) == "<class 'Tokens.King.King'>":
                    pos = j.possibPositions()
                    for p in pos:
                        if (bychk.x, bychk.y) == p:
                            return [True, j]
                elif str(type(j)) == "<class 'Tokens.Pawn.Pawn'>":
                    pos = j.diaPos(board)
                    print(pos)
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
        self.buttons = [[None for i in range(8)] for j in range(8)]

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
                self.buttons[i][j] = current_button

        root.mainloop()
    def clearb(self):
        for y_ind in range(8):
            for x_ind in range(8):
                if (self.buttons[y_ind][x_ind].getColor() != "red"):
                    self.buttons[y_ind][x_ind].resetColor()
                self.buttons[y_ind][x_ind].resetParent()

    def onClick(self, i, j):
        #print(f"You pressed button {i},{j}")
        if(self.buttons[i][j].getColor()=="lightgreen"):
            par=self.buttons[i][j].getParent()
            if str(type(self.board[par[0]][par[1]]))=="<class 'Tokens.Pawn.Pawn'>":
                print("here+++++++++++++++++1", (not self.board[i][j]) , (par[0]!=i and par[1]!=j))
                if (not self.board[i][j]) and (par[0]!=i and par[1]!=j):
                    print("here+++++++++++++++++2",str(type(self.board[par[0]][j])))
                    if str(type(self.board[par[0]][j]))=="<class 'Tokens.Pawn.Pawn'>":
                        if self.board[par[0]][j].color=="white":
                            self.all_white.remove(self.board[par[0]][j])
                        elif self.board[par[0]][j].color=="black":
                            self.all_black.remove(self.board[par[0]][j])
                    self.board[par[0]][j] = None
                    self.buttons[par[0]][j].setIcon('')
                    
            if self.board[i][j]:
                if self.board[i][j].color=="white":
                    self.all_white.remove(self.board[i][j])
                elif self.board[i][j].color=="black":
                    self.all_black.remove(self.board[i][j])
            print(par,"_"*10,str(type(self.board[par[0]][par[1]])))
            
                
            if str(type(self.board[par[0]][par[1]]))=="<class 'Token.King.King'>":
                print("in")
                if j-par[1] == 2:
                    self.board[i][7].setPosition((5, i))
                    self.board[i][7].moved=1
                    self.board[i][5] = self.board[i][7]
                    self.board[i][7] = None
                    self.buttons[i][5].setIcon(self.buttons[i][7].getIcon())
                    self.buttons[i][7].setIcon('')
                    print("in 1")
                elif j - par[1] == -2:
                    self.board[i][0].moved = 1
                    self.board[i][0].setPosition((3, i))
                    self.board[i][3] = self.board[i][0]
                    self.board[i][0] = None
                    self.buttons[i][3].setIcon(self.buttons[i][0].getIcon())
                    self.buttons[i][0].setIcon('')
                    print("in 2")

                self.board[par[0]][par[1]].moved = 1
            elif str(type(self.board[par[0]][par[1]])) == "<class 'Tokens.Rook.Rook'>":
                self.board[par[0]][par[1]].moved = 1

            self.clearb()
            self.buttons[i][j].setColor("orchid1")
            self.end_box=str(j)+str(i)
            self.last_move=self.start_box+"-"+self.end_box
            history.write(self.last_move+"\n")
            self.buttons[par[0]][par[1]].setColor("purple")
            self.board[par[0]][par[1]].setPosition((j, i))
            self.board[i][j] = self.board[par[0]][par[1]]
            self.board[par[0]][par[1]] = None
            self.buttons[i][j].setIcon(self.buttons[par[0]][par[1]].getIcon())
            self.buttons[par[0]][par[1]].setIcon('')
            self.turn = (self.turn+1) % 2
            self.checkCheckMate()
            GameState.setState(self.board,self.check,self.check_mate,self.last_move)
            #self.printBoard()
        else:
            self.clearb()
            print("->",self.board[i][j])
            if self.board[i][j]:
                self.start_box=self.board[i][j].icon+str(j)+str(i)
                pmoves = self.board[i][j].possibPositionsbyB(self.board,self.last_move)
                if self.dcolor[self.turn] == self.board[i][j].color:
                    self.buttons[i][j].setColor("lightblue")
                    for m in pmoves:
                        self.buttons[m[1]][m[0]].setColor("lightgreen")
                        self.buttons[m[1]][m[0]].setParent((i, j))
                else:
                    self.buttons[i][j].setColor("firebrick1")
                    for m in pmoves:
                        self.buttons[m[1]][m[0]].setColor("coral")




if __name__ == '__main__':
    G=Game()
    G.initB()
    G.printBoard()
    G.display()