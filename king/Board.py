import copy
#'p','r','h','b','k','q'
#pawn,rook,knight,bishop,king,queen

class Board:
    check=False
    turn='b'
    checkmate=False
    last_move="k66-65"
    board=[['rbc','  ','  ','  ','kbc','  ','  ','rbc'],
            ['  ','  ','rb','  ','  ','  ','  ','rw'],
            ['  ','  ','  ','rb','  ','  ','pb','  '],
            ['  ','  ','  ','rw','  ','  ','  ','  '],
            ['  ','pb','  ','  ','  ','pb','rw','rb'],
            ['pb','  ','  ','  ','  ','rw','  ','rw'],
            ['rw','rw','rw','  ','  ','  ','  ','  '],
            ['  ','  ','  ','  ','rw','  ','  ','  ']]  
    
    def __init__(self):
        # global check, checkmate, board
        # board=[['  ','  ','  ','  ','  ','  ','  ','pb'],
        #             ['  ','  ','  ','  ','  ','  ','pw','  '],
        #             ['  ','  ','  ','pb','pb','pb','  ','  '],
        #             ['  ','  ','pb','  ','pw','  ','  ','pb'],
        #             ['  ','pb','  ','pw','  ','pb','  ','  '],
        #             ['pb','  ','  ','pb','  ','pw','  ','pw'],
        #             ['pw','pw','pw','  ','  ','  ','  ','  '],
        #             ['  ','  ','  ','  ','  ','  ','  ','  ']]
        # check=False
        # checkmate=False
        pass
    
    @staticmethod
    def print(board):
        for i in board:
            print(end="| ")
            for j in i:
                print(j,end= " | ")
            print("\n","-"*43)
    
    @classmethod
    def printb(self):
        for i in self.board:
            print(end="| ")
            for j in i:
                print(j,end= " | ")
            print("\n","-"*43)
            
    @staticmethod
    def is_check_resolved():   
        return True
    
    @classmethod
    def show_moves(self,moves):
        board_map=copy.deepcopy(self.board)
        for move in moves:
            k=f"{board_map[move[1]][move[0]]}"
            board_map[move[1]][move[0]]=f"({k.strip()})"
        self.print(board_map)
        
    @classmethod
    def check_check(self):
        x,y=-1,-1
        for xi,i in enumerate(self.board):
            for xj,j in enumerate(i):
                if j!="  " and j.name=="k"+self.turn:
                    x=xj
                    y=xi
                    break
            if x!=-1:
                break
        self.evaluate_board(x,y) 
        
    @classmethod
    def is_check_resolvable(self,moves):
        return True
    
    @classmethod
    def check_checkmate(self):
        if self.check_check():
            if self.is_check_resolvable():
                return False
            else:
                return True  
        else:
            return False
        
    @classmethod
    def evaluate_board(self,x,y):
        moves=[]
        for xi,i in enumerate(self.board):
            for xj,j in enumerate(i):
                if j!="  " and j.color!=self.turn:
                    moves+=j.generate_possible_moves(Board.board)
                    if (x,y) in moves:
                        self.check=True  
                        return True          
        return False
        
        
        