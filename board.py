class Board:
    """
    Creates a representation of a checkers game
    Default is the international version
    Pieces are represented in a list with 25 options
    """
    @staticmethod
    def movePiece(pos, direction, count=1):
        """
        Take a piece position (0-49), a direction to move (UL, UR, LL, or LR)
        and the number of moves.
        Returns the new position of the piece after making [count] number of moves in
        the specified direction. Returns None if the move would take the piece off the board
        """

        # First validate the that the piece can actually move in the desired direction
        if direction[0] == "U":
            # If the direction is up and the piece is at the top row
            if pos // 5 == 0:
                return None
        else:
            # If the direction is down and the piece is at the bottom row
            if pos // 5 == 9:
                return None
        if direction[1] == "R":
            # If the direction is right and the piece is at the right side
            if pos % 10 == 4:
                return None
        else:
            # If the direction is left and the piece is at the left side
            if pos % 10 == 5:
                return None

        # Next actually do the math
        if direction == "UL":
            newPos = (pos - 5) - ((pos // 5) % 2)
        elif direction == "UR":
            newPos = (pos - 4) - ((pos // 5) % 2)
        elif direction == "LL":
            newPos = (pos + 5) - ((pos // 5) % 2)
        else:
            newPos = (pos + 6) - ((pos // 5) % 2)
        return newPos if count == 1 else Board.movePiece(newPos, direction, count-1)

    def __init__(self):
        self._board = [-1] * 20
        self._board.extend([0] * 10)
        self._board.extend([1] * 20)
        self._stack = []
        self._whiteTurn = True
        self._legalMoves = self._calcLegalMoves()

    def getLegalMoves(self):
        return self._legalMoves

    def pushMove(self, move):
        """
        Pushes a given move to the stack if the move is valid
        :param move: tuple
        :return:
        """

    def _movePiece(self, move):
        """
        :param move: tuple(startingPiecePosition, newPiecePosition, [listOfJumpedPieces])
        """
        self._board[move[1]] = self._board[move[0]]
        self._board[move[0]] = 0
        for pos in move[2]:
            self._board[pos] = 0

    # TODO: Add movement forcing
    def _calcLegalMoves(self):
        legalMoves = {}
        for pos in range(len(self._board)):
            if self._whiteTurn and self._board[pos] > 0:
                legalMoves.update({pos: self._getPieceMoves(pos)} if self._getPieceMoves(pos) else {})
            elif not self._whiteTurn and self._board[pos] < 0:
                legalMoves.update({pos: self._getPieceMoves(pos)} if self._getPieceMoves(pos) else {})
        return legalMoves

    def _getPieceMoves(self, pos):
        """
        Returns unvalidated moves from a piece, assumes it's the piece's turn. To get validated moves,
        use getLegalMoves()[piece]
        :param pos: The position of the piece
        :return: Dictionary containing possible moves and the pieces that would be jumped as a result
        """
        if self._board[pos] == 1 or self._board[pos] == 2:
            return self._scanMoves(pos, self._board[pos])

    def _scanMoves(self, startingPos, pieceJumping, jumped=[]):
        """
        Generates all possible moves for a given piece to make from the given starting position
        The starting position doesn't have to be where the piece is at the start of the jump, to
        chain jumps together simply recursively call the function at the post-jump position
        :param startingPos: The position where the piece currently is
        :param pieceJumping: The actual value of the piece (-1 or 1,
        if the piece is a king it should use another function)
        :param jumped: The pieces that have already been jumped in this sequence
        :return: An unvalidated dictionary of possible moves and what they've jumped
        """

        toReturn = {}
        upDirections = ["UL", "UR"]
        downDirections = ["LL", "LR"]

        for direction in upDirections:
            newPos = Board.movePiece(startingPos, direction)
            if newPos is None:
                break

            # The piece on the square we're moving into
            movePiece = self._board[newPos]
            if movePiece == 0 and not jumped and pieceJumping == 1:
                toReturn.update({newPos: []})
            if movePiece != 0 and movePiece != pieceJumping and not (movePiece in jumped):
                # The position we would be at if we jumped over the adjacent piece
                jumpedPos = Board.movePiece(startingPos, direction, 2)
                if jumpedPos is None:
                    break
                if not (jumpedPos is None) and self._board[jumpedPos] == 0:
                    toReturn.update(self._scanMoves(jumpedPos, pieceJumping, jumped+[newPos]))
        for direction in downDirections:
            newPos = Board.movePiece(startingPos, direction)
            if newPos is None:
                break

            # The piece on the square we're moving into

            movePiece = self._board[newPos]
            if movePiece == 0 and not jumped and pieceJumping == -1:
                toReturn.update({newPos: []})
            if movePiece != 0 and movePiece != pieceJumping and not (movePiece in jumped):
                # The position we would be at if we jumped over the adjacent piece
                jumpedPos = Board.movePiece(startingPos, direction, 2)
                if jumpedPos is None:
                    break
                if not (jumpedPos is None) and self._board[jumpedPos] == 0:
                    toReturn.update(self._scanMoves(jumpedPos, pieceJumping, jumped+[newPos]))

        return toReturn

    def __repr__(self):
        toReturn = ""
        isCheckingPiece = False
        for row in range(10):
            rowReturn = ""
            for col in range(10):
                if isCheckingPiece and self._board[(row * 5) + (col // 2)] != 0:
                    piece = self._board[(row * 5) + (col // 2)]
                    rowReturn += (str(piece) if piece < 0 else " " + str(piece))
                else:
                    rowReturn += " ."
                rowReturn += " "
                isCheckingPiece = not isCheckingPiece
            toReturn += rowReturn + "\n"
            isCheckingPiece = not isCheckingPiece
        return toReturn