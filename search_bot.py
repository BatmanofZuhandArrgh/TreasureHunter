from operator import pos
from bot import Bot
from data_structure.node import Node

class tree_search_bot(Bot):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.root = Node(position = position, parent_node=None,cost2reach=0)
        self.outer_leaves = [self.root]

    def query_surrounding(self):
        pass

class breadth_first_tree_search(tree_search_bot):
    def __init__(self, position) -> None:
        super(breadth_first_tree_search, self).__init__(position)
        print(position)

    def query_surrounding(self, fringe):
        new_outer_leaves = [] #Reset outer leaves
        new_children_positions = []
        for index, parent_node in enumerate(self.outer_leaves):
            for jndex, child_position in enumerate(len(fringe[index])):
                child = Node(
                    position = child_position,
                    parent_node=parent_node,
                    cost2reach=0, #TODO, fixlater
                    )
                parent_node.children.append(child)
                new_outer_leaves.append(child)
                new_children_positions.append((parent_node.position, child_position))

        self.outer_leaves = new_outer_leaves

        return new_children_positions