from board import Board


def validateMoves(val):
    print(Board.movePiece(val, "UL"))
    print(Board.movePiece(val, "UR"))
    print(Board.movePiece(val, "LL"))
    print(Board.movePiece(val, "LR"))


b = Board()
b.pushMove((30, 25, []))
b.pushMove((16, 20, []))
print(b)
print(b.getLegalMoves())
