import pygame
import random

# Configurações iniciais
WIDTH, HEIGHT = 600, 500
BG_COLOR = (240, 240, 240)
GRID_ROWS, GRID_COLS = 5, 4
CELL_SIZE = 100
MARGIN = 10
CAKE_WIDTH, CAKE_HEIGHT = 60, 80
CAKE_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]


def draw_grid(screen):
    """Desenha o grid visível ao jogador."""
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            pygame.draw.rect(screen, (200, 200, 200),
                             (col * (CELL_SIZE + MARGIN), row * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE), 2)


def draw_cake(screen, x, y, layers):
    """Desenha um bolo empilhado com camadas de diferentes cores."""
    if not layers:
        return
    layer_height = CAKE_HEIGHT // len(layers)
    for i, color in enumerate(layers):
        pygame.draw.rect(screen, color, (x, y + i * layer_height, CAKE_WIDTH, layer_height))


def generate_random_cake():
    """Gera um bolo aleatório com algumas fatias."""
    num_layers = random.randint(2, 4)
    return random.sample(CAKE_COLORS, num_layers)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cake Sorting Puzzle")
    clock = pygame.time.Clock()

    grid = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_grid(screen)

        # Desenha os bolos no grid
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                if grid[row][col]:
                    x = col * (CELL_SIZE + MARGIN) + (CELL_SIZE - CAKE_WIDTH) // 2
                    y = row * (CELL_SIZE + MARGIN) + (CELL_SIZE - CAKE_HEIGHT) // 2
                    draw_cake(screen, x, y, grid[row][col])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // (CELL_SIZE + MARGIN)
                row = y // (CELL_SIZE + MARGIN)
                if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS and grid[row][col] is None:
                    grid[row][col] = generate_random_cake()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
