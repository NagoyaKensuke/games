import pygame


class LifeGameModel:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def step(self):
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                alive_neighbors = self.get_alive_neighbors(row, col)
                if self.grid[row][col] == 1 and (alive_neighbors == 2 or alive_neighbors == 3):
                    new_grid[row][col] = 1
                elif self.grid[row][col] == 0 and alive_neighbors == 3:
                    new_grid[row][col] = 1
        self.grid = new_grid

    def get_alive_neighbors(self, row, col):
        neighbors = [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1), (row, col + 1),
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
        ]
        count = 0
        for neighbor_row, neighbor_col in neighbors:
            if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                count += self.grid[neighbor_row][neighbor_col]
        return count


class LifeGameView:
    def __init__(self, model, cell_size=10):
        self.model = model
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((model.cols * cell_size, model.rows * cell_size))
        pygame.display.set_caption("Conway's Game of Life")

    def draw(self):
        self.screen.fill((255, 255, 255))
        for row in range(self.model.rows):
            for col in range(self.model.cols):
                if self.model.grid[row][col] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()


class LifeGameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = False
        self.autoplay = False
        self.speed = 5  # 1 to 60, higher is faster

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // self.view.cell_size, x // self.view.cell_size
                    self.model.grid[row][col] = 1 if self.model.grid[row][col] == 0 else 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.autoplay = not self.autoplay
                    elif event.key == pygame.K_UP and self.speed < 60:
                        self.speed += 1
                    elif event.key == pygame.K_DOWN and self.speed > 1:
                        self.speed -= 1

            if self.autoplay:
                self.model.step()

            self.view.draw()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    model = LifeGameModel(50, 50)
    view = LifeGameView(model)
    controller = LifeGameController(model, view)
    controller.run()
