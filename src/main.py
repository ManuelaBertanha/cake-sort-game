import pygame
import random

from gameState import GameState
from cakeState import CakeState
from cake import Cake
from slice import Slice

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
BG_COLOR = (240, 240, 240)
GRID_ROWS, GRID_COLS = 5, 4
CELL_SIZE = 90
MARGIN = 10
CAKE_WIDTH, CAKE_HEIGHT = 75, 75
SLICE_COUNT = 6  # Cada bolo completo tem 6 fatias
CAKE_COLORS = [(153, 51, 51), (0, 204, 102)]  # [(153, 51, 51), (0, 204, 102), (102, 153, 153), (255, 255, 77)]
COLOR_NAMES = {(153, 51, 51): "vermelho", (0, 204, 102): "verde"}
BORDER_COLOR = (102, 102, 102)
SELECTED_BORDER_COLOR = (255, 117, 26)  # Laranja para indicar seleção
BORDER_THICKNESS = 1

# Centralizar o grid
GRID_WIDTH = GRID_COLS * (CELL_SIZE + MARGIN) - MARGIN
GRID_HEIGHT = GRID_ROWS * (CELL_SIZE + MARGIN) - MARGIN
GRID_X = (WIDTH - GRID_WIDTH) // 2
GRID_Y = (HEIGHT - GRID_HEIGHT) // 2

# Posição inicial dos bolos gerados fora do grid
OUT_GRID_X = WIDTH - 150
OUT_GRID_Y_START = 150
OUT_GRID_SPACING = 120


def draw_grid(screen):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            pygame.draw.rect(screen, (200, 200, 200),
                             (GRID_X + col * (CELL_SIZE + MARGIN),
                              GRID_Y + row * (CELL_SIZE + MARGIN),
                              CELL_SIZE, CELL_SIZE), 2)


def draw_cake(screen, x, y, layers, selected=False):
    layer_height = CAKE_HEIGHT // SLICE_COUNT
    border_color = SELECTED_BORDER_COLOR if selected else BORDER_COLOR
    for i in range(SLICE_COUNT):
        color = layers[i].color if i < len(layers) else (220, 220, 220)
        pygame.draw.rect(screen, color, (x, y + i * layer_height, CAKE_WIDTH, layer_height))
        pygame.draw.rect(screen, border_color, (x, y + i * layer_height, CAKE_WIDTH, layer_height), BORDER_THICKNESS)


def generate_random_cake():
    num_layers = random.randint(1, 5)  # Quantidade aleatória de fatias entre 1 e 5
    return [Slice(color, COLOR_NAMES[color]) for color in random.choices(CAKE_COLORS, k=num_layers)]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cake Sorting Puzzle")
    clock = pygame.time.Clock()

    pygame.font.init()
    font = pygame.font.SysFont('Arial', 24)

    initial_grid = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    game_state = GameState()
    cake_state = CakeState(initial_grid, game_state)

    available_cakes = [Cake(generate_random_cake()) for _ in range(3)]
    selected_cake_index = None

    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_grid(screen)

        score_text = font.render(f"Score: {game_state.score}", True, (0, 0, 0))
        screen.blit(score_text, (20, 20))

        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                if cake_state.grid[row][col]:
                    x = GRID_X + col * (CELL_SIZE + MARGIN) + (CELL_SIZE - CAKE_WIDTH) // 2
                    y = GRID_Y + row * (CELL_SIZE + MARGIN) + (CELL_SIZE - CAKE_HEIGHT) // 2
                    draw_cake(screen, x, y, cake_state.grid[row][col].slices)

        for i, cake in enumerate(available_cakes):
            x = OUT_GRID_X
            y = OUT_GRID_Y_START + i * OUT_GRID_SPACING
            draw_cake(screen, x, y, cake.slices, selected=(selected_cake_index == i))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                for i in range(len(available_cakes)):
                    cake_x = OUT_GRID_X
                    cake_y = OUT_GRID_Y_START + i * OUT_GRID_SPACING
                    if cake_x <= x <= cake_x + CAKE_WIDTH and cake_y <= y <= cake_y + CAKE_HEIGHT:
                        selected_cake_index = i
                        break
                else:
                    col = (x - GRID_X) // (CELL_SIZE + MARGIN)
                    row = (y - GRID_Y) // (CELL_SIZE + MARGIN)

                    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS and selected_cake_index is not None:
                        if not cake_state.grid[row][col]:
                            cake_state.grid[row][col] = Cake()
                        cake_state.grid[row][col].slices.extend(available_cakes[selected_cake_index].slices)
                        available_cakes[selected_cake_index] = Cake(generate_random_cake())
                        selected_cake_index = None
                        cake_state.apply_operator(row, col)  # Passa as coordenadas do bolo posicionado

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
