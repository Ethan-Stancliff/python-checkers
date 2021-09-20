from board import Board
from graphics import Graphics


def validateMoves(val):
    print(Board.movePiece(val, "UL"))
    print(Board.movePiece(val, "UR"))
    print(Board.movePiece(val, "LL"))
    print(Board.movePiece(val, "LR"))


b = Board()
b.push((30, 25, []))

g = Graphics(b)
g.run()
print(b)
