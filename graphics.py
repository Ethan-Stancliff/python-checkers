import pygame


class Graphics:
    _defaults = {
        "LIGHT_SQUARE_COLOR": (180, 180, 180),
        "DARK_SQUARE_COLOR": (60, 60, 60),
        "PIECE_SIZE": 27,
        "WHITE_PIECE_COLOR": (230, 230, 230),
        "RED_PIECE_COLOR": (200, 0, 0),
        "PADDING_SIZE": 4,
        "PADDING_COLOR_WHITE": (128, 128, 128),
        "PADDING_COLOR_RED": (192, 128, 128)
    }

    def __init__(self, board, **kwargs):
        self.board = board
        for key in Graphics._defaults:
            self.__dict__.update({key: kwargs[key] if key in kwargs else Graphics._defaults[key]})
        self.win = pygame.display.set_mode((750, 750))
        self.clock = pygame.time.Clock()

    def run(self):
        run = True
        while run:
            self.clock.tick(30)

            # TODO: Check Winner

            # TODO: Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # TODO: Update
            self._updateBoard()
        pygame.quit()

    def _updateBoard(self):
        self._drawBoardSquares()
        self._drawPieces()

        pygame.display.update()

    def _drawBoardSquares(self):
        self.win.fill(self.DARK_SQUARE_COLOR)
        for row in range(10):
            for col in range(row % 2, 10, 2):
                pygame.draw.rect(self.win, self.LIGHT_SQUARE_COLOR, (row*75, col*75, 75, 75))

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
                                        (75 * col + (75 // 2), 75 * row + (75 // 2)),
                                        self.PIECE_SIZE + self.PADDING_SIZE)
                    pygame.draw.circle(self.win,
                                       self.WHITE_PIECE_COLOR if piece > 0 else self.RED_PIECE_COLOR,
                                       (75 * col + (75 // 2), 75 * row + (75 // 2)),
                                       self.PIECE_SIZE)

    def _handleMouseInput(self):
        pass
