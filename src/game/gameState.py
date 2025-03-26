class GameState:
    def __init__(self):
        self.score = 0
        self.running = 0

    def end_game(self):
        self.running = 1

    """
    if self.running == 0: Game is running
    if self.running == 1: Player won the game
    if self.running == 2: Player quit the game
    """
