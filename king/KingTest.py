from King import King
from Rook import Rook
from Board import Board
from Pawn import Pawn

for xi,i in enumerate(Board.board):
    for xj,j in enumerate(i):
        if j[0]=="r":
            Board.board[xi][xj]=Rook(xj,xi,j[1])
        elif j[0]=="p":
            Board.board[xi][xj]=Pawn(xj,xi,j[1])
        elif j[0]=="k":
            Board.board[xi][xj]=King(xj,xi,j[1])
            
# k1=King(0,6,'w')
# k2=King(1,6,'w')
# k3=King(2,6,'w')
# k4=King(3,3,'w')
# k5=King(4,3,'w')
# k6=King(5,5,'w')
# k7=King(6,4,'w')
# k8=King(7,5,'w')

# p1=Pawn(0,5,'b')
# p2=Pawn(1,4,'b')
# r3=Rook(2,1,'b')
# k1=King(3,0,'b')
# r4=Rook(3,2,'b')
# p4=Pawn(5,4,'b')
# p5=Pawn(6,2,'b')
# r5=Rook(7,4,'b')
# r1=Rook(0,0,'b')
# r2=Rook(7,0,'b')

for xi,i in enumerate(Board.board):
    for xj,j in enumerate(i):
        if j!="  ":
            print(j,xi,xj)
            Board.show_moves(j.generate_moves())
            print("*"*40)