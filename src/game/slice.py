class Slice:
    def __init__(self, color, color_name):
        self.color = color
        self.color_name = color_name

    def equals(self, other_slice):
        return self.color is other_slice.color and self.color_name == other_slice.color_name
