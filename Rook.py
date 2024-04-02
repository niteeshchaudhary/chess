from Board import Board 
import math
COLORS={'w':'b','b':'w'}
DIRECTIONS={'w':-1,'b':1}
class Rook:
    def __init__(self,x,y,color):
        self.color=color
        self.opcolor=COLORS[color]
        if (y==0 or y==7) and (x==0 or x==7):
            self.moved=False
        else:
            self.moved=True
        self.x=x
        self.y=y
        self.name="p"+color
        
    def checkd(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
        if Board.board[y][x][1]==self.opcolor:
            if not Board.check:
                return True
            else:
                prev=Board.board[y][x]
                Board.board[y][x]=self.name
                if Board.is_check_resolved(Board.board[y][x]):
                    Board.board[y][x]=prev
                    return True
                Board.board[y][x]=prev
        return False
    
    def checks(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        if Board.board[y][x]=="  ":
            if not Board.check:
                return True
            else:
                Board.board[y][x]=self.name
                if Board.is_check_resolved(Board.board[y][x]):
                    Board.board[y][x]="  "
                    return True
                Board.board[y][x]="  "
        return False
    
    def initchecks(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        d=DIRECTIONS[self.opcolor] # we want to check one before like for white y-2 check y+d
        # print(Board.board[y+d][x],Board.board[y][x],f"{y+d} {x} {Board.board[y+d]}")
        if Board.board[y+d][x]=="  " and Board.board[y][x]=="  ":
            if not Board.check:
                return True
            else:
                Board.board[y][x]=self.name
                if Board.is_check_resolved(Board.board[y][x]):
                    Board.board[y][x]="  "
                    return True
                Board.board[y][x]="  "
        return False
    
            
    
    def generate_moves(self)->list:
        moves=[]
        d=DIRECTIONS[self.color] # to decide direction of movement
        if self.checkd(self.x+1,self.y+d):
            print(self.x+1,self.y+d,"*")
            moves.append((self.x+1,self.y+d))
        if self.checkd(self.x-1,self.y+d):
            print(self.x,self.y,self.x-1,self.y+d,"_")
            moves.append((self.x-1,self.y+d))
        if self.checks(self.x,self.y+d):
            print(self.x,self.y+d,"(")
            moves.append((self.x,self.y+d))
            
        if (not self.moved) and self.initchecks(self.x,self.y+d*2):
            print(self.x,self.y+d*2,":")
            moves.append((self.x,self.y+d*2))
            
            
                
        return moves
            
            
        