
import random
class RandomMove:

    def __init__(self):
        pass

    def choose_piece(self,position):
        options=['queen']*30+['rook']*15+['bishop']*5+['knight']*10
        return random.choice(options)

    
    def getNextMove(self,board,moves):
        keys=list(moves.keys())
        cur=random.choice(keys)
        next_position=random.choice(moves[cur])
        current_position=[cur//10,cur%10]
        return[current_position,next_position]

