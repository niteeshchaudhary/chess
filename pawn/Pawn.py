from Board import Board 
import math
COLORS={'w':'b','b':'w'}
DIRECTIONS={'w':-1,'b':1}
class Pawn:
    def __init__(self,x,y,color):
        self.color=color
        self.opcolor=COLORS[color]
        if y==1 or y==6:
            self.moved=False
        else:
            self.moved=True
        self.x=x
        self.y=y
        self.name="p"+color
        self.icon = "♙" if color == "white" else "♟"
        
    def checkPromote(self):
        if self.color=='w' and self.y==0:
            return True
        if self.color=='b' and self.y==7:
            return True
        return False
        
    def checkd(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
        if Board.board[y][x][1]==self.opcolor:
            if not Board.check:
                return True
            else:
                prev=Board.board[y][x]
                Board.board[y][x]=self.name
                Board.board[self.y][self.x]="  "
                if Board.is_check_resolved(Board.board[y][x]):
                    Board.board[y][x]=prev
                    Board.board[self.y][self.x]=self.name
                    return True
                Board.board[self.y][self.x]=self.name
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
                Board.board[self.y][self.x]="  "
                if Board.is_check_resolved(Board.board[y][x]):
                    Board.board[y][x]="  "
                    Board.board[self.y][self.x]=self.name
                    return True
                Board.board[self.y][self.x]=self.name
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
                Board.board[self.y][self.x]="  "
                if Board.is_check_resolved(Board.board[y][x]):
                    Board.board[y][x]="  "
                    Board.board[self.y][self.x]=self.name
                    return True
                Board.board[self.y][self.x]=self.name
                Board.board[y][x]="  "
        return False
    
    def check_en_peasant(self,x,y):
        mv=Board.last_move
        if mv[0]=="p":
            print( int(mv[1])==x and math.floor((int(mv[2])+int(mv[5]))/2) == y)
            if int(mv[1])==x and math.floor((int(mv[2])+int(mv[5]))/2) == y:
                if not Board.check:
                    return True
            
                else:
                    prev=Board.board[y][x]
                    Board.board[y][x]=self.name
                    Board.board[self.y][self.x]="  "
                    if Board.is_check_resolved(Board.board[y][x]):
                        Board.board[y][x]=prev
                        Board.board[self.y][self.x]=self.name
                        return True
                    Board.board[self.y][self.x]=self.name
                    Board.board[y][x]=prev
            
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
            
            
        if self.check_en_peasant(self.x+1,self.y+d):
            print("+"*50)
            print(self.x,self.y,self.x+1,self.y+d,"\n")
            moves.append((self.x+1,self.y+d))
        if self.check_en_peasant(self.x-1,self.y+d):
            print("+"*50)
            print(self.x,self.y,self.x-1,self.y+d,"\n")
            moves.append((self.x-1,self.y+d))
                
        return moves
            
            
        