class Node():
    def __init__(self, position, parent_node, cost2reach) -> None:
        self.children = []
        self.position = position
        self.parent = parent_node
        self.cost = cost2reach