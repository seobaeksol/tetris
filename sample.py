import random
import sys
from logging import root
from typing import List

import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
GRID_SIZE = 25

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE]

# fmt: off
SHAPES = [
    [
        [
            '.....',
            '.....',
            '..00.',
            '..00.',
            '.....'
        ]
    ],
    [
        [
            '.....',
            '.....',
            '.....',
            '0000.',
            '.....'
        ],
        [
            '.....',
            '..0..',
            '..0..',
            '..0..',
            '..0..'
        ]
    ],
    [
        [
            '.....',
            '.....',
            '..0..',
            '.000.',
            '.....'
        ],
        [
            '.....',
            '..0..',
            '.00..',
            '..0..',
            '.....'
        ],
        [
            '.....',
            '.....',
            '.000.',
            '..0..',
            '.....'
        ],
        [
            '.....',
            '..0..',
            '..00.',
            '..0..',
            '.....'
        ],
    ],
    [
        [
            '.....',
            '.....',
            '..00.',
            '.00..',
            '.....'
        ],
        [
            '.....',
            '.0...',
            '.00..',
            '..0..',
            '.....'
        ],
        [
            '.....',
            '.....',
            '..00.',
            '.00..',
            '.....'
        ],
        [
            '.....',
            '.0...',
            '.00..',
            '..0..',
            '.....'
        ],
    ],
    [
        [
            '.....',
            '.....',
            '.00..',
            '..00.',
            '.....'
        ],
        [
            '.....',
            '..0..',
            '.00..',
            '.0...',
            '.....'
        ],
        [
            '.....',
            '.00..',
            '..00.',
            '.....',
            '.....'
        ],
        [
            '.....',
            '...0.',
            '..00.',
            '..0..',
            '.....'
        ],
    ],
    [
        [
            '.....',
            '.0...',
            '.0...',
            '.00..',
            '.....'
        ],
        [
            '.....',
            '.000.',
            '.0...',
            '.....',
            '.....'
        ],
        [
            '.....',
            '..00.',
            '...0.',
            '...0.',
            '.....'
        ],
        [
            '.....',
            '.....',
            '...0.',
            '.000.',
            '.....'
        ],
    ],
    [
        [
            '.....',
            '...0.',
            '...0.',
            '..00.',
            '.....'
        ],
        [
            '.....',
            '.....',
            '.0...',
            '.000.',
            '.....'
        ],
        [
            '.....',
            '.00..',
            '.0...',
            '.0...',
            '.....'
        ],
        [
            '.....',
            '.000.',
            '...0.',
            '.....',
            '.....'
        ],
    ],
]


class Tetromino:
    shape: list[list[str]]
    x: int
    y: int
    color: tuple[int, int, int]
    rotation: int

    def __init__(self, x: int, y: int, shape: list[list[str]]):
        self.shape = shape
        self.x = 0
        self.y = 0
        self.color = random.choice(COLORS)
        self.rotation = 0

class Tetris:
    width: int
    height: int
    grid: list[list[int | tuple[int, int, int]]]
    current_piece: Tetromino
    game_over: bool
    score: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        return Tetromino(self.width // 2, 0, shape)

    def valid_move(self, piece: Tetromino, x: int, y: int, rotation: int):
        """Check if the piece can move to the given position"""
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, cell in enumerate(row):
                new_x = piece.x + j + x
                new_y = piece.y + i + y

                if cell == '0' and (new_x < 0 or new_x >= self.width or new_y >= self.height):
                    return False

                if cell == '0' and (self.grid[new_y][new_x] != 0):
                    return False

        return True

    def clear_lines(self):
        """Clear the lines that are full and return the number of cleared lines"""
        lines_cleared = 0
        for i, row in enumerate(self.grid[:-1]):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])

        return lines_cleared

    def lock_piece(self, piece: Tetromino):
        """Lock the piece in place and create a new piece"""
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == '0':
                    self.grid[piece.y + i][piece.x + j] = piece.color

        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100
        self.current_piece = self.new_piece()

        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True

        return lines_cleared

    def update(self):
        """Move the tetromino down one cell"""
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)


    def draw(self, screen: pygame.Surface):
        """Draw the grid and the current piece"""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        if self.current_piece:
            for i, row in enumerate(self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == '0':
                        pygame.draw.rect(screen, self.current_piece.color, ((self.current_piece.x + j) * GRID_SIZE, (self.current_piece.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))


    def move_left(self):
        if self.valid_move(self.current_piece, -1, 0, 0):
            self.current_piece.x -= 1

    def move_right(self):
        if self.valid_move(self.current_piece, 1, 0, 0):
            self.current_piece.x += 1

    def move_down(self):
        if self.valid_move(self.current_piece, 0, 1, 0):
            self.current_piece.y += 1

    def move_up(self):
        if self.valid_move(self.current_piece, 0, -1, 0):
            self.current_piece.rotation += 1

    def move_space(self):
        while self.valid_move(self.current_piece, 0, 1, 0):
            self.current_piece.y += 1
        self.lock_piece(self.current_piece)

    def move(self, key):
        if key == pygame.K_LEFT:
            self.move_left()
        elif key == pygame.K_RIGHT:
            self.move_right()
        elif key == pygame.K_DOWN:
            self.move_down()
        elif key == pygame.K_UP:
            self.move_up()
        elif key == pygame.K_SPACE:
            self.move_space()


def draw_score(screen, score, x, y):
    """Draw the score on the screen"""
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (x, y))

def draw_game_over(screen, x, y):
    """Draw the game over text on the screen"""
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (x, y))


def main():
    # Initialize game
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    # Create a clock object
    clock = pygame.time.Clock()
    # Create a game object
    game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)

    fall_time = 0
    fall_speed = 50 # miliseconds

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                game.move(event.key)

        delta_time = clock.get_rawtime()
        fall_time += delta_time

        if fall_time >= fall_speed:
            game.update()
            fall_time = 0

        draw_score(screen, game.score, 10, 10)

        game.draw(screen)

        if game.game_over:
            draw_game_over(screen, WIDTH // 2 - 100, HEIGHT // 2 - 30)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
