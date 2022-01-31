from bot import Bot
from data_structure.node import Node

class tree_search_bot(Bot):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.root = Node(position = position, parent_node=None,cost2reach=0)
    
    def query_surrounding():
        pass

class breadth_first_tree_search(tree_search_bot):
    def __init__(self, position) -> None:
        super(breadth_first_tree_search, self).__init__(position)





