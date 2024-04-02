from Board import Board
from Possible_Moves import KingMoves, PawnMoves, RookMoves  
import math
COLORS={'w':'b','b':'w'}
DIRECTIONS={'w':-1,'b':1}

class King:
    def __init__(self,x,y,color):
        self.color=color
        self.opcolor=COLORS[color]
        if y==0 or y==7:
            self.moved=False
        else:
            self.moved=True
        self.x=x
        self.y=y
        self.name="k"+color
        self.icon = "♔" if color == "w" else "♚"
        
    def __str__(self):
        return self.name
        
    def check(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        if Board.board[y][x]=="  " or Board.board[y][x].color==self.opcolor:
            if not Board.check:
                prev=Board.board[y][x]
                Board.board[y][x]=self
                Board.board[self.y][self.x]="  "
                if not self.is_danger(x,y):
                    Board.board[self.y][self.x]=self
                    Board.board[y][x]=prev
                    return True
                Board.board[self.y][self.x]=self
                Board.board[y][x]=prev
            else: 
                prev=Board.board[y][x]
                Board.board[y][x]="  "
                if Board.is_check_resolved():
                    Board.board[y][x]=prev
                    return True
                Board.board[y][x]=prev
            
        return False
    
    def initchecks(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
    
    def check_left_castle(self,x,y):
        if not (x==2 and (y==0 or y==7)):
            return False
        
        # Your king can not have moved- Once your king moves, you can no longer castle, even if you move the king back to the starting square. Many strategies involve forcing the opponent’s king to move just for this reason. 
        # Your rook can not have moved- If you move your rook, you can’t castle on that side anymore. Both the king and the rook you are castling with can’t have moved. 
        if (not self.moved):
            # left Rook
            if Board.board[self.y][0].name=="r"+self.color:
                r=Board.board[self.y][0]
                if not r.moved:
                    for block in Board.board[self.y][1:self.x]:
                        if block!="  ":
                            return False
                    if not Board.check and self.check(self.x-1,self.y) and self.check(self.x-2,self.y):
                        return True
    
    def check_right_castle(self,x,y):
        if not (x==6 and (y==0 or y==7)):
            return False
        
        # Your king can not have moved- Once your king moves, you can no longer castle, even if you move the king back to the starting square. Many strategies involve forcing the opponent’s king to move just for this reason. 
        # Your rook can not have moved- If you move your rook, you can’t castle on that side anymore. Both the king and the rook you are castling with can’t have moved. 
        if (not self.moved):
            # right Rook
            if Board.board[self.y][7].name=="r"+self.color:
                r=Board.board[self.y][7]
                if not r.moved:
                    for block in Board.board[self.y][self.x+1:7]:
                        if block!="  ":
                            return False
                    if not Board.check and self.check(self.x+1,self.y) and self.check(self.x+2,self.y):
                        return True
                        
                            
        # Your king can NOT be in check- Though castling often looks like an appealing escape, you can’t castle while you are in check! Once you are out of check, then you can castle. Unlike moving, being checked does not remove the ability to castle later. 
        # Your king can not pass through check- If any square the king moves over or moves onto would put you in check, you can’t castle. You’ll have to get rid of that pesky attacking piece first!
        # No pieces can be between the king and rook- All the spaces between the king and rook must be empty. This is part of why it’s so important to get your pieces out into the game as soon as possible! 

    
    def is_danger(self,x,y):
        for i in Board.board:
            for j in i:
                if j!="  " and j.color!=Board.board[y][x].color:
                    moves=j.generate_possible_moves(Board.board)
                    if (x,y) in moves:
                        return True     
        return False
                
    def generate_moves(self)->list:
        moves=[]
        d=DIRECTIONS[self.color] # to decide direction of movement
        if self.check(self.x+1,self.y+1):
            print(self.x+1,self.y+1)
            moves.append((self.x+1,self.y+1))
        if self.check(self.x,self.y+1):
            print(self.x,self.y+1)
            moves.append((self.x,self.y+1))
        if self.check(self.x-1,self.y+1):
            print(self.x-1,self.y+1)
            moves.append((self.x-1,self.y+1))
            
        if self.check(self.x+1,self.y):
            print(self.x+1,self.y)
            moves.append((self.x+1,self.y))
        if self.check(self.x-1,self.y):
            print(self.x-1,self.y)
            moves.append((self.x-1,self.y))
            
        if self.check(self.x+1,self.y-1):
            print(self.x+1,self.y-1)
            moves.append((self.x+1,self.y-1))
        if self.check(self.x,self.y-1):
            print(self.x,self.y-1)
            moves.append((self.x,self.y-1))
        if self.check(self.x-1,self.y-1):
            print(self.x-1,self.y-1)
            moves.append((self.x-1,self.y-1))
        
            
        if self.check_right_castle(self.x+2,self.y):
            print(self.x+2,self.y,":")
            moves.append((self.x+2,self.y))
        
        if self.check_left_castle(self.x-2,self.y):
            print(self.x-2,self.y,":")
            moves.append((self.x-2,self.y))
                
        return moves
    
    def possible_check(self,x,y,board):
        if x<0 or y<0 or x>7 or y>7:
            return False
        if board[y][x].color==self.opcolor or board[y][x]=="  ":
            return True
            
        return False
    
    def generate_possible_moves(self,board)->list:
        moves=[]
        if self.possible_check(self.x+1,self.y+1,board):
            moves.append((self.x+1,self.y+1))
        if self.possible_check(self.x,self.y+1,board):
            moves.append((self.x,self.y+1))
        if self.possible_check(self.x-1,self.y+1,board):
            moves.append((self.x-1,self.y+1))
            
        if self.possible_check(self.x+1,self.y,board):
            moves.append((self.x+1,self.y))
        if self.possible_check(self.x-1,self.y,board):
            moves.append((self.x-1,self.y))
            
        if self.possible_check(self.x+1,self.y-1,board):
            moves.append((self.x+1,self.y-1))
        if self.possible_check(self.x,self.y-1,board):
            moves.append((self.x,self.y-1))
        if self.possible_check(self.x-1,self.y-1,board):
            moves.append((self.x-1,self.y-1))
                
        return moves
            
            
        