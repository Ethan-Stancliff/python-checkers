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
        return newPos if count == 1 else Board.movePiece(newPos, direction, count - 1)

    def __init__(self, board=[]):
        if not board:
            self._board = [-1] * 20
            self._board.extend([0] * 10)
            self._board.extend([1] * 20)
        else:
            self._board = board
        self._stack = []
        self._whiteTurn = True
        self._legalMoves = self._calcLegalMoves()

    def getLegalMoves(self):
        return self._legalMoves

    def push(self, move):
        """
        Pushes a given move to the stack if the move is valid
        :param move: tuple(startingPiecePosition, newPiecePosition, [listOfJumpedPieces])
        """

        # TODO: Validate move
        # The stack sequentially stores moves made to the board, format:
        # [tuple(startingPiecePosition, newPiecePosition, {deletedPiecePos: deletedPieceValues})]
        self._stack.append((
            move[0],
            move[1],
            dict(zip(move[2], [self._board[i] for i in move[2]]))
        ))

        self._movePiece(move)
        self._whiteTurn = not self._whiteTurn
        self._legalMoves = self._calcLegalMoves()

    def pop(self):
        """Unmakes the most recent move made"""
        lastMove = self._stack[-1]
        if not lastMove:
            return
        self._unmakeMove(lastMove)
        self._whiteTurn = not self._whiteTurn
        self._legalMoves = self._calcLegalMoves()

    def _movePiece(self, move):
        """
        :param move: tuple(startingPiecePosition, newPiecePosition, [listOfJumpedPieces])
        """
        self._board[move[1]] = self._board[move[0]]
        self._board[move[0]] = 0
        for pos in move[2]:
            self._board[pos] = 0

    def _unmakeMove(self, move):
        """Takes a move and unmakes it
        :param move: tuple(startingPiecePosition, newPiecePosition, {deletedPiecePos: deletedPieceValue})
        """
        self._board[move[0]] = self._board[move[1]]
        self._board[move[1]] = 0
        for pos in move[2]:
            self._board[pos] = move[2][pos]

    # TODO: Add movement forcing
    def _calcLegalMoves(self):
        legalMoves = {}
        for pos in range(len(self._board)):
            if self._whiteTurn and self._board[pos] > 0:
                legalMoves.update({pos: self._getPieceMoves(pos)} if self._getPieceMoves(pos) else {})
            elif not self._whiteTurn and self._board[pos] < 0:
                legalMoves.update({pos: self._getPieceMoves(pos)} if self._getPieceMoves(pos) else {})

        # Checks to see if there are any jumps possible, if so, forces them
        longestPossibleJump = 0
        for piece in legalMoves:
            for move in legalMoves[piece]:
                if len(legalMoves[piece][move]) > longestPossibleJump:
                    longestPossibleJump = len(legalMoves[piece][move])

        if longestPossibleJump > 0:
            for piece in legalMoves.copy():
                for move in legalMoves[piece].copy():
                    if len(legalMoves[piece][move]) < longestPossibleJump:
                        legalMoves[piece].pop(move)
                if len(legalMoves[piece]) == 0:
                    legalMoves.pop(piece)
        return legalMoves

    def _getPieceMoves(self, pos):
        """
        Returns unvalidated moves from a piece, assumes it's the piece's turn. To get validated moves,
        use getLegalMoves()[piece]
        :param pos: The position of the piece
        :return: Dictionary containing possible moves and the pieces that would be jumped as a result
        """
        if self._board[pos] == 1 or self._board[pos] == -1:
            return self._scanMoves(pos, self._board[pos])
        elif self._board[pos] == 2 or self._board[pos] == -2:
            return self._scanPromotedMoves(pos, self._board[pos])

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
                continue

            # The piece on the square we're moving into
            movePiece = self._board[newPos]
            if movePiece == 0 and not jumped and pieceJumping == 1:
                toReturn.update({newPos: []})
            if movePiece != 0 and movePiece != pieceJumping and not (movePiece in jumped):
                # The position we would be at if we jumped over the adjacent piece
                jumpedPos = Board.movePiece(startingPos, direction, 2)
                if jumpedPos is None:
                    continue
                if self._board[jumpedPos] == 0:
                    toReturn.update({jumpedPos: jumped + [newPos]})
                    toReturn.update(self._scanMoves(jumpedPos, pieceJumping, jumped + [newPos]))
        for direction in downDirections:
            newPos = Board.movePiece(startingPos, direction)
            if newPos is None:
                continue

            # The piece on the square we're moving into

            movePiece = self._board[newPos]
            if movePiece == 0 and not jumped and pieceJumping == -1:
                toReturn.update({newPos: []})
            if movePiece != 0 and movePiece != pieceJumping and not (movePiece in jumped):
                # The position we would be at if we jumped over the adjacent piece
                jumpedPos = Board.movePiece(startingPos, direction, 2)
                if jumpedPos is None:
                    continue
                if not (jumpedPos is None) and self._board[jumpedPos] == 0:
                    toReturn.update({jumpedPos: jumped + [newPos]})
                    toReturn.update(self._scanMoves(jumpedPos, pieceJumping, jumped + [newPos]))

        return toReturn

    def _scanPromotedMoves(self, startingPos, pieceJumping, jumped=[]):
        directions = ["UL", "UR", "LL", "LR"]
        toReturn = {}

        for direction in directions:
            foundEnemy = None
            beforeJumped = {}
            afterJumped = {}
            newPos = Board.movePiece(startingPos, direction)

            while newPos is not None:
                newPiece = self._board[newPos]
                if newPiece == 0:
                    if not foundEnemy and not jumped:
                        beforeJumped.update({newPos: []})
                    if foundEnemy and newPos not in jumped:
                        afterJumped.update({newPos: [foundEnemy]})
                        afterJumped.update(self._scanPromotedMoves(newPos, pieceJumping, [foundEnemy] + jumped))
                elif (newPiece >= 1) == (pieceJumping >= 1):
                    break
                else:
                    if not foundEnemy and newPos not in jumped:
                        foundEnemy = newPos
                    else:
                        break
                newPos = Board.movePiece(newPos, direction)
            if foundEnemy and afterJumped:
                toReturn.update(afterJumped)
            elif beforeJumped:
                toReturn.update(beforeJumped)

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
