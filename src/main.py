import pygame
import random

# Initial settings
WIDTH, HEIGHT = 800, 600
BG_COLOR = (240, 240, 240)
GRID_ROWS, GRID_COLS = 5, 4
CELL_SIZE = 90
MARGIN = 10
CAKE_WIDTH, CAKE_HEIGHT = 75, 75
SLICE_COUNT = 6  # Each complete cake has 6 slices
CAKE_COLORS = [(153, 51, 51), (0, 204, 102), (102, 153, 153), (255, 255, 77)]
BORDER_COLOR = (102, 102, 102)
SELECTED_BORDER_COLOR = (255, 117, 26)  # Orange color to indicate selection
BORDER_THICKNESS = 1

# Center the grid
GRID_WIDTH = GRID_COLS * (CELL_SIZE + MARGIN) - MARGIN
GRID_HEIGHT = GRID_ROWS * (CELL_SIZE + MARGIN) - MARGIN
GRID_X = (WIDTH - GRID_WIDTH) // 2
GRID_Y = (HEIGHT - GRID_HEIGHT) // 2

# Starting position of cakes generated outside the grid
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
        color = layers[i] if i < len(layers) else (220, 220, 220)  # Gray for empty slices
        pygame.draw.rect(screen, color, (x, y + i * layer_height, CAKE_WIDTH, layer_height))
        pygame.draw.rect(screen, border_color, (x, y + i * layer_height, CAKE_WIDTH, layer_height), BORDER_THICKNESS)


def generate_random_cake():
    num_layers = random.randint(2, 5)
    return random.choices(CAKE_COLORS, k=num_layers)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cake Sorting Puzzle")
    clock = pygame.time.Clock()

    grid = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    available_cakes = [generate_random_cake() for _ in range(3)]
    selected_cake_index = None  # Index of selected cake

    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_grid(screen)

        # Draw the cakes on the grid
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                if grid[row][col]:
                    x = GRID_X + col * (CELL_SIZE + MARGIN) + (CELL_SIZE - CAKE_WIDTH) // 2
                    y = GRID_Y + row * (CELL_SIZE + MARGIN) + (CELL_SIZE - CAKE_HEIGHT) // 2
                    draw_cake(screen, x, y, grid[row][col])

        # Design the cakes available to choose from
        for i, cake in enumerate(available_cakes):
            x = OUT_GRID_X
            y = OUT_GRID_Y_START + i * OUT_GRID_SPACING
            draw_cake(screen, x, y, cake, selected=(selected_cake_index == i))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Checks if the player clicked on one of the available cakes
                for i in range(len(available_cakes)):
                    cake_x = OUT_GRID_X
                    cake_y = OUT_GRID_Y_START + i * OUT_GRID_SPACING
                    if cake_x <= x <= cake_x + CAKE_WIDTH and cake_y <= y <= cake_y + CAKE_HEIGHT:
                        selected_cake_index = i
                        break
                else:
                    # Checks if the player clicked on an empty space on the grid
                    col = (x - GRID_X) // (CELL_SIZE + MARGIN)
                    row = (y - GRID_Y) // (CELL_SIZE + MARGIN)
                    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS and grid[row][col] is None and selected_cake_index is not None:
                        grid[row][col] = available_cakes.pop(selected_cake_index)
                        available_cakes.append(generate_random_cake())  # Add a new cake
                        selected_cake_index = None  # Reset the selection

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
