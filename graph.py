# libs: Matplotlib, PyQt, Seaborn, Pandas
# graphviz?
from graphviz import Digraph as Tree
from Person import Person as p
from Family import Family as f


class graph_representation:
    node_attr = {
    }
    child_attr = {
    }
    marr_attr = {
        "style": "tapered",
        "arrowhead": "none"
    }

    def __init__(self, data=None):
        self.data = data
        self.current_level = set()

    def upload_data(self, data):
        self.data = data

    def find_top(self):
        for entry in self.data.values():
            if isinstance(entry, p) and entry.origin is None:
                self.current_level.add(entry.idn)

    def create_nodes(self):
        next_level = set()
        with self.tree.subgraph() as level:
            level.attr(rank='same')
            while not len(self.current_level) == 0:
                el = self.data[self.current_level.pop()]
                if el.family_connections is not None:
                    for fam_idn in el.family_connections:
                        family = self.data[fam_idn]
                        level.node(fam_idn, shape="point")
                        level.node(el.idn, el.clean_display())
                        for c in family.family_connections:
                            print(next_level)
                            next_level.add(c)
                else:
                    level.node(el.idn, el.clean_display())
        if len(next_level) != 0:
            self.current_level = next_level
            self.create_nodes()

    def create_connections(self):
        for entry in self.data.values():
            if isinstance(entry, f):
                self.tree.edge(entry.head, entry.idn, arrowhead="none")
                self.tree.edge(entry.idn, entry.partner, arrowhead="none")
                for c in entry.family_connections:
                    self.tree.edge(entry.idn, c)

    def show(self):
        self.tree = Tree()
        self.find_top()
        # sort by ranks
        self.create_nodes()
        # self.create_nodes()
        self.create_connections()
        self.tree.view()
