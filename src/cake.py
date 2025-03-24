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

        # Caso não haja fatia com cor diferente, retorna ela mesma para que a fatia não se perca
        return new_slice

    def remove_single_slice(self, target_slice):
        """Remove apenas uma fatia específica pela cor."""
        for i, slice_obj in enumerate(self.slices):
            if slice_obj.equals(target_slice):
                del self.slices[i]
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
