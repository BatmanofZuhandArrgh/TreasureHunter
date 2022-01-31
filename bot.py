
STARTING_SCORE = 100


class Bot:
    def __init__(self, position = (-1,-1)):
        self.action = [
            'left',
            'right',
            'down',
            'up'
        ]
        self.position = position
        self.state = "Searching"