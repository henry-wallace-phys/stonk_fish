'''
Classes that enable chess within python including piece scoring (Hopefully better than attempt 1!)
'''
from ast import Pass
from logging import raiseExceptions
from string import ascii_lowercase
from itertools import product


class chessPiece:
    '''
    What do we want : 
     1. Piece colour, scoring and type
     2. Each piece should know which pieces are in the way and which squares it can move to
     3. King should know if it's in check
     4. Pawn needs to be able to do its unique moves (or brick on Pipi)
     5. Castling
    '''

    def __init__(self, colour: int, startSquare: str, value: int) -> None:
        '''
        Sets up chess piece 
        colour = +-1 (-1=Black, +1 = White)
        value = piece value
        '''
        self._colour=colour
        self._currentSquare=startSquare
        self._value=value
        self._pieceType='NaN'
        self._boardcols={L:iL for iL, L in enumerate(ascii_lowercase[:8])} #Useful since it's annoying to deal with letters
     
     
        self._friendlyPieces=[]
        self._enemypieces=[]
        self._blockingSquares=[]

        self._isTaken=False
 

        self._positiveline = lambda x : x
        self._negativeline = lambda x : -x

        self._totalmoves=0


        self._friendlyPiecesOnRow=[]
        self._friendlyPiecesOnCol =[]

        self._takeablePiecesOnRow=[]
        self._takeablePiecesOnCol=[]

        self._friendlyPiecesOnPosDiag=[]
        self._friendlyPiecesOnNegDiag=[]

        self._takeablePiecesOnPosDiag=[]
        self._takeablePiecesOnNegDiag=[]
        self._lastMoved=False



    @property
    def currentSquare(self):
        return self._currentSquare

    @property
    def colour(self):
        return self._colour

    @property
    def pieceType(self):
        return self._pieceType

    @property
    def value(self):
        return self._value

    @property 
    def totalMoves(self):
        return self._totalmoves

    def setLastMoved(self, val: bool):
        self._lastMoved=val

    @property
    def lastMoved(self):
        return self._lastMoved

    def checkBoardState(self, friendlyPieces: list, enemyPieces: list)->None:
        #Let's get a quick scan of everything done here
        self._friendlyPieces=friendlyPieces
        self._enemypieces=enemyPieces

        self._friendlyPiecesOnRow=[sq for sq in friendlyPieces if sq.currentSquare[0]==self._currentSquare[0]]
        self._friendlyPiecesOnCol=[sq for sq in friendlyPieces if sq.currentSquare[1]==self._currentSquare[1]]

        self._takeablePiecesOnRow=[sq for sq in enemyPieces if sq.currentSquare[0]==self._currentSquare[0]]
        self._takeablePiecesOnCol=[sq for sq in enemyPieces if sq[1]==self._currentSquare[1]]

        pdiagsq, ndiagsq=self.getDiagMoves()
        self._friendlyPiecesOnPosDiag=[sq for sq in friendlyPieces if sq.currentSquare in pdiagsq]
        self._friendlyPiecesOnNegDiag=[sq for sq in friendlyPieces if sq.currentSquare in ndiagsq]

        self._takeablePiecesOnPosDiag=[sq for sq in enemyPieces if sq.currentSquare in pdiagsq]
        self._takeablePiecesOnNegDiag=[sq for sq in enemyPieces if sq.currentSquare in ndiagsq]

    def getDiagMoves(self):
        xindex=self._boardcols[self._currentSquare[0]]
        yindex=int(self._currentSquare[1])

        self._positiveline = lambda x : x+(yindex-xindex)
        self._negativeline = lambda x : -x+(yindex-xindex)

        posdiagMoves=[f"{list(self._boardcols.values())[lX]}{self._positiveline(lX)}" for lX in range(1,9) if 0<self._positiveline(lX)<9]
        negativediagMoves=[f"{list(self._boardcols.values())[lX]}{self._positiveline(lX)}" for lX in range(1,9) if 0<self._negativeline(lX)<9]

        return posdiagMoves, negativediagMoves
    
    def getLinearMoves(self):        
        verticleMoves=[f"{self._currentSquare[0]}{lY}" for lY in range(1,9)]
        horizontalMoves=[f"{list(self._boardcols.values())[lX]}{self._currentSquare[1]}" for lX in range(1,9)]
        return verticleMoves, horizontalMoves

    def setNewSquare(self, newSquare: str)->None:
        self._currentSquare=newSquare

    def takePiece(self):
        self._isTaken=True

    def getLegalLinearMoves(self):
        vertarray=self._friendlyPiecesOnRow+self._takeablePiecesOnRow
        horarray=self._friendlyPiecesOnCol+self._takeablePiecesOnCol

        uparray=[piece for piece in vertarray if int(piece.currentSquare[1])>int(self.currentSquare[1])]
        uppiece=self.getClosestPiece(uparray)

        downarray=[piece for piece in vertarray if int(piece.currentSquare[1])<int(self.currentSquare[1])]
        downpiece=self.getClosestPiece(downarray)

        leftarray=[piece for piece in horarray if self._boardcols[piece.currentSquare[0]]<self._boardcols[self.currentSquare[0]]]
        leftpiece=self.getClosestPiece(leftarray)

        rightarray=[piece for piece in horarray if self._boardcols[piece.currentSquare[0]]>self._boardcols[self.currentSquare[0]]]
        rightpiece=self.getClosestPiece(rightarray)

        self._blockingSquares.append([uppiece,downpiece,leftpiece,rightpiece])

    def getLegalDiagonalMoves(self):
        posdiagarray=self._friendlyPiecesOnPosDiag+self._takeablePiecesOnPosDiag

        lhposarr=[piece for piece in posdiagarray if int(piece.currentSquare[1])<int(self.currentSquare[1])]
        lhpospiece=self.getClosestPiece(lhposarr)
        
        rhposarr=[piece for piece in posdiagarray if int(piece.currentSquare[1])>int(self.currentSquare[1])]
        rhpospiece=self.getClosestPiece(rhposarr)

        negdiagarray=self._friendlyPiecesOnNegDiag+self._takeablePiecesOnNegDiag

        lhnegarr=[piece for piece in negdiagarray if int(piece.currentSquare[1])>int(self.currentSquare[1])]
        lhnegpiece=self.getClosestPiece(lhnegarr)

        rhnegarr=[piece for piece in negdiagarray if int(piece.currentSquare[1])<int(self.currentSquare[1])]
        rhnegpiece=self.getClosestPiece(rhnegarr)

        self._blockingSquares.extend([lhpospiece, rhpospiece, lhnegpiece, rhnegpiece])

    def getClosestPiece(self, inarr):
        closestpiece=None
        dist=999
        for piece in inarr:
            iDist=abs(int(piece.currentSquare[1])-int(self._currentSquare[1]))
            if iDist<dist:
                closestpiece=piece
                dist=iDist
        return closestpiece

    def moveHorizontal(self, proposedSquare)->bool:
        if proposedSquare[0]!=self._currentSquare[0] or proposedSquare[1]!=self._currentSquare[1]:
            return False
        
        if proposedSquare==self._currentSquare:
            return False

        self._blockingSquares=[]
        self.getLegalLinearMoves()
        xcoord=self._boardcols[proposedSquare[0]]
        ycoord=int(proposedSquare[1])

        uplimit=int(self._blockingSquares[0].currentSquare[1])
        downlimit=int(self._blockingSquares[1].currentSquare[1])

        leftlimit=self._boardcols[self._blockingSquares[2].currentSquare[0]]
        rightlimit=self._boardcols[self._blockingSquares[3].currentSquare[0]]

        havemoved=False

        if ycoord<=uplimit:
            if ycoord==uplimit and self._blockingSquares[0].colour!=self._colour:
                self._currentSquare=self._blockingSquares[0].currentSquare
                havemoved=True

        elif ycoord >= downlimit:
            if ycoord==downlimit and self._blockingSquares[1].colour!=self._colour:
                havemoved=True

        elif xcoord>=leftlimit:
            if xcoord==leftlimit and self._blockingSquares[2].colour!=self._colour:
                havemoved=True

        elif xcoord>=rightlimit:
            if xcoord==rightlimit and self._blockingSquares[3].colour!=self._colour:
                havemoved=True

        else:
            havemoved=True

        return havemoved



    def moveDiagonal(self, proposedSquare: str)->bool:
        positivearr,negativerr = self.getDiagMoves()
        allMoves=positivearr+negativerr
        
        if proposedSquare not in allMoves or proposedSquare==self._currentSquare:
            return False

        self._blockingSquares=[]
        self.getLegalDiagonalMoves()
        ycoord=int(proposedSquare[1])
        
        lhposlimit=int(self._blockingSquares[0].currentSquare[1])
        rhposlimit=int(self._blockingSquares[1].currentSquare[1])

        lhneglimit=int(self._blockingSquares[2].currentSquare[1])
        rhneglimit=int(self._blockingSquares[3].currentSquare[1])

        havemoved=False

        if ycoord>=lhposlimit:
            if ycoord==lhposlimit and self._blockingSquares[0].colour!=self._colour:
                havemoved=True
        elif ycoord<=rhposlimit:
            if ycoord==rhposlimit and self._blockingSquares[1].colour!=self._colour:
                havemoved=True
        elif ycoord<=lhneglimit:
            if ycoord==lhneglimit and self._blockingSquares[2].colour!=self._colour:
                havemoved=True
        elif ycoord>=rhneglimit:
            if ycoord==rhneglimit and self._blockingSquares[3].colour!=self._colour:
                havemoved=True
        else:
            havemoved=True
        return havemoved
        


#####################

class rook(chessPiece):
    def __init__(self, colour: int, startSquare: str) -> None:
        super().__init__(colour, startSquare, value=5)
        self._pieceType='R'

    def checkMoveLegal(self, proposedStep):
        return self.moveHorizontal(proposedStep)

    def movePiece(self, proposedStep):
        move = self.checkMoveLegal(proposedStep)
        if move:
            self._totalmoves+=1
            self._currentSquare=proposedStep
        return move

class bishop(chessPiece):
    def __init__(self, colour: int, startSquare: str) -> None:
        super().__init__(colour, startSquare, 3)
        self._pieceType='B'

    def checkMoveLegal(self, proposedStep):
        return self.moveDiagonal(proposedStep)

    def movePiece(self, proposedStep):
        move = self.checkMoveLegal(proposedStep)
        if move:
            self._totalmoves+=1
            self._currentSquare=proposedStep
        return move

class queen(chessPiece):
    def __init__(self, colour: int, startSquare: str) -> None:
        super().__init__(colour, startSquare, 9)
        self._pieceType='Q'

    def checkMoveLegal(self, proposedStep):
        move=False
        move=self.moveDiagonal(proposedStep)
        if not move:
            self.moveHorizontal(proposedStep)
        return move

    def movePiece(self, proposedStep):
        move = self.checkMoveLegal(proposedStep)
        if move:
            self._totalmoves+=1
            self._currentSquare=proposedStep
        return move

class king(chessPiece):
    def __init__(self, colour: int, startSquare: str) -> None:
        super().__init__(colour, startSquare, 1000)
        self._isInCheck=False
        self.hasCastled=False
        self._pieceType='K'

    def checkMoveLegal(self, proposedStep):
        proposedX=self._boardcols[proposedStep[0]]
        currX=self._boardcols[self._currentSquare[0]]

        proposedY=int(proposedStep[1])
        currY=int(self._currentSquare[1])

        if abs(proposedX-currX)>1 or abs(proposedY-currY)>1:
            if self._totalmoves==0 and abs(proposedY-currY)==0 and abs(proposedX-currX)==2:
                self.getLegalLinearMoves()
                crossingpoint=list(self._boardcols.values())[int((proposedX+currX)/2)]
                for enemy in self._enemypieces:
                    if crossingpoint in enemy.checkMoveLegal(f"{crossingpoint}{proposedY}"):
                        return False
                for i in [2,3]:
                    if self._blockingSquares[i].pieceType=='R' and self._blockingSquares[i].totalMoves==0:
                        self._totalmoves+=1
                        self._hasCastled=True
                        return True

        move=False
        move=self.moveDiagonal(proposedStep)
        if not move:
            self.moveHorizontal(proposedStep)
        return move
        
    def movePiece(self, proposedStep):
        move = self.checkMoveLegal(proposedStep)
        if move:
            self._totalmoves+=1
            self._currentSquare=proposedStep
        return move

class knight(chessPiece):
    def __init__(self, colour: int, startSquare: str) -> None:
        super().__init__(colour, startSquare, 2)
        self._pieceType='N'


    def movePiece(self, proposedStep):
        '''
        How does the horsey move
        '''
        move = self.checkMoveLegal(proposedStep)
        if move:
            self._totalmoves+=1
            self._currentSquare=proposedStep
        return move

    def checkMoveLegal(self, proposedStep)->bool:

        xMoves = [self._boardcols[self._currentSquare[0]]+dx for dx in [-1,1, -2, 2]]
        yMoves = [int(self._currentSquare[1])+dy for dy in [-1, 1, -2, 2]]

        vertmoves=[m for m in product(xMoves[0:2],yMoves[2:]) if 0<m[0]<9 and 0<m[1]<9] #Up +-2 along +-1
        hormoves=[m for m in product(xMoves[2:], yMoves[:2]) if 0<m[0]<9 and 0<m[1]<9]

        
        stepcoord=(self._boardcols[proposedStep[0]], int(proposedStep[1]))
        if stepcoord not in vertmoves+hormoves:
            return False

        for friendly in self._friendlyPieces:
            if friendly.currentSquare==proposedStep:
                return False

        return True

class pawn(chessPiece):
    def __init__(self, colour: int, startSquare: str) -> None:
        super().__init__(colour, startSquare, 1)
        self._pieceType='p'

    def checkLegalMoves(self, proposedStep):
        currentXcoord=self._boardcols[self._currentSquare[0]]
        proposedXcoord=self._boardcols[proposedStep[0]]

        currentYcoord=int(self._currentSquare[1])
        proposedYcoord=int(proposedStep[1])

        if proposedXcoord==currentXcoord and proposedYcoord==proposedYcoord+1*self._colour:
            return self.moveHorizontal(proposedStep)

        elif proposedXcoord==currentXcoord and proposedYcoord==currentYcoord+2*self._colour and self._totalmoves==0:
            return self.moveHorizontal(proposedStep)
        elif abs(proposedXcoord-currentXcoord)==1 and proposedYcoord==currentYcoord+2*self._colour:
            return True
        elif self.canDoEnPassant(proposedStep):
            return True

        return False
        


    def canDoEnPassant(self, proposedStep):
        if abs(self._boardcols[proposedStep[0]]-self._boardcols[self._currentSquare])!=1 or int(proposedStep[1])!=int(self._currentSquare)+1*self._colour:
            return 1
        for piece in self._enemypieces:
            if piece.pieceType=='p' and piece.totalMoves==1 and piece.lastMoved==True:
                pieceY=int(piece.currentSquare[1])
                pieceX=self._boardcols[piece.currentSquare[0]]
                if pieceY==int(proposedStep[1]) and abs(pieceX-self._boardcols[proposedStep[0]])==0 and pieceY==5 or pieceY==4:
#                   print("GOOGLE EN PASSANT")
                    return True
        return False

                