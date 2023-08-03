import pygame
import random

# 定数
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Tetris'
CELL_SIZE = 30
ROWS = 20
COLS = 10
WHITE = (255, 255, 255)
TETRIMINO_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (128, 0, 128),
]

# テトリミノの形状
SHAPES = [
    [
        [1, 1, 1],
        [0, 1, 0],
    ],
    [
        [1, 1],
        [1, 1]
    ],
    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [0, 1, 1],
        [1, 1, 0]
    ],
    [
        [1, 1, 1, 1]
    ],
    [
        [1, 0, 0],
        [1, 1, 1]
    ],
    [
        [0, 0, 1],
        [1, 1, 1]
    ]
]

# ボードクラス
class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.game_over = False

    def add_tetrimino(self, tetrimino):
        for i in range(len(tetrimino.shape)):
            for j in range(len(tetrimino.shape[i])):
                if tetrimino.shape[i][j]:
                    row = tetrimino.row + i
                    col = tetrimino.col + j
                    if row >= 0 and col >= 0 and row < self.rows and col < self.cols:
                        self.grid[row][col] = tetrimino.color_index + 1
                    else:
                        self.game_over = True

    def is_line_full(self, row):
        return all(self.grid[row][col] > 0 for col in range(self.cols))

    def remove_line(self, row):
        for r in range(row, 0, -1):
            self.grid[r] = self.grid[r - 1][:]
        self.grid[0] = [0 for _ in range(self.cols)]

    def is_collision(self, tetrimino, drow=0, dcol=0):
        for i in range(len(tetrimino.shape)):
            for j in range(len(tetrimino.shape[i])):
                if tetrimino.shape[i][j]:
                    row = tetrimino.row + i + drow
                    col = tetrimino.col + j + dcol
                    if row < 0 or col < 0 or row >= self.rows or col >= self.cols or self.grid[row][col] > 0:
                        return True
        return False

    def display(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                color_index = self.grid[row][col]
                color = WHITE if color_index == 0 else TETRIMINO_COLORS[color_index - 1]
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
                pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# テトリミノクラス
class Tetrimino:
    def __init__(self, shape_index):
        self.shape = SHAPES[shape_index][:]
        self.color_index = shape_index
        self.row = -len(self.shape) // 2
        self.col = COLS // 2 - len(self.shape[0]) // 2

    def rotate(self):
        self.shape = [[self.shape[col][row] for col in range(len(self.shape))] for row in range(len(self.shape[0]) - 1, -1, -1)]

# ゲームクラス
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.board = Board(ROWS, COLS)
        self.current_tetrimino = Tetrimino(random.randint(0, len(SHAPES) - 1))
        self.tick_time = 0
        self.fall_speed = 500
        self.score = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not self.board.is_collision(self.current_tetrimino, dcol=-1):
                    self.current_tetrimino.col -= 1
                elif event.key == pygame.K_RIGHT and not self.board.is_collision(self.current_tetrimino, dcol=1):
                    self.current_tetrimino.col += 1
                elif event.key == pygame.K_DOWN:
                    self.fall_speed = 50
                elif event.key == pygame.K_UP:
                    self.current_tetrimino.rotate()
                    if self.board.is_collision(self.current_tetrimino):
                        self.current_tetrimino.rotate()
                        self.current_tetrimino.rotate()
                        self.current_tetrimino.rotate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.fall_speed = 500

    def update(self, dt):
        self.tick_time += dt
        if self.tick_time > self.fall_speed:
            self.tick_time = 0
            if not self.board.is_collision(self.current_tetrimino, drow=1):
                self.current_tetrimino.row += 1
            else:
                self.board.add_tetrimino(self.current_tetrimino)
                self.current_tetrimino = Tetrimino(random.randint(0, len(SHAPES) - 1))
                for row in range(self.board.rows - 1, -1, -1):
                    if self.board.is_line_full(row):
                        self.board.remove_line(row)
                        self.score += 100

    def render(self):
        self.screen.fill(WHITE)
        self.board.display(self.screen)
        self.display_tetrimino(self.current_tetrimino)
        pygame.display.flip()

    def display_tetrimino(self, tetrimino):
        for i in range(len(tetrimino.shape)):
            for j in range(len(tetrimino.shape[i])):
                if tetrimino.shape[i][j]:
                    row = tetrimino.row + i
                    col = tetrimino.col + j
                    color = TETRIMINO_COLORS[tetrimino.color_index]
                    if row >= 0 and col >= 0:
                        pygame.draw.rect(self.screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
                        pygame.draw.rect(self.screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def run(self):
        while not self.board.game_over:
            dt = self.clock.tick(60)
            self.handle_input()
            self.update(dt)
            self.render()
        print("Game Over! Final Score:", self.score)
        pygame.quit()
        exit(0)

if __name__ == "__main__":
    Game().run()

