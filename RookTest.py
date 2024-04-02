from Pawn import Pawn
from ... import Board

# p1=Pawn(0,6,'w')
# p2=Pawn(1,6,'w')
# p3=Pawn(2,6,'w')
# p4=Pawn(3,3,'w')
# p5=Pawn(4,3,'w')
# p6=Pawn(5,5,'w')
# p7=Pawn(6,4,'w')
# p8=Pawn(7,5,'w')

p1=Pawn(0,5,'b')
p2=Pawn(1,4,'b')
p3=Pawn(2,3,'b')
p4=Pawn(3,1,'b')
p5=Pawn(4,2,'b')
p6=Pawn(5,4,'b')
p7=Pawn(6,2,'b')
p8=Pawn(7,4,'b')

Board.show_moves(p1.generate_moves())
print("*"*40)
Board.show_moves(p2.generate_moves())
print("*"*40)
Board.show_moves(p3.generate_moves())
print("*"*40)
Board.show_moves(p4.generate_moves())
print("*"*40)
Board.show_moves(p5.generate_moves())
print("*"*40)
Board.show_moves(p6.generate_moves())
print("*"*40)
Board.show_moves(p7.generate_moves())
print("*"*40)
Board.show_moves(p8.generate_moves())
print("*"*40)


# class Game():
#     def __init__(self):
        
    