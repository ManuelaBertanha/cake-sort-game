from cake import Cake, SLICE_COUNT


class CakeState:
    def __init__(self, grid):
        self.grid = [[cell if isinstance(cell, Cake) else None for cell in row] for row in grid]

    def is_valid(self, x, y):
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

    def merge_cakes(self):
        changed = True
        safety_counter = 0
        max_iterations = 100

        while changed and safety_counter < max_iterations:
            changed = False
            safety_counter += 1
            for x in range(len(self.grid)):
                for y in range(len(self.grid[0])):
                    if not self.grid[x][y]:
                        continue
                    current_cake = self.grid[x][y]

                    # Verifica os bolos adjacentes
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if self.is_valid(nx, ny) and self.grid[nx][ny]:
                            neighbor_cake = self.grid[nx][ny]

                            # Combina fatias de cores iguais
                            for slice in current_cake.slices[:]:  # Itera sobre uma cópia para evitar problemas ao modificar a lista
                                if any(ns.color == slice.color for ns in neighbor_cake.slices):
                                    neighbor_cake.add_slice(slice)  # Adiciona a fatia ao bolo vizinho
                                    current_cake.slices.remove(slice)  # Remove a fatia do bolo original
                                    changed = True

                            # Verifica se o bolo vizinho agora está completo
                            if neighbor_cake.is_complete():
                                break

            if safety_counter >= max_iterations:
                print("Merge interrompido para evitar loop infinito.")

    def apply_operator(self):
        self.merge_cakes()
