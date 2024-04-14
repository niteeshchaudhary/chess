# def minMax(position,depth,alpha,beta,maximizingPlayer):
#     if depth==0 or position.is_checkmate():
#         return -position.evaluate_board()
#     if maximizingPlayer:
#         maxEval=float('-inf')
#         for move in position.legal_moves:
#             position.push(move)
#             eval=minMax(position,depth-1,alpha,beta,False)
#             position.pop()
#             maxEval=max(maxEval,eval)
#             alpha=max(alpha,eval)
#             if beta<=alpha:
#                 break
#         return maxEval
#     else:
#         minEval=float('inf')
#         for move in position.legal_moves:
#             position.push(move)
#             eval=minMax(position,depth-1,alpha,beta,True)
#             position.pop()
#             minEval=min(minEval,eval)
#             beta=min(beta,eval)
#             if beta<=alpha:
#                 break
#         return minEval

def minMax(position, depth, isMaxPlayer):
    if depth==0 or position.is_checkmate():
        return -position.evaluate_board()

    if isMaxPlayer:
        maxscore=-10000000
        for child in position:
            myscore=minMax(child,depth-1,False)
            maxscore=max(maxscore,myscore)
        return maxscore
    else:
        minscore=+1000000
        for child in position:
            myscore=minMax(position,depth-1,True)
            minscore=min(minscore,myscore)
        return minscore

