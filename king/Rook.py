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
        
    def __str__(self):
        return self.name
        
    def check(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        if Board.board[y][x]=="  " or Board.board[y][x].color==self.opcolor:
            if not Board.check:
                return True
            else: 
                prev=Board.board[y][x]
                Board.board[y][x]=self
                Board.board[self.y][self.x]="  "
                if Board.is_check_resolved():
                    Board.board[y][x]=prev
                    Board.board[self.y][self.x]=self
                    return True
                Board.board[self.y][self.x]=self
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
    
    
    def possible_check(self,x,y,board):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        if board[y][x]=="  " or board[y][x].color==self.opcolor:
            return True
            
        return False
    
    def pmoveLeft(self,x,y,moves,board):
        if self.possible_check(x,y,board):
            moves+=[(x,y)]
            if board[y][x]=="  ":
                self.pmoveLeft(x-1,y,moves,board)
                
    def pmoveRight(self,x,y,moves,board):
        if self.possible_check(x,y,board):
            moves+=[(x,y)]
            if board[y][x]=="  ":
                self.pmoveRight(x+1,y,moves,board)
    
    def pmoveUp(self,x,y,moves,board):
        if self.possible_check(x,y,board):
            moves+=[(x,y)]
            if board[y][x]=="  ":
                self.pmoveUp(x,y-1,moves,board)
    
    def pmoveDown(self,x,y,moves,board):
        if self.possible_check(x,y,board):
            moves+=[(x,y)]
            if board[y][x]=="  ":
                self.pmoveDown(x,y+1,moves,board)
                
    def generate_possible_moves(self,board)->list:
        moves=[]
        self.pmoveLeft(self.x-1,self.y,moves,board)
        self.pmoveRight(self.x+1,self.y,moves,board)
        self.pmoveUp(self.x,self.y-1,moves,board)
        self.pmoveDown(self.x,self.y+1,moves,board)
        return moves
            
            
        