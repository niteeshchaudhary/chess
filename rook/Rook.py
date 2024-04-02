from Board import Board
# from Possible_Moves import KingMoves,PawnMoves 
import math
COLORS={'w':'b','b':'w'}
DIRECTIONS={'w':-1,'b':1}

class Rook:
    def __init__(self,x,y,color):
        self.color=color
        self.opcolor=COLORS[color]
        if y==0 or y==7:
            self.moved=False
        else:
            self.moved=True
        self.x=x
        self.y=y
        self.name="r"+color
        self.icon = "♖" if color == "white" else "♜"
        
    def check(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        if Board.board[y][x][1]==self.opcolor or Board.board[y][x]=="  ":
            if not Board.check:
                return True
            else: 
                prev=Board.board[y][x]
                Board.board[y][x]=self.name
                Board.board[self.y][self.x]="  "
                if Board.is_check_resolved():
                    Board.board[y][x]=prev
                    Board.board[self.y][self.x]=self.name
                    return True
                Board.board[self.y][self.x]=self.name
                Board.board[y][x]=prev

        return False
    
    def moveLeft(self,x,y,moves):
        if self.check(x,y):
            moves+=[(x,y)]
            if Board.board[y][x]=="  ":
                self.moveLeft(x-1,y,moves)
                
    def moveRight(self,x,y,moves):
        if self.check(x,y):
            moves+=[(x,y)]
            if Board.board[y][x]=="  ":
                self.moveRight(x+1,y,moves)
    
    def moveUp(self,x,y,moves):
        if self.check(x,y):
            moves+=[(x,y)]
            if Board.board[y][x]=="  ":
                self.moveUp(x,y-1,moves)
    
    def moveDown(self,x,y,moves):
        if self.check(x,y):
            moves+=[(x,y)]
            if Board.board[y][x]=="  ":
                self.moveDown(x,y+1,moves)
        
        
    def initchecks(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
                
    def generate_moves(self)->list:
        moves=[]
        self.moveLeft(self.x-1,self.y,moves)
        self.moveRight(self.x+1,self.y,moves)
        self.moveUp(self.x,self.y-1,moves)
        self.moveDown(self.x,self.y+1,moves)
        return moves
            
            
        