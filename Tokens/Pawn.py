from .GameState import GameState
import math
COLORS={'white':'black','black':'white'}
DIRECTIONS={'white':-1,'black':1}
class Pawn:
    def __init__(self,x,y,color):
        self.color=color
        self.opcolor=COLORS[color]
        self.x=x
        self.enable = True
        self.y=y
        if self.y==1 or self.y==6:
            self.moved=False
        else:
            self.moved=True
        
        self.name="p"+color[0]
        self.icon = "♙" if color == "white" else "♟"
        
    # def __str__(self):
    #     return self.icon
    
    def checkPromote(self):
        if self.color=='white' and self.y==0:
            return True
        if self.color=='black' and self.y==7:
            return True
        return False
        
    def checkd(self,x,y,board):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        if board[y][x] and board[y][x].color==self.opcolor:
            if not GameState.check:
                return True
            else:
                prev=board[y][x]
                board[y][x]=self.name
                curr=board[self.y][self.x]
                board[self.y][self.x]=None
                if GameState.is_check_resolved(board[y][x]):
                    board[y][x]=prev
                    return True
                board[self.y][self.x]=curr
                board[y][x]=prev
        return False
    
    def checks(self,x,y,board):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        if board[y][x]==None:
            if not GameState.check:
                return True
            else:
                board[y][x]=self.name
                if GameState.is_check_resolved(board[y][x]):
                    board[y][x]=None
                    return True
                board[y][x]=None
        return False
    
    def initchecks(self,x,y,board):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        d=DIRECTIONS[self.opcolor] # we want to check one before like for white y-2 check y+d
        # print(Board.board[y+d][x],Board.board[y][x],f"{y+d} {x} {Board.board[y+d]}")
        if board[y+d][x]==None and board[y][x]==None:
            if not GameState.check:
                return True
            else:
                board[y][x]=self.name
                if GameState.is_check_resolved(board[y][x]):
                    board[y][x]=None
                    return True
                board[y][x]=None
        return False
    
    def check_en_peasant(self,x,y,board,last_move):
        mv=last_move
        print(mv)
        icon="♟" if self.color == "white" else "♙" #checking for oppent icon
        if mv[0]==icon:
            
            print( int(mv[1])==x , math.ceil((int(mv[2])+int(mv[5]))/2) == y)
            if int(mv[1])==x and math.ceil((int(mv[2])+int(mv[5]))/2) == y:
                if not GameState.check:
                    return True
                else:
                    board[y][x]=self.name
                    prev=board[y-DIRECTIONS[self.color]][x]
                    board[y-DIRECTIONS[self.color]][x]=None
                    if GameState.is_check_resolved(board[y][x]):
                        board[y][x]=None
                        return True
                    board[y-DIRECTIONS[self.color]][x]=prev
                    board[y][x]=None
        return False
            
    def possibPositionsbyB(self,board,last_move):
        print(GameState.check,":"*30)
        return self.generate_moves(board,last_move)
    
    def generate_moves(self,board,last_move)->list:
        moves=[]
        d=DIRECTIONS[self.color] # to decide direction of movement
        if self.checkd(self.x+1,self.y+d,board):
            print(self.x+1,self.y+d,"*")
            moves.append((self.x+1,self.y+d))
        if self.checkd(self.x-1,self.y+d,board):
            print(self.x,self.y,self.x-1,self.y+d,"_")
            moves.append((self.x-1,self.y+d))
        if self.checks(self.x,self.y+d,board):
            print(self.x,self.y+d,"(")
            moves.append((self.x,self.y+d))
            
        if (not self.moved) and self.initchecks(self.x,self.y+d*2,board):
            print(self.x,self.y+d*2,":")
            moves.append((self.x,self.y+d*2))
            
            
        if self.check_en_peasant(self.x+1,self.y+d,board,last_move):
            print("+"*50)
            print(self.x,self.y,self.x+1,self.y+d,"\n")
            moves.append((self.x+1,self.y+d))
        if self.check_en_peasant(self.x-1,self.y+d,board,last_move):
            print("+"*50)
            print(self.x,self.y,self.x-1,self.y+d,"\n")
            moves.append((self.x-1,self.y+d))
                
        return moves
    
    def diaPos(self,board):
        moves=[]
        d=DIRECTIONS[self.color] # to decide direction of movement
        if self.checkd(self.x+1,self.y+d,board):
            print(self.x+1,self.y+d,"*")
            moves.append((self.x+1,self.y+d))
        if self.checkd(self.x-1,self.y+d,board):
            print(self.x,self.y,self.x-1,self.y+d,"_")
            moves.append((self.x-1,self.y+d))
        return moves
    
    def setPosition(self, pos):
        self.moved=True
        self.x, self.y = pos
        
    def getPosition(self):
        return [self.x, self.y]
    
    def setEnable(self, val):
        self.enable = val

    def isEnable(self):
        return self.enable
            
            
        