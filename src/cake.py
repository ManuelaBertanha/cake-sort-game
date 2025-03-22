from slice import Slice

SLICE_COUNT = 6  # Número máximo de fatias por bolo


class Cake:
    def __init__(self, slices=None):
        self.slices = slices if slices else []

    def add_slice(self, new_slice):
        if len(self.slices) < SLICE_COUNT:  # Garantir que o bolo não exceda o número máximo de fatias
            self.slices.append(new_slice)

    def replace_slice(self, new_slice):
        """Substitui a primeira fatia com uma cor diferente de new_slice.color.
        Retorna a fatia removida para ser reaproveitada."""

        # Encontra a primeira fatia com uma cor diferente da nova fatia
        for i, slice_obj in enumerate(self.slices):
            if slice_obj.color != new_slice.color:
                # Substitui a fatia encontrada
                removed_slice = self.slices[i]
                self.slices[i] = new_slice  # Substitui pela nova fatia
                return removed_slice  # Retorna a fatia removida

        # Caso não haja fatia com cor diferente (teoricamente improvável)
        return None

    def remove_slice(self, color):
        """Remove todas as fatias de uma cor específica de um bolo."""
        self.slices = [s for s in self.slices if s.color != color]

    def remove_single_slice(self, color):
        """Remove apenas uma fatia específica pela cor."""
        for s in self.slices:
            if s.color == color:
                self.slices.remove(s)
                break

    def is_complete(self):
        if len(self.slices) == SLICE_COUNT:
            # Verifica se todas as fatias têm a mesma cor
            return all(slice.color == self.slices[0].color for slice in self.slices)
        return False

    def get_colors(self):
        return [slice.color for slice in self.slices]

    def count_slices(self):
        return len(self.slices)
