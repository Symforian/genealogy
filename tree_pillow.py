"""
    Wraps pillow for graph/tree representation
    Is responsible for:

    Drawing nodes and edges.

    Using pillow to generate image.
"""
from copy import deepcopy
from PIL import Image, ImageDraw, ImageFont


class Tree:

    def __init__(self):
        self.__node_width = 50
        self.__node_height = 50
        self.__font_size = 12
        self.__node_spacing_y = 15
        self.__node_spacing_x = 10
        self.__y_pos = 0
        self.__x_pos = 0
        self.__tree = Image.new("RGB", (5000, 5000), "white")
        self.__drawer = ImageDraw.Draw(self.__tree)

    def draw_edge(self, node_a, node_b):
        return
        self.__draw_edge(node_a, node_b)

    def draw_arrowless_edge(self, node_a, node_b):
        return
        self.__draw_edge(node_a, node_b, "none")

    def __draw_edge(self, node_a, node_b, ah=""):
        return
        self.__tree.edge(node_a, node_b, arrowhead=ah)

    def draw_node(self, node, text, color):
        pos = deepcopy((self.__x_pos, self.__y_pos, self.__node_width, self.__node_height))
        self.__drawer.ellipse(pos, fill=color)
        try:
            self.__drawer.text((self.__x_pos, self.__y_pos), text=text, language="polish")
        except UnicodeEncodeError:
            print(f"Error encode\n")
        self.__x_pos = self.__x_pos + self.__node_width+self.__node_spacing_x
        return
        s = 'filled'
        self.__tree.node(node, text, style=s, color=color)

    def draw_point(self, node):
        return
        self.__tree.node(node, shape="point")

    def add_subtree(self, subtree):
        return
        self.__tree.subgraph(subtree.__tree)

    def draw_next_line(self):
        self.__y_pos+=self.__node_height + self.__node_spacing_y

    def get_result(self, just_show=False):
        self.__tree.save("pillow.jpeg")
        return "pillow.jpeg"
