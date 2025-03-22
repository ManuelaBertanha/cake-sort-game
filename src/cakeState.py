from cake import Cake, SLICE_COUNT


class CakeState:
    def __init__(self, grid, game_state):
        self.grid = [[cell if isinstance(cell, Cake) else None for cell in row] for row in grid]
        self.game_state = game_state

    def update_score(self, cake):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] is cake:
                    self.grid[row][col] = None
                    self.game_state.score += 1

    def analyze_and_merge(self, current_cake, neighbor_cake):
        """Analisa as cores e realiza a combinação entre dois bolos."""
        # Conta as fatias por cor para os bolos atual e vizinho
        slice_counts_current = {color: sum(1 for s in current_cake.slices if s.color == color) for color in
                                current_cake.get_colors()}
        slice_counts_neighbor = {color: sum(1 for s in neighbor_cake.slices if s.color == color) for color in
                                 neighbor_cake.get_colors()}

        # Identifica as cores em comum
        common_colors = set(slice_counts_current.keys()) & set(slice_counts_neighbor.keys())

        for color in common_colors:
            # Soma as fatias de mesma cor de ambos os bolos
            total_current = slice_counts_current[color]
            total_neighbor = slice_counts_neighbor[color]

            # Decide qual bolo fica com mais fatias dessa cor
            if total_current > total_neighbor:
                # O bolo atual assimila as fatias dessa cor do bolo vizinho
                slices_to_transfer = [s for s in neighbor_cake.slices if s.color == color][:total_neighbor]
                space_available = SLICE_COUNT - current_cake.count_slices()
                if len(slices_to_transfer) > space_available:
                    slices_to_transfer = slices_to_transfer[:space_available]

                for slice_obj in slices_to_transfer:
                    neighbor_cake.remove_single_slice(slice_obj.color)
                    if len(current_cake.slices) < SLICE_COUNT:
                        current_cake.add_slice(slice_obj)
                    else:
                        removed_slice = current_cake.replace_slice(slice_obj)
                        if removed_slice:
                            neighbor_cake.add_slice(removed_slice)  # Adiciona a fatia removida ao bolo de origem
                if len(neighbor_cake.slices) == 0:
                    for x in range(len(self.grid)):
                        for y in range(len(self.grid[0])):
                            if self.grid[x][y] is neighbor_cake:  # Localiza e remove o bolo do grid
                                self.grid[x][y] = None
                if current_cake.is_complete():
                    self.update_score(current_cake)

            elif total_neighbor > total_current:
                # O bolo vizinho assimila as fatias dessa cor do bolo atual
                slices_to_transfer = [s for s in current_cake.slices if s.color == color][:total_current]
                space_available = SLICE_COUNT - neighbor_cake.count_slices()
                if len(slices_to_transfer) > space_available:
                    slices_to_transfer = slices_to_transfer[:space_available]

                for slice_obj in slices_to_transfer:
                    current_cake.remove_single_slice(slice_obj.color)  # current_cake.slices.remove(slice_obj)
                    if len(neighbor_cake.slices) < SLICE_COUNT:
                        neighbor_cake.add_slice(slice_obj)
                    else:
                        removed_slice = neighbor_cake.replace_slice(slice_obj)
                        if removed_slice:
                            current_cake.add_slice(removed_slice)
                if len(current_cake.slices) == 0:
                    for x in range(len(self.grid)):
                        for y in range(len(self.grid[0])):
                            if self.grid[x][y] is current_cake:
                                self.grid[x][y] = None
                if neighbor_cake.is_complete():
                    self.update_score(neighbor_cake)

            else:
                # Empate: tenta juntar todas as fatias no bolo que tenha espaço suficiente
                total_slices = total_current + total_neighbor  # Total das fatias da cor atual

                # Verifica quantas fatias cabem em cada bolo
                space_in_current = SLICE_COUNT - current_cake.count_slices()
                space_in_neighbor = SLICE_COUNT - neighbor_cake.count_slices()

                if total_slices <= space_in_current:
                    # Todas as fatias cabem no bolo atual
                    slices_to_transfer = [s for s in neighbor_cake.slices if s.color == color]
                    for slice_obj in slices_to_transfer:
                        neighbor_cake.remove_single_slice(slice_obj.color)
                        if len(current_cake.slices) < SLICE_COUNT:
                            current_cake.add_slice(slice_obj)
                        else:
                            # Substituição se o bolo atual estiver cheio
                            removed_slice = current_cake.replace_slice(slice_obj)
                            if removed_slice:
                                neighbor_cake.add_slice(removed_slice)  # Adiciona a fatia substituída ao bolo vizinho
                    if len(neighbor_cake.slices) == 0:
                        for x in range(len(self.grid)):
                            for y in range(len(self.grid[0])):
                                if self.grid[x][y] is neighbor_cake:
                                    self.grid[x][y] = None
                    if current_cake.is_complete():
                        self.update_score(current_cake)

                elif total_slices <= space_in_neighbor:
                    # Todas as fatias cabem no bolo vizinho
                    slices_to_transfer = [s for s in current_cake.slices if s.color == color]
                    for slice_obj in slices_to_transfer:
                        current_cake.remove_single_slice(slice_obj.color)
                        if len(neighbor_cake.slices) < SLICE_COUNT:
                            neighbor_cake.add_slice(slice_obj)
                        else:
                            # Substituição se o bolo vizinho estiver cheio
                            removed_slice = neighbor_cake.replace_slice(slice_obj)
                            if removed_slice:
                                current_cake.add_slice(removed_slice)  # Adiciona a fatia substituída ao bolo atual
                    if len(current_cake.slices) == 0:
                        for x in range(len(self.grid)):
                            for y in range(len(self.grid[0])):
                                if self.grid[x][y] is current_cake:
                                    self.grid[x][y] = None
                    if neighbor_cake.is_complete():
                        self.update_score(neighbor_cake)

                else:
                    # Nem todas as fatias cabem num único bolo; move o máximo possível
                    if space_in_current >= space_in_neighbor:
                        # Dá preferência ao bolo atual
                        slices_to_transfer = [s for s in neighbor_cake.slices if s.color == color][:space_in_current]
                        for slice_obj in slices_to_transfer:
                            neighbor_cake.remove_single_slice(slice_obj.color)
                            if len(current_cake.slices) < SLICE_COUNT:
                                current_cake.add_slice(slice_obj)
                            else:
                                # Substituição se o bolo atual estiver cheio
                                removed_slice = current_cake.replace_slice(slice_obj)
                                if removed_slice:
                                    neighbor_cake.add_slice(removed_slice)
                        if len(neighbor_cake.slices) == 0:
                            for x in range(len(self.grid)):
                                for y in range(len(self.grid[0])):
                                    if self.grid[x][y] is neighbor_cake:
                                        self.grid[x][y] = None
                        if current_cake.is_complete():
                            self.update_score(current_cake)

                    else:
                        # Dá preferência ao bolo vizinho
                        slices_to_transfer = [s for s in current_cake.slices if s.color == color][:space_in_neighbor]
                        for slice_obj in slices_to_transfer:
                            current_cake.remove_single_slice(slice_obj.color)
                            if len(neighbor_cake.slices) < SLICE_COUNT:
                                neighbor_cake.add_slice(slice_obj)
                            else:
                                # Substituição se o bolo vizinho estiver cheio
                                removed_slice = neighbor_cake.replace_slice(slice_obj)
                                if removed_slice:
                                    current_cake.add_slice(removed_slice)
                        if len(current_cake.slices) == 0:
                            for x in range(len(self.grid)):
                                for y in range(len(self.grid[0])):
                                    if self.grid[x][y] is current_cake:
                                        self.grid[x][y] = None
                        if neighbor_cake.is_complete():
                            self.update_score(neighbor_cake)

    def is_valid(self, x, y):
        """Verifica se uma posição no grid é válida."""
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

    def find_adjacent_cakes(self, x, y):
        """Encontra bolos adjacentes ao bolo na posição (x, y)."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacent_cakes = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny) and self.grid[nx][ny]:
                adjacent_cakes.append(((nx, ny), self.grid[nx][ny]))
        return adjacent_cakes

    def merge_cakes(self, x, y):
        """Realiza as verificações nas 4 direções e combina bolos adjacentes."""
        current_cake = self.grid[x][y]
        if not current_cake:
            return

        adjacent_cakes = self.find_adjacent_cakes(x, y)
        for (nx, ny), neighbor_cake in adjacent_cakes:
            self.analyze_and_merge(current_cake, neighbor_cake)  # Analisa e combina com o bolo adjacente

    def apply_operator(self, x, y):
        """Aplica o operador para combinar bolos adjacentes à posição (x, y)."""
        self.merge_cakes(x, y)
