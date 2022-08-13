
'''
Chess player
'''
import chessPieces
from string import ascii_lowercase

class chessPlayer:
    def __init__(self, colour: int) -> None:
        self._colour=colour

        startY=1
        if colour==-1:
            startY=8

        self._pieces=[chessPieces.rook(self._colour, f"a{startY}"),
                    chessPieces.knight(self._colour, f"b{startY}"),
                    chessPieces.bishop(self._colour,  f"c{startY}"),
                    chessPieces.queen(self._colour,  f"d{startY}"),
                    chessPieces.king(self._colour,  f"e{startY}"),
                    chessPieces.bishop(self._colour,  f"f{startY}"),
                    chessPieces.knight(self._colour, f"g{startY}"),
                    chessPieces.rook(self._colour, f"h{startY}")]

        for iSquare in ascii_lowercase[:8]:
            self._pieces.append(chessPieces.pawn(self._colour, f"{iSquare}{startY+self._colour}"))
    
    def takePieceFromSquare(self, pieceSquare: str)->int:
        for piece in self._pieces:
            if piece.currentSquare==pieceSquare:
                piece.currentSquare='Taken'
                return piece.value
        return 0

    def scanAllowedSquares(self, enemyPieces: list)->None:
        for iPiece, piece in enumerate(self._pieces):
            friendlyPieces: list=self._pieces[:iPiece]+self._pieces[iPiece+1:]
            piece.checkBoardState(friendlyPieces, enemyPieces)
    
    def ProposeMove(self, pieceIndex: int, proposedMove: str)->bool:
        return self._pieces[pieceIndex].movePiece(proposedMove)
