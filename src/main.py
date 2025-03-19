import pygame
import random

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
BG_COLOR = (240, 240, 240)
GRID_ROWS, GRID_COLS = 5, 4
CELL_SIZE = 90
MARGIN = 10
CAKE_WIDTH, CAKE_HEIGHT = 75, 75
SLICE_COUNT = 6  # Cada bolo completo tem 6 fatias
CAKE_COLORS = [(153, 51, 51), (0, 204, 102), (102, 153, 153), (255, 255, 77)]
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


class Slice:
    def __init__(self, color, id):
        self.color = color
        self.id = id

    def __eq__(self, other):
        return self.id == other.id


def generate_random_cake():
    num_layers = random.randint(2, 5)
    return [Slice(color, id(Slice)) for color in random.choices(CAKE_COLORS, k=num_layers)]


class CakeState:
    def __init__(self, grid):
        self.grid = [[cell[:] if cell else [] for cell in row] for row in grid]

    def is_valid(self, x, y):
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

    def merge_colors(self):
        changed = True
        safety_counter = 0  # Contador de segurança para evitar loop infinito
        max_iterations = 100  # Limite para evitar travamento

        while changed and safety_counter < max_iterations:
            changed = False
            safety_counter += 1
            for x in range(GRID_ROWS):
                for y in range(GRID_COLS):
                    if not self.grid[x][y]:
                        continue
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if self.is_valid(nx, ny) and self.grid[nx][ny]:
                            current_cake = self.grid[x][y]
                            neighbor_cake = self.grid[nx][ny]

                            # Tenta combinar as fatias com as mesmas cores
                            combined = False
                            for slice in current_cake:
                                for neighbor_slice in neighbor_cake:
                                    if slice.color == neighbor_slice.color:
                                        # Combinando as fatias de mesma cor
                                        new_layers = sorted(current_cake + neighbor_cake, key=lambda s: s.color)

                                        # Verifica se o novo bolo não ultrapassa 6 fatias
                                        if len(new_layers) <= SLICE_COUNT:
                                            # Atualiza a grade
                                            self.grid[nx][ny] = new_layers
                                            self.grid[x][y] = []
                                            changed = True
                                            combined = True
                                            break
                                if combined:
                                    break

                            # Se o bolo adjacente foi combinado, interrompe a iteração para o próximo bolo
                            if combined:
                                break

            if safety_counter >= max_iterations:
                print("Merge interrompido para evitar loop infinito.")

    def apply_operator(self):
        self.merge_colors()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cake Sorting Puzzle")
    clock = pygame.time.Clock()

    initial_grid = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    cake_state = CakeState(initial_grid)

    available_cakes = [generate_random_cake() for _ in range(3)]
    selected_cake_index = None

    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_grid(screen)

        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                if cake_state.grid[row][col]:
                    x = GRID_X + col * (CELL_SIZE + MARGIN) + (CELL_SIZE - CAKE_WIDTH) // 2
                    y = GRID_Y + row * (CELL_SIZE + MARGIN) + (CELL_SIZE - CAKE_HEIGHT) // 2
                    draw_cake(screen, x, y, cake_state.grid[row][col])

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
                        if cake_state.grid[row][col] is None:
                            cake_state.grid[row][col] = []
                        cake_state.grid[row][col].extend(available_cakes.pop(selected_cake_index))
                        available_cakes.append(generate_random_cake())
                        selected_cake_index = None
                        cake_state.apply_operator()

        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()