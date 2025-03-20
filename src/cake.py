from slice import Slice

SLICE_COUNT = 6  # Número máximo de fatias por bolo


class Cake:
    def __init__(self, slices=None):
        self.slices = slices if slices else []

    def add_slice(self, new_slice):
        if len(self.slices) < SLICE_COUNT:  # Garantir que o bolo não exceda o número máximo de fatias
            self.slices.append(new_slice)

    def remove_slice(self, color):
        self.slices = [s for s in self.slices if s.color != color]

    def is_complete(self):
        if len(self.slices) == SLICE_COUNT:
            # Verifica se todas as fatias têm a mesma cor
            return all(slice.color == self.slices[0].color for slice in self.slices)
        return False

    def get_colors(self):
        return [slice.color for slice in self.slices]

    def count_slices(self):
        return len(self.slices)
