from typing import Tuple

import numpy as np
import math
import pygame
from pygame import display, draw, font, Surface, QUIT, MOUSEBUTTONDOWN

# static variables
ROW_COUNT = 15
COL_COUNT = 15

EMPTY = 0
BLACK_PIECE = 1  # black
WHITE_PIECE = 2  # white
PIECES = (BLACK_PIECE, WHITE_PIECE)

# define screen size
BLOCKSIZE = 50                    # individual grid
S_WIDTH = COL_COUNT * BLOCKSIZE   # screen width
S_HEIGHT = ROW_COUNT * BLOCKSIZE  # screen height
PADDING_RIGHT = 200               # for game menu
SCREENSIZE = (S_WIDTH + PADDING_RIGHT, S_HEIGHT)
RADIUS = 20                       # game piece radius

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (205, 128, 0)
PIECE_COLOURS = (BLACK, WHITE)


def create_board(row: int, col: int) -> np.ndarray:
    return np.zeros((row, col), dtype=np.int32)


def draw_board(screen: Surface) -> None:
    screen.fill(BROWN)

    # draw vertical inner grid lines
    for x in range(BLOCKSIZE // 2, S_WIDTH + BLOCKSIZE // 2, BLOCKSIZE):
        draw.line(
            screen, BLACK,
            start_pos=(x, BLOCKSIZE // 2),
            end_pos=(x, S_HEIGHT-BLOCKSIZE // 2),
            width=2,
        )

    # draw horizontal inner lines
    for y in range(BLOCKSIZE // 2, S_HEIGHT + BLOCKSIZE // 2, BLOCKSIZE):
        draw.line(
            screen, BLACK,
            start_pos=(BLOCKSIZE // 2, y),
            end_pos=(S_WIDTH - BLOCKSIZE // 2, y),
            width=2,
        )


def drop_piece(board: np.ndarray, row: int, col: int, piece: int) -> None:
    board[row][col] = piece


def pixel_from_grid(x: int, y: int) -> Tuple[int, int]:
    return (
        x * BLOCKSIZE + BLOCKSIZE // 2,
        y * BLOCKSIZE + BLOCKSIZE // 2,
    )


def draw_piece(screen: Surface, board: np.ndarray) -> None:
    for piece, colour in zip(PIECES, PIECE_COLOURS):
        for y, x in np.argwhere(board == piece):
            draw.circle(
                screen, PIECE_COLOURS[board[y][x] - 1],
                pixel_from_grid(x, y), RADIUS,
            )
    display.update()


def is_valid_loc(board: np.ndarray, row: int, col: int) -> bool:
    return board[row][col] == EMPTY


def who_wins(board: np.ndarray, piece: int) -> bool:
    # check for horizontal win
    for c in range(COL_COUNT - 4):
        for r in range(ROW_COUNT):
            if np.all(board[r, c:c+5] == piece):
                return True

    # check for vertical win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 4):
            if np.all(board[r:r+5, c] == piece):
                return True

    # check for positively sloped diagonal wih
    for c in range(COL_COUNT - 4):
        for r in range(4, ROW_COUNT):
            if (
                board[r, c] == piece
                and board[r-1, c+1] == piece
                and board[r-2, c+2] == piece
                and board[r-3, c+3] == piece
                and board[r-4, c+4] == piece
            ):
                return True

    # check for negatively sloped diagonal win
    for c in range(COL_COUNT - 4):
        for r in range(ROW_COUNT - 4):
            if (
                board[r, c] == piece
                and board[r+1, c+1] == piece
                and board[r+2, c+2] == piece
                and board[r+3, c+3] == piece
                and board[r+4, c+4] == piece
            ):
                return True

    return False


def setup_gui() -> Surface:
    screen = display.set_mode(SCREENSIZE)
    display.set_caption('Gomoku (Connet 5)')
    # icon = pygame.image.load('icon.png')
    # pygame.display.set_icon(icon)

    draw_board(screen)
    display.update()
    return screen


def end_banner(screen: Surface, piece: str) -> None:
    my_font = font.Font('freesansbold.ttf', 32)
    label = my_font.render(f'{piece} wins!', True, WHITE, BLACK)
    screen.blit(label, (280, 50))
    display.update()


def game(screen: Surface) -> None:
    turn = BLACK_PIECE

    # board 2D array
    board = create_board(ROW_COUNT, COL_COUNT)

    # game loop
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            return

        elif event.type == MOUSEBUTTONDOWN:
            x_pos, y_pos = event.pos
            col = math.floor(x_pos / BLOCKSIZE)
            row = math.floor(y_pos / BLOCKSIZE)

            if not is_valid_loc(board, row, col):
                continue

            drop_piece(board, row, col, turn)
            draw_piece(screen, board)

            if who_wins(board, turn):
                name = 'Black' if turn == BLACK_PIECE else 'White'
                end_banner(screen, name)
                return

            turn = 3 - turn


def main() -> None:
    # initialize the pygame program
    pygame.init()
    try:
        screen = setup_gui()
        game(screen)
        while pygame.event.wait().type != QUIT:
            pass
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
