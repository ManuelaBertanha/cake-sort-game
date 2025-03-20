class Slice:
    def __init__(self, color, id):
        self.color = color
        self.id = id

    def __eq__(self, other):
        return self.id == other.id
