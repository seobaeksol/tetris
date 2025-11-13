import random
import pygame

# fmt: off
TETROMINO_INFO = [
    {
        'shapes': [
            [
                '00',
                '00',
            ]
        ],
        'color': (255, 255, 0)
    },
    {
        'shapes': [
            [
                '....',
                '....',
                '....',
                '0000',
                '....',
            ],
            [
                '.0..',
                '.0..',
                '.0..',
                '.0..'
            ],
            [
                '....',
                '....',
                '....',
                '0000',
                '....',
            ],
            [
                '..0.',
                '..0.',
                '..0.',
                '..0.'
            ],
        ],
        'color': (0, 255, 255)
    },
    {
        'shapes': [
            [
                '.0.',
                '000',
                '...',
            ],
            [
                '.0.',
                '.00',
                '.0.',
            ],
            [
                '...',
                '000',
                '.0.',
            ],
            [
                '.0.',
                '00.',
                '.0.',
            ],
        ],
        'color': (255, 0, 255)
    },
    {
        'shapes': [
            [
                '.....',
                '..00.',
                '.00..',
                '.....',
            ],
            [
                '.....',
                '.0...',
                '.00..',
                '..0..',
            ],
            [
                '.....',
                '..00.',
                '.00..',
                '.....',
            ],
            [
                '.....',
                '.0...',
                '.00..',
                '..0..',
            ],
        ],
        'color': (0, 255, 0)
    },
    {
        'shapes': [
            [
                '.....',
                '.00..',
                '..00.',
                '.....',
            ],
            [
                '.....',
                '..0..',
                '.00..',
                '.0...',
            ],
            [
                '.....',
                '.00..',
                '..00.',
                '.....',
            ],
            [
                '.....',
                '...0.',
                '..00.',
                '..0..',
            ],
        ],
        'color': (255, 165, 0)
    },
    {
        'shapes': [
            [
                '.....',
                '..0..',
                '..0..',
                '..00.',
                '.....',
            ],
            [
                '.....',
                '.....',
                '.000.',
                '.0...',
                '.....',
            ],
            [
                '.....',
                '.00..',
                '..0..',
                '..0..',
                '.....',
            ],
            [
                '.....',
                '...0.',
                '.000.',
                '.....',
                '.....',
            ]
        ],
        'color': (255, 165, 0)
    },
    {
        'shapes': [
            [
                '.....',
                '..0..',
                '..0..',
                '.00..',
                '.....',
            ],
            [
                '.....',
                '.0...',
                '.000.',
                '.....',
                '.....',
            ],
            [
                '.....',
                '..00.',
                '..0..',
                '..0..',
                '.....',
            ],
            [
                '.....',
                '.....',
                '.000.',
                '...0.',
                '.....',
            ],
        ],
        'color': (0, 0, 255)
    },
]

class Tetromino:
    shape: list[list[str]]
    rotation: int
    color: tuple[int, int, int]
    position: tuple[int, int]

    def __init__(self, shape: list[list[str]], color: tuple[int, int, int]) -> None:
        self.shape = shape
        self.rotation = 0
        self.color = color
        self.position = (0, 0)

    def rotate(self) -> None:
        self.rotation = (self.rotation + 1) % len(self.shape)

    def get_shape(self) -> list[str]:
        return self.shape[self.rotation]

class Tetris:
    screen: pygame.Surface
    bg_color: tuple[int, int, int] = (0, 0, 0)
    left_panel_color: tuple[int, int, int] = (50, 50, 50)
    right_panel_color: tuple[int, int, int] = (50, 50, 50)
    grid_color: tuple[int, int, int] = (200, 200, 200)
    grid_line_color: tuple[int, int, int] = (0, 0, 0)
    grid_columns: int = 10
    grid_rows: int = 20
    grid: list[list[int | tuple[int, int, int]]]
    current_piece: Tetromino | None = None
    next_piece: Tetromino | None = None
    game_speed: int = 500  # milliseconds per drop
    score: int = 0
    level: int = 1
    lines_cleared: int = 0
    is_game_over: bool = False
    held_keys: dict[int, tuple[int, int]] = {}
    repeat_delay: int = 100  # milliseconds
    move_delay: int = 30  # milliseconds
    shake_end_time: int = 0
    shake_magnitude: int = 0
    shake_offset: tuple[int, int] = (0, 0)

    def __init__(self, width = 400, height = 500) -> None:
        pygame.init()
        flags = pygame.RESIZABLE
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.update_display_size()

        # Initialize the grid
        self.grid = [[0 for _ in range(self.grid_columns)] for _ in range(self.grid_rows)]

        # Initialize the first pieces
        random_tetromino = random.choice(TETROMINO_INFO)
        self.next_piece = Tetromino(random_tetromino['shapes'], random_tetromino['color'])
        random_tetromino = random.choice(TETROMINO_INFO)
        self.current_piece = Tetromino(random_tetromino['shapes'], random_tetromino['color'])

        # Screen shake state
        self.shake_end_time = 0        # timestamp (ms) when the shake should stop
        self.shake_magnitude = 0       # maximum pixel offset during shake
        self.shake_offset = (0, 0)     # current frame's offset (x, y)
    
    def update_display_size(self) -> None:
        screen_width, screen_height = self.screen.get_size()
        screen_width = screen_width // 1
        screen_height = screen_height // 1
        horizontal_center = screen_width // 2
        vertical_center = screen_height // 2

        if screen_width < 400 or screen_height < 500:
            raise ValueError("Screen size must be at least 400x500")

        # Calculate panel widths
        if screen_width >= screen_height:
            panel_height = screen_height
            panel_width = panel_height // 4
        else:
            panel_height = screen_width
            panel_width = panel_height // 4

        self.panel_width = panel_width
        self.panel_height = panel_height
        self.panel_start_y = vertical_center - panel_height // 2
        self.left_panel_start_x = horizontal_center - panel_width * 2
        self.right_panel_start_x = horizontal_center + panel_width
        self.grid_start_x = horizontal_center - panel_width
        self.grid_width = panel_width * 2
        self.piece_size = self.grid_width // self.grid_columns  # Assuming 10 columns in the grid

    def reset(self) -> None:
        self.grid = [[0 for _ in range(self.grid_columns)] for _ in range(self.grid_rows)]
        self.current_piece = None
        self.game_speed = 500
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.is_game_over = False

    def draw_background(self) -> None:
        # Initialize values
        screen_width, screen_height = self.screen.get_size()
        horizontal_center = screen_width // 2

        if screen_width < 400 or screen_height < 500:
            raise ValueError("Screen size must be at least 400x500")

        # Use current shake offset when drawing
        offset_x, offset_y = self.shake_offset

        # Fill the background with black
        self.screen.fill(self.bg_color)

        # Draw left panel
        pygame.draw.rect(self.screen, self.left_panel_color, (horizontal_center - self.panel_width * 2 + offset_x, self.panel_start_y + offset_y, self.panel_width, self.panel_height))

        # Draw right panel
        pygame.draw.rect(self.screen, self.right_panel_color, (horizontal_center + self.panel_width + offset_x, self.panel_start_y + offset_y, self.panel_width, self.panel_height))

        # Draw grid area
        pygame.draw.rect(self.screen, self.grid_color, (self.grid_start_x + offset_x, self.panel_start_y + offset_y, self.grid_width, self.panel_height))
        for i in range(self.grid_columns + 1):
            x = self.grid_start_x + i * self.piece_size + offset_x
            pygame.draw.line(self.screen, self.grid_line_color, (x, self.panel_start_y + offset_y), (x, self.panel_start_y + self.panel_height + offset_y))
        for j in range(self.grid_rows + 1):
            y = self.panel_start_y + j * self.piece_size + offset_y
            pygame.draw.line(self.screen, self.grid_line_color, (self.grid_start_x + offset_x, y), (self.grid_start_x + self.grid_width + offset_x, y))

    def valid_move(self, dx: int, dy: int) -> bool:
        """Check if the current piece can move by (dx, dy)"""
        if self.current_piece is None:
            return False

        new_x = self.current_piece.position[0] + dx
        new_y = self.current_piece.position[1] + dy

        # Check for collisions
        for i, row in enumerate(self.current_piece.get_shape()):
            for j, cell in enumerate(row):
                if cell == '0':
                    grid_x = new_x + j
                    grid_y = new_y + i
                    if grid_x < 0 or grid_x >= self.grid_columns or grid_y < 0 or grid_y >= self.grid_rows:
                        return False
                    if self.grid[grid_y][grid_x] != 0:
                        return False
        return True
    
    def move_piece(self, dx: int, dy: int) -> None:
        """Move the current piece by (dx, dy) if possible"""
        if self.current_piece is None:
            return

        if self.valid_move(dx, dy):
            self.current_piece.position = (self.current_piece.position[0] + dx, self.current_piece.position[1] + dy)

    def drop_piece(self) -> None:
        """Drop the current piece down until it lands"""
        if self.current_piece is None:
            return

        while self.valid_move(0, 1):
            self.current_piece.position = (self.current_piece.position[0], self.current_piece.position[1] + 1)

    def rotate_piece(self) -> None:
        """Rotate the current piece if possible"""
        if self.current_piece is None:
            return

        original_rotation = self.current_piece.rotation
        self.current_piece.rotate()
        
        if not self.valid_move(0, 0):
            if self.current_piece.position[0] < 0:
                self.current_piece.position = (0, self.current_piece.position[1])
            elif self.current_piece.position[0] + len(self.current_piece.get_shape()[0]) > self.grid_columns:
                self.current_piece.position = (self.grid_columns - len(self.current_piece.get_shape()[0]), self.current_piece.position[1])
            
        # If still not valid, revert rotation
        if not self.valid_move(0, 0):
            self.current_piece.rotation = original_rotation

    def lock_piece(self) -> None:
        """Lock the current piece into the grid"""
        if self.current_piece is None:
            return

        x, y = self.current_piece.position
        for i, row in enumerate(self.current_piece.get_shape()):
            for j, cell in enumerate(row):
                if cell == '0':
                    self.grid[y + i][x + j] = self.current_piece.color

        self.current_piece = None

    def draw_status(self) -> None:
        font_size = self.panel_width // 10
        font = pygame.font.SysFont('Arial', font_size)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        level_text = font.render(f'Level: {self.level}', True, (255, 255, 255))
        lines_text = font.render(f'Lines: {self.lines_cleared}', True, (255, 255, 255))

        offset_x, offset_y = self.shake_offset

        self.screen.blit(score_text, (self.left_panel_start_x + 10 + offset_x, self.panel_start_y + 10 + offset_y))
        self.screen.blit(level_text, (self.left_panel_start_x + 10 + offset_x, self.panel_start_y + 40 + offset_y))
        self.screen.blit(lines_text, (self.left_panel_start_x + 10 + offset_x, self.panel_start_y + 70 + offset_y))

        # Draw next piece
        if self.next_piece is not None:
            next_text = font.render('Next:', True, (255, 255, 255))
            self.screen.blit(next_text, (self.right_panel_start_x + 10 + offset_x, self.panel_start_y + 10 + offset_y))

            for i, row in enumerate(self.next_piece.get_shape()):
                for j, cell in enumerate(row):
                    if cell == '0':
                        pygame.draw.rect(
                            self.screen,
                            self.next_piece.color,
                            (
                                self.right_panel_start_x + 10 + j * self.piece_size + offset_x,
                                self.panel_start_y + 40 + i * self.piece_size + offset_y,
                                self.piece_size - 1,
                                self.piece_size - 1
                            )
                        )

    def update(self) -> None:
        if self.current_piece is None:
            random_tetromino = random.choice(TETROMINO_INFO)
            self.current_piece = self.next_piece
            self.next_piece = Tetromino(random_tetromino['shapes'], random_tetromino['color'])

        # If the new piece cannot be placed, the game is over
        if not self.valid_move(0, 0):
            self.is_game_over = True
            return

        # Clear full lines
        lines_to_clear = []
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(i)
        
        if lines_to_clear:
            combo_bonus = 0
            for line in lines_to_clear:
                del self.grid[line]
                self.grid.insert(0, [0 for _ in range(self.grid_columns)])
                combo_bonus += 1
                self.score += 100 * combo_bonus

            # Trigger a screen shake for multi-line clears
            if len(lines_to_clear) >= 1:
                # duration grows slightly with more lines, magnitude scales but is clamped
                duration = 300  # milliseconds
                self.shake_magnitude = len(lines_to_clear)
                self.shake_end_time = pygame.time.get_ticks() + duration

        self.lines_cleared += len(lines_to_clear)
        if self.lines_cleared >= 10 * self.level:
            self.level += 1
            self.score += 1000
            self.game_speed = max(100, self.game_speed - 50)

    def draw_grid(self) -> None:
        offset_x, offset_y = self.shake_offset
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(
                        self.screen,
                        cell,
                        (
                            self.grid_start_x + x * self.piece_size + offset_x,
                            y * self.piece_size + self.panel_start_y + offset_y,
                            self.piece_size - 1,
                            self.piece_size - 1
                        )
                    )

        # Draw current piece
        if self.current_piece is not None:
            x, y = self.current_piece.position
            for i, row in enumerate(self.current_piece.get_shape()):
                for j, cell in enumerate(row):
                    if cell == '0':
                        pygame.draw.rect(
                            self.screen,
                            self.current_piece.color,
                            (
                                self.grid_start_x + (x + j) * self.piece_size + offset_x,
                                (y + i) * self.piece_size + self.panel_start_y + offset_y,
                                self.piece_size - 1,
                                self.piece_size - 1
                            )
                        )

    def run(self) -> None:
        last_drop_time = pygame.time.get_ticks()
        last_move_time = pygame.time.get_ticks()
        prev_frame_time = pygame.time.get_ticks()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.VIDEORESIZE:
                    width = max(400, event.w)
                    height = max(500, event.h)
                    self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    self.update_display_size()

                if self.is_game_over and event.type == pygame.KEYDOWN:
                    self.reset()
                    continue

                # Handle single-press actions (rotation and hard drop)
                if not self.is_game_over and event.type == pygame.KEYDOWN:
                    now = pygame.time.get_ticks()
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                        self.held_keys[pygame.K_LEFT] = (now, now)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                        self.held_keys[pygame.K_RIGHT] = (now, now)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece(0, 1)
                        self.held_keys[pygame.K_DOWN] = (now, now)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.drop_piece()
                        self.lock_piece()
                
                if event.type == pygame.KEYUP:
                    if event.key in self.held_keys:
                        del self.held_keys[event.key]
            
            # Handle held keys for continuous movement
            if not self.is_game_over and self.current_piece is not None:
                current_time = pygame.time.get_ticks()
                
                for key, (first_press_time, last_move_time_key) in list(self.held_keys.items()):
                    if current_time - first_press_time > self.repeat_delay:
                        if current_time - last_move_time_key > self.move_delay:
                            if key == pygame.K_LEFT and self.valid_move(-1, 0):
                                self.current_piece.position = (self.current_piece.position[0] - 1, self.current_piece.position[1])
                                self.held_keys[key] = (first_press_time, current_time)
                            elif key == pygame.K_RIGHT and self.valid_move(1, 0):
                                self.current_piece.position = (self.current_piece.position[0] + 1, self.current_piece.position[1])
                                self.held_keys[key] = (first_press_time, current_time)
                            elif key == pygame.K_DOWN and self.valid_move(0, 1):
                                self.current_piece.position = (self.current_piece.position[0], self.current_piece.position[1] + 1)
                                self.held_keys[key] = (first_press_time, current_time)

            # compute shake offset for this frame
            current_time = pygame.time.get_ticks()
            if current_time < self.shake_end_time:
                m = self.shake_magnitude
                self.shake_offset = (random.randint(-m, m), random.randint(-m, m))
            else:
                self.shake_offset = (0, 0)

            self.draw_background()
            current_time = pygame.time.get_ticks()
            if current_time - last_drop_time > self.game_speed:
                last_drop_time = current_time
                if not self.valid_move(0, 1):
                    # If the piece can't move down, it has landed
                    self.lock_piece()
                elif self.current_piece is not None:
                    # Move the piece down
                    self.current_piece.position = (self.current_piece.position[0], self.current_piece.position[1] + 1)

            self.update()
            self.draw_grid()
            self.draw_status()

            if self.is_game_over:
                font = pygame.font.SysFont('Arial', 50)
                game_over_text = font.render('Game Over', True, (255, 0, 0))
                text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
                self.screen.blit(game_over_text, text_rect)

            pygame.display.flip()
            self.clock.tick(60)

def main():
    tetris = Tetris()
    tetris.run()

if __name__ == "__main__":
    main()
