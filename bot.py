
STARTING_SCORE = 100


class Bot:
    def __init__(self, position = (-1,-1)):
        self.action = [
            'left',
            'right',
            'down',
            'up',
            'up-left',
            'up-right',
            'down-left',
            'down-right'
        ]
        self.position = position
        self.state = "Searching"