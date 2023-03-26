"""
    Contains graph representation.
    Is responsible for:

    Sorting and placing nodes with proper data.

    Focus select.
"""
from person import Person
from family import Family
from tree_pillow import Tree


class GraphRepresentation:

    MODE = 1

    MODES = {
        "GRAPHVIZ": 0,
        "PILLOW": 1,
    }

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

    def check_mode(mode_name):
        return GraphRepresentation.MODE == GraphRepresentation.MODES[mode_name]

    def __init__(self, data=None):
        """Create a new graph representation.

        If `data` is `None`, the representation's enviroment is empty.
        """
        self.data = data
        self.current_level = list()
        self.drawn_entries = set()
        self.tree = Tree()
        self.selected = False
        self.current_depth = 0
        self.filetext = list()

    def send_data(self, data):
        self.data = data

    def draw_node(self, el):
        """Draw node from person class element and it's family node if exists.

        Argument:

        *el* -- element which node will be drawn
        """
        if len(el.family_connections):
            for fam_idn in el.family_connections:
                self.tree.draw_point(fam_idn)
                self.drawn_entries.add(fam_idn)
        c = GraphRepresentation.get_color(el.focus, el.select)
        self.tree.draw_node(el.idn, el.clean_display(), color=c)
        self.drawn_entries.add(el.idn)

    def sort_current_level(self):
        pass

    def add_current_level_originless_partners(self):
        """Inserts people who do not have origin specified to current_level"""
        result = list()
        for p_id in self.current_level:
            result.append(p_id)
            originless_partners = self.data.get_originless_partners(p_id)
            for originless_partner in originless_partners:
                if originless_partner not in self.drawn_entries:
                    result.append(originless_partner)
        self.current_level = result

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
            if bloodline.head:
                right_side = self.data.entries()[bloodline.head]
            if current_focus > -1:
                right_side.focus = current_focus + 1
            else:
                right_side.focus = current_focus
            self.focus_parents(right_side, current_focus + 1)
            if bloodline.partner:
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
        for entry_idn, entry in self.data.get_persons():
            if entry.select:
                self.select_node(entry_idn, deselect=True)
                break

    def add_families_to_current_level(self, next_level, current_level_ids):
        for person_id in self.current_level:
            person = self.data.entries()[person_id]
            if person.depth != self.current_depth:
                next_level.append(person_id)
                continue
            families = self.data.get_person_families(person)
            if len(families):
                current_level_ids += [fam for fam in families
                                      if fam not in self.drawn_entries and
                                      fam not in current_level_ids]
            elif person_id not in self.drawn_entries:
                current_level_ids.append(person_id)

    def draw_level_return_next(self):
        """Draw current row of nodes."""
        next_lv = list()
        current_lv_ids = list()
        self.add_families_to_current_level(next_lv, current_lv_ids)
        for id in current_lv_ids:
            entry = self.data.entries()[id]
            if isinstance(entry, Family):
                children = self.data.get_children_from_family(entry)
                if len(children):
                    next_lv += [child for child in children
                                if child not in self.drawn_entries]
                family_not_drawn = entry.idn not in self.drawn_entries
                if entry.head:
                    entry_obj = self.data.entries()[entry.head]
                    self.draw_node(entry_obj)
                    self.filetext.append(
                        f"""{self.current_depth}|{entry.head}| {entry_obj.name} {entry_obj.surname}\n""")
                if entry.partner:
                    entry_obj = self.data.entries()[entry.partner]
                    self.draw_node(entry_obj)
                    self.filetext.append(
                        f"""{self.current_depth}|{entry.partner}| {entry_obj.name} {entry_obj.surname}\n""")
                if family_not_drawn and entry.idn in self.drawn_entries:
                    self.draw_edges(entry)
            elif isinstance(entry, Person):
                entry_obj = self.data.entries()[id]
                self.draw_node(self.data.entries()[id])
                self.filetext.append(
                    f"""{self.current_depth}|{id}| {entry_obj.name} {entry_obj.surname}\n""")
        return next_lv

    def return_next_level(self):
        """Draw current row of nodes."""
        next_lv = list()
        for el_id in self.current_level:
            el = self.data.entries()[el_id]
            children = self.data.get_children(el)
            next_lv.append([child for child in children
                           if child not in self.drawn_entries])
        return next_lv

    def create_nodes(self):
        """
            Create nodes. Manage subtrees (rows).
        """
        next_level = list()
        if GraphRepresentation.check_mode("PILLOW"):
            self.subtree = self.tree
        elif GraphRepresentation.check_mode("GRAPHVIZ"):
            self.subtree = Tree()
        next_level = self.draw_level_return_next()
        #self.tree.add_subtree(self.subtree)
        if len(next_level) != 0:
            self.current_depth -= 1
            self.current_level = next_level
            if GraphRepresentation.check_mode("PILLOW"):
                self.tree.draw_next_line()
            self.create_nodes()

    def draw_edges(self, family: Family):
        """Draw edges."""
        if family.head:
            self.tree.draw_arrowless_edge(family.head, family.idn)
        if family.partner:
            self.tree.draw_arrowless_edge(family.idn, family.partner)
        if len(family.family_connections):
            for c in family.family_connections:
                self.tree.draw_edge(family.idn, c)

    def push_up(self, idn, offset):
        if not idn:
            return -1
        self.data.entries()[idn].depth += offset
        entry = self.data.entries()[idn]
        if not entry.origin:
            return self.data.entries()[idn].depth
        family_origin = self.data.entries()[entry.origin]
        return max(self.push_up(family_origin.head, offset),
                   self.push_up(family_origin.partner, offset))

    def fix_family_depth(self):
        max_depth = 0
        for _, family in self.data.get_families():
            if not family.head or not family.partner:
                continue
            head_depth = self.data.entries()[family.head].depth
            partner_depth = self.data.entries()[family.partner].depth
            tmp = -1
            if head_depth < partner_depth:
                tmp = self.push_up(family.head, partner_depth - head_depth)
            elif partner_depth < head_depth:
                tmp = self.push_up(family.partner, head_depth - partner_depth)
            max_depth = max(max_depth, tmp)
        return max_depth

    def set_current_tree_depth(self):
        current_depth = 0
        for entry_idn in self.current_level:
            entry_depth = self.set_person_depth(entry_idn, 0)
            current_depth = max(entry_depth, current_depth)
        self.current_depth = max(current_depth, self.fix_family_depth())

    def set_person_depth(self, person_id, depth):
        entry = self.data.entries()[person_id]
        if not entry.family_connections:
            self.data.entries()[person_id].depth = depth
            return depth
        max_depth = depth
        for fam_idn in entry.family_connections:
            family = self.data.entries()[fam_idn]
            if family.family_connections:
                child_id_result = list()
                for child_id in family.family_connections:
                    child_depth = self.set_person_depth(child_id, depth + 1)
                    child_id_result.append((child_id, child_depth))
                    max_depth = max(child_depth, max_depth)
                for child_id, result in child_id_result:
                    if result < max_depth:
                        offset = (max_depth - result) + depth + 1
                        self.set_person_depth(child_id, offset)
                max_depth += 1
        self.data.entries()[person_id].depth = max_depth
        return max_depth

    def show(self, just_show=False):
        """Display proper tree.
           If `just_show` is `False` return the tree instead.
        """
        self.tree = Tree()
        self.drawn_entries = set()
        self.current_level = self.data.find_top()
        self.set_current_tree_depth()
        self.selected = False
        self.create_nodes()
        with open("log.txt", 'w') as logger:
            logger.writelines(self.filetext)
        return self.tree.get_result(just_show)
