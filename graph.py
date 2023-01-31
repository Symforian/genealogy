"""
    Contains graph representation.
    Is responsible for:

    Drawing nodes and edges.

    Sorting nodes.

    Focus select.

    Using graphviz to generate image.
"""
from graphviz import Digraph as Tree
from person import Person
from family import Family


class GraphRepresentation:

    NODE_COLOR = {
        "default": '#E2C94B',
        "focused": '#764141',
        "selected": '#A94949',
    }
    """Map program's description of node's color representation
    to proper color."""

    def get_color(focus, selected):
        """Map focus integer from person to color."""
        if selected:
            return GraphRepresentation.NODE_COLOR['selected']
        if focus >= 0:
            return GraphRepresentation.NODE_COLOR['focused']
        return GraphRepresentation.NODE_COLOR['default']

    def __init__(self, data=None):
        """Create a new graph representation.

        If `data` is `None`, the representation's enviroment is empty.
        """
        self.data = data
        self.current_level = set()
        self.selected = False

    def send_data(self, data):
        self.data = data

    def draw_node(self, el):
        """Draw node from person class element and it's family node if exists.

        Argument:

        *el* -- element which node will be drawn
        """
        s = 'filled'
        if len(el.family_connections):
            for fam_idn in el.family_connections:
                self.subtree.node(fam_idn, shape="point")
                c = GraphRepresentation.get_color(el.focus, el.select)
                self.subtree.node(el.idn, el.clean_display(), style=s, color=c)
        else:
            c = GraphRepresentation.get_color(el.focus, el.select)
            self.subtree.node(el.idn, el.clean_display(), style=s, color=c)

    def sort_current_level(self):
        pass

    def get_current_level_originless_partners(self):
        """Return set of people who do not have origin family specified."""
        result = set()
        for p_id in self.current_level:
            originless_partners = self.data.get_originless_partners(p_id)
            result |= originless_partners
        return result

    def focus_children(self, children, value=0):
        """
            Change focus value of children to the given value.
            Then the same to children's children and so on.

        Arguments:

        *children* -- set of children to focus on.

        *value* -- optional value to change children value.
        """
        if len(children) > 0:
            for child_id in children:
                child = self.data.entries()[child_id]
                child.focus = value
                self.focus_children(self.data.get_children(child), value)

    def focus_parents(self, person, current_focus):
        """
            Change focus value of ascendants to the proper value.
            Then the same to ascendants's ascendants and so on.

        Arguments:

        *person* -- person whose parents we want to focus.

        *current_focus* -- current focus value to pass on ascendants.
        """
        if person.origin is not None:
            bloodline = self.data.entries()[person.origin]
            right_side = self.data.entries()[bloodline.head]
            if current_focus > -1:
                right_side.focus = current_focus + 1
            else:
                right_side.focus = current_focus
            self.focus_parents(right_side, current_focus + 1)
            left_side = self.data.entries()[bloodline.partner]
            left_side.focus = current_focus
            self.focus_parents(left_side, current_focus)

    def select_node(self, idn, deselect=False):
        """
            Change node's color.
            Colors straight line ascendants and descendants.

        Arguments:

        *idn* -- person who focus and select values we are changing.

        *deselect* -- if `True` clears select and focus values.
        """
        selected = self.data.entries()[idn]
        if not deselect:
            selected.focus = 0
            selected.select = True
            self.focus_children(self.data.get_children(selected))
            self.focus_parents(selected, 0)
        else:
            selected.focus = -1
            selected.select = False
            self.focus_children(self.data.get_children(selected), -1)
            self.focus_parents(selected, -1)

    def deselect(self):
        """Set all nodes' color to default."""
        for entry in self.data.entries().values():
            if isinstance(entry, Person) and entry.select:
                self.select_node(entry.idn, deselect=True)
                break

    def draw_level_return_next(self):
        """Draw current row of nodes."""
        next_lv = set()
        for el_id in self.current_level:
            el = self.data.entries()[el_id]
            next_lv |= self.data.get_children(el)
            print(self.data.entries()[el_id].name
                  + self.data.entries()[el_id].surname)
            self.draw_node(el)
        return next_lv

    def return_next_level(self):
        """Draw current row of nodes."""
        next_lv = set()
        for el_id in self.current_level:
            el = self.data.entries()[el_id]
            next_lv |= self.data.get_children(el)
        return next_lv

    def create_nodes(self):
        """
            Create nodes. Manage subtrees (rows).
        """
        next_level = set()
        originless = self.get_current_level_originless_partners()
        self.current_level |= originless
        self.subtree = Tree()
        self.subtree.attr(rank='same', ordering='out')
        next_level = self.draw_level_return_next()
        self.tree.subgraph(self.subtree)
        if len(next_level) != 0:
            self.current_level = next_level
            self.create_nodes()

    def create_connections(self):
        """Draw edges."""
        for entry in self.data.entries().values():
            if isinstance(entry, Family):
                self.tree.edge(entry.head, entry.idn, arrowhead="none")
                self.tree.edge(entry.idn, entry.partner, arrowhead="none")
                if len(entry.family_connections):
                    for c in entry.family_connections:
                        self.tree.edge(entry.idn, c)

    def show(self, just_show=False):
        """Display proper tree.
           If `just_show` is `False` return the tree instead.
        """
        self.tree = Tree()
        self.current_level = self.data.find_top()
        self.selected = False
        self.create_nodes()
        self.create_connections()

        if just_show:
            self.tree.view()
        else:
            return self.tree.render(format='jpeg')
