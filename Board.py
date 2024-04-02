import copy
#'p','r','h','b','k','q'
#pawn,rook,knight,bishop,king,queen
class Board:
    check=False
    checkmate=False
    last_move="p66-65"
    board=[['  ','  ','  ','  ','  ','  ','  ','  '],
            ['  ','  ','  ','pb','  ','  ','  ','  '],
            ['  ','  ','  ','  ','pb','  ','pb','  '],
            ['  ','  ','pb','pw','pw','  ','  ','  '],
            ['  ','pb','  ','  ','  ','pb','pw','pb'],
            ['pb','  ','  ','  ','  ','pw','  ','pw'],
            ['pw','pw','pw','  ','  ','  ','  ','  '],
            ['  ','  ','  ','  ','  ','  ','  ','  ']]  
    
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
            print("| "," | ".join(i), " |")
            print("-"*43)
        
            
    @staticmethod
    def is_check_resolved(board):
        return False
    
    @classmethod
    def show_moves(self,moves):
        board_map=copy.deepcopy(self.board)
        for move in moves:
            board_map[move[1]][move[0]]="()"
        self.print(board_map)
        
        
        