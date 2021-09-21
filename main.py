from board import Board
from graphics import Graphics


def validateMoves(val):
    print(Board.movePiece(val, "UL"))
    print(Board.movePiece(val, "UR"))
    print(Board.movePiece(val, "LL"))
    print(Board.movePiece(val, "LR"))


b = Board()
print(b.getLegalMoves())

g = Graphics(b)
g.run()
print(b)
