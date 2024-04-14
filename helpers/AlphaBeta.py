

def minMaxAlphaBeta(position,depth, alpha, beta, isMaxPlayer):

    if depth==0 or position.is_checkmate():
        return -position.evaluate()
    
    if isMaxPlayer:
        maxVal=-1000000
        for child in position:
            myval=minMaxAlphaBeta(child, depth-1,alpha,beta,False)
            maxVal=max(myval,maxVal)
            alpha=max(alpha,myval)
            if beta<=alpha:
                break
        return maxVal
    else:
        minVal=1000000
        for child in position:
            myval=minMaxAlphaBeta(child,depth-1,alpha,beta,True)
            minVal=min(myval,minVal)
            beta=min(beta,myval)
            if beta<=alpha:
                break
        return minVal