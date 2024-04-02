COLORS={'w':'b','b':'w'}
DIRECTIONS={'w':-1,'b':1}

class KingMoves:
    
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
        
    def possible_check(self,x,y,board):
        if x<0 or y<0 or x>7 or y>7:
            return False
        if board[y][x][1]==self.opcolor or board[y][x]=="  ":
            return True
            
        return False
    
    def generate_possible_moves(self,board)->list:
        moves=[]
        if self.possible_check(self.x+1,self.y+1,board):
            # print(self.x+1,self.y+1)
            moves.append((self.x+1,self.y+1))
        if self.possible_check(self.x,self.y+1,board):
            # print(self.x,self.y+1)
            moves.append((self.x,self.y+1))
        if self.possible_check(self.x-1,self.y+1,board):
            # print(self.x-1,self.y+1)
            moves.append((self.x-1,self.y+1))
            
        if self.possible_check(self.x+1,self.y,board):
            # print(self.x+1,self.y)
            moves.append((self.x+1,self.y))
        if self.possible_check(self.x-1,self.y,board):
            # print(self.x-1,self.y)
            moves.append((self.x-1,self.y))
            
        if self.possible_check(self.x+1,self.y-1,board):
            # print(self.x+1,self.y-1)
            moves.append((self.x+1,self.y-1))
        if self.possible_check(self.x,self.y-1,board):
            # print(self.x,self.y-1)
            moves.append((self.x,self.y-1))
        if self.possible_check(self.x-1,self.y-1,board):
            # print(self.x-1,self.y-1)
            moves.append((self.x-1,self.y-1))
                
        return moves
    
class PawnMoves:
    
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
    
    def checkd(self,x,y,board):
        if x<0 or y<0 or x>7 or y>7:
            return False
        if board[y][x][1]==self.opcolor:
            return True
        return False
    
    
    def generate_possible_moves(self,board)->list:
        moves=[]
        d=DIRECTIONS[self.color] # to decide direction of movement
        if self.checkd(self.x+1,self.y+d,board):
            print(self.x+1,self.y+d,"*")
            moves.append((self.x+1,self.y+d))
        if self.checkd(self.x-1,self.y+d,board):
            print(self.x,self.y,self.x-1,self.y+d,"_")
            moves.append((self.x-1,self.y+d))
                
        return moves
    
class RookMoves:
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
        
    def check(self,x,y,board):
        if x<0 or y<0 or x>7 or y>7:
            return False
        
        if board[y][x][1]==self.opcolor or board[y][x]=="  ":
            return True
            
        return False
    
    def moveLeft(self,x,y,moves,board):
        if self.check(x,y,board):
            moves+=[(x,y)]
            if board[y][x]=="  ":
                self.moveLeft(x-1,y,moves,board)
                
    def moveRight(self,x,y,moves,board):
        if self.check(x,y,board):
            moves+=[(x,y)]
            if board[y][x]=="  ":
                self.moveRight(x+1,y,moves,board)
    
    def moveUp(self,x,y,moves,board):
        if self.check(x,y,board):
            moves+=[(x,y)]
            if board[y][x]=="  ":
                self.moveUp(x,y-1,moves,board)
    
    def moveDown(self,x,y,moves,board):
        if self.check(x,y,board):
            moves+=[(x,y)]
            if board[y][x]=="  ":
                self.moveDown(x,y+1,moves,board)
        
        
    def initchecks(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return False
                
    def generate_possible_moves(self,board)->list:
        moves=[]
        self.moveLeft(self.x-1,self.y,moves,board)
        self.moveRight(self.x+1,self.y,moves,board)
        self.moveUp(self.x,self.y-1,moves,board)
        self.moveDown(self.x,self.y+1,moves,board)
        return moves