from Rook import Rook
from Board import Board

# r1=Rook(0,6,'w')
# r2=Rook(1,6,'w')
# r3=Rook(2,6,'w')
# r4=Rook(3,3,'w')
# r5=Rook(4,3,'w')
# r6=Rook(5,5,'w')
# r7=Rook(6,4,'w')
# r8=Rook(7,5,'w')

r1=Rook(0,5,'b')
r2=Rook(1,4,'b')
r3=Rook(2,1,'b')
r4=Rook(3,0,'b')
r5=Rook(4,2,'b')
r6=Rook(5,4,'b')
r7=Rook(6,2,'b')
r8=Rook(7,4,'b')

Board.show_moves(r1.generate_moves())
print("*"*40)
Board.show_moves(r2.generate_moves())
print("*"*40)
Board.show_moves(r3.generate_moves())
print("*"*40)
Board.show_moves(r4.generate_moves())
print("*"*40)
Board.show_moves(r5.generate_moves())
print("*"*40)
Board.show_moves(r6.generate_moves())
print("*"*40)
Board.show_moves(r7.generate_moves())
print("*"*40)
Board.show_moves(r8.generate_moves())
print("*"*40)


# class Game():
#     def __init__(self):
        
    