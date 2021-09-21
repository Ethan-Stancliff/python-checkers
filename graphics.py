import pygame


class Graphics:
    _defaults = {
        "SQUARE_SIZE": 75,
        "LIGHT_SQUARE_COLOR": (170, 170, 170),
        "DARK_SQUARE_COLOR": (60, 60, 60),
        "PIECE_SIZE": 27,
        "WHITE_PIECE_COLOR": (230, 230, 230),
        "RED_PIECE_COLOR": (200, 0, 0),
        "PADDING_SIZE": 4,
        "PADDING_COLOR_WHITE": (96, 96, 96),
        "PADDING_COLOR_RED": (128, 96, 96),
        "SELECTED_COLOR": (0, 0, 255),
        "SELECTED_SIZE": 15
    }

    def __init__(self, board, **kwargs):
        self.board = board
        for key in Graphics._defaults:
            self.__dict__.update({key: kwargs[key] if key in kwargs else Graphics._defaults[key]})
        self.win = pygame.display.set_mode((self.SQUARE_SIZE * 10, self.SQUARE_SIZE * 10))
        self.clock = pygame.time.Clock()
        self.selectedPiece = None
        self.legalMoves = board.getLegalMoves()

    def run(self):
        run = True
        self._updateBoard()
        while run:
            self.clock.tick(30)

            # TODO: Check Winner

            # TODO: Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handleMouseInput(pygame.mouse.get_pos())

        pygame.quit()

    def _updateBoard(self):
        self._drawBoardSquares()
        self._drawPieces()
        self._drawSelected()

        pygame.display.update()

    def _drawSelected(self):
        if self.selectedPiece is None:
            return
        if self.selectedPiece in self.legalMoves:
            for key in self.legalMoves[self.selectedPiece]:
                row = key // 5
                col = (key % 5) * 2
                col += 1 if row % 2 == 0 else 0
                pygame.draw.circle(
                    self.win,
                    self.SELECTED_COLOR,
                    (self.SQUARE_SIZE * col + (self.SQUARE_SIZE // 2), self.SQUARE_SIZE * row + (self.SQUARE_SIZE // 2)),
                    self.SELECTED_SIZE)

    def _drawBoardSquares(self):
        self.win.fill(self.DARK_SQUARE_COLOR)
        for row in range(10):
            for col in range(row % 2, 10, 2):
                pygame.draw.rect(self.win,
                                 self.LIGHT_SQUARE_COLOR,
                                 (row * self.SQUARE_SIZE, col * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def _drawPieces(self):
        board = self.board.getBoard()
        for row in range(10):
            for col in range((1 if row % 2 == 0 else 0), 10, 2):
                pos = (row * 5) + (col // 2)
                piece = board[pos]
                if piece != 0:
                    # Draw the larger circle first
                    pygame.draw.circle(self.win,
                                       self.PADDING_COLOR_WHITE if piece > 0 else self.PADDING_COLOR_RED,
                                       (self.SQUARE_SIZE * col + (self.SQUARE_SIZE // 2), self.SQUARE_SIZE * row + (self.SQUARE_SIZE // 2)),
                                       self.PIECE_SIZE + self.PADDING_SIZE)
                    pygame.draw.circle(self.win,
                                       self.WHITE_PIECE_COLOR if piece > 0 else self.RED_PIECE_COLOR,
                                       (self.SQUARE_SIZE * col + (self.SQUARE_SIZE // 2), self.SQUARE_SIZE * row + (self.SQUARE_SIZE // 2)),
                                       self.PIECE_SIZE)

    def _handleMouseInput(self, mPos):
        selectedRow, selectedCol = self._getPosFromMousePos(mPos)

        # First checks if the selected position is a dark square
        isDark = selectedRow % 2 != selectedCol % 2
        if not isDark:
            self.selectedPiece = False
            self._updateBoard()
            return

        pos = (5 * selectedRow) + (selectedCol // 2)

        if pos in self.legalMoves:
            self.selectedPiece = pos
        elif self.selectedPiece is None:
            pass
        elif pos in self.legalMoves[self.selectedPiece]:
            self.board.push((self.selectedPiece, pos, self.legalMoves[self.selectedPiece][pos]))
            self.selectedPiece = None
            self.legalMoves = self.board.getLegalMoves()
        else:
            self.selectedPiece = None
        self._updateBoard()

    def _getPosFromMousePos(self, mPos):
        x, y = mPos
        row = y // self.SQUARE_SIZE
        col = x // self.SQUARE_SIZE
        return row, col
