from pyplasm import *
import itertools

# This approach works but maybe it's better to generate three list of indices:
#  - One made by the indices of the "horizontal frame pieces"
#  - One made by the indices of the "vertical frame pieces"
#  - One made by the indices of the other pieces

def window(X,Y,Z,occupancy):
    
    def sum(a):
        def s(b):
            return a+b
        return s
    
    def genModel(dx,dy,dz):
        cartesianProd = itertools.product(range(len(X)-1),range(len(Y)-1),range(len(Z)-1))
        
        # The three lists
        pieces = [(i,j,k) for (i,j,k) in cartesianProd if occupancy[i][j][k]]
        hPieces = [(i,j,k) for (i,j,k) in pieces if (Y[j+1]-Y[j]) > 0.05 and (X[i+1]-X[i]) / (Y[j+1]-Y[j]) > 2]
        vPieces = [(i,j,k) for (i,j,k) in pieces if (X[i+1]-X[i]) > 0.05 and (X[i+1]-X[i]) / (Y[j+1]-Y[j]) < 0.5]
        
        # Now I want to find a set of X quote indices of horizontal frame pieces.
        hPiecesIndexes = list(set([i for (i,_,_) in hPieces]))
        vPiecesIndexes = list(set([j for (_,j,_) in vPieces]))
        
        # Now the length of these pieces
        hPiecesLength = SUM([X[i+1]-X[i] for i in hPiecesIndexes])
        vPiecesLength = SUM([Y[j+1]-Y[j] for j in vPiecesIndexes])
        
        # Now the length that the frame pieces must be
        hPiecesDesiredLength = (dx - X[-1] + hPiecesLength) / len(hPiecesIndexes)
        vPiecesDesiredLength = (dy - Y[-1] + vPiecesLength) / len(vPiecesIndexes)
        
        # Now let's generate the new quote vectors
        finalX = X[:]
        finalY = Y[:]
        
        for i in hPiecesIndexes:
            finalX = finalX[:i+1] + AA(sum(hPiecesDesiredLength-(finalX[i+1]-finalX[i])))(finalX[i+1:])
        
        for j in vPiecesIndexes:
            finalY = finalY[:j+1] + AA(sum(vPiecesDesiredLength-(finalY[j+1]-finalY[j])))(finalY[j+1:])
        
        return STRUCT([
            T([1,2,3])([finalX[i],finalY[j],Z[k]])(
                CUBOID([
                        finalX[i+1]-finalX[i],
                        finalY[j+1]-finalY[j],
                        Z[k+1]-Z[k]
                    ])
            )
            for [i,j,k] in pieces
        ])
        
    
    return genModel
