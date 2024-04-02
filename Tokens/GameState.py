class GameState:
    board=[]
    check=False
    check_mate=False
    last_move="None"
    @staticmethod
    def setState(bd,ck,ckm,lm):
        global board,check,check_mate,last_move
        board=bd
        check=ck
        check_mate=ckm
        last_move=lm
        
    def is_check_resolved(point):
        print("***",point) 
            
    