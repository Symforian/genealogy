"""
    Wraps graphviz for graph/tree representation
    Is responsible for:

    Drawing nodes and edges.

    Using graphviz to generate image.
"""
from graphviz import Digraph as InternalTree


class Tree:

    def __init__(self):
        self.__tree = InternalTree()
        self.__tree.attr(rank="same", ordering="in")

    def draw_edge(self, node_a, node_b):
        self.__draw_edge(node_a, node_b)

    def draw_arrowless_edge(self, node_a, node_b):
        self.__draw_edge(node_a, node_b, "none")

    def __draw_edge(self, node_a, node_b, ah=""):
        self.__tree.edge(node_a, node_b, arrowhead=ah)

    def draw_node(self, node, text, color):
        s = 'filled'
        self.__tree.node(node, text, style=s, color=color)

    def draw_point(self, node):
        self.__tree.node(node, shape="point")

    def add_subtree(self, subtree):
        self.__tree.subgraph(subtree.__tree)

    def get_result(self, just_show=False):
        if just_show:
            self.__tree.view()
        else:
            return self.__tree.render(format='jpeg')
