# libs: Matplotlib, PyQt, Seaborn, Pandas
# graphviz?
from graphviz import Digraph as Tree
from Person import Person as p
from Family import Family as f


class graph_representation:

    node_color = {
        "default": '#E2C94B',
        "focused": '#764141',
        "selected": '#A94949',
    }

    def get_color(focus, selected):
        if selected:
            return graph_representation.node_color['selected']
        if focus >= 0:
            return graph_representation.node_color['focused']
        return graph_representation.node_color['default']

    def __init__(self, data=None):
        self.data = data
        self.current_level = set()

    def send_data(self, data):
        self.data = data

    def get_originless_partners(self, idn):
        partners = self.get_partners(idn)
        result = set()
        if partners is not None:
            for partner_id in partners:
                partner = self.data[partner_id]
                if partner.origin is None:
                    result.add(partner_id)
        return result

    def get_partners(self, idn):
        fam_c_ids = self.data[idn].family_connections
        if fam_c_ids is None:
            return None
        else:
            ids = set()
            for fam_c_id in fam_c_ids:
                family = self.data[fam_c_id]
                if family.head == idn:
                    ids.add(family.partner)
                else:
                    ids.add(family.head)
        return ids

    def find_top(self):
        for entry in self.data.values():
            if isinstance(entry, p) and entry.origin is None:
                part_with_origin = False
                partners = self.get_partners(entry.idn)
                if partners is not None:
                    for partner_id in list(partners):
                        partner = self.data[partner_id]
                        if partner.origin is not None:
                            part_with_origin = True
                            break
                if not part_with_origin:
                    self.current_level.add(entry.idn)

    def draw_node(self, el):
        s = 'filled'
        # if they have a family
        if el.family_connections is not None:
            for fam_idn in el.family_connections:
                # family nodes are drawn twice!!! TODO
                self.subtree.node(fam_idn, shape="point")
                c = graph_representation.get_color(el.focus, el.select)
                self.subtree.node(el.idn, el.clean_display(), style=s, color=c)
        else:
            c = graph_representation.get_color(el.focus, el.select)
            self.subtree.node(el.idn, el.clean_display(), style=s, color=c)

    def get_children(self, el, children):
        # if they have a family
        if el.family_connections is not None:
            for fam_idn in el.family_connections:
                family = self.data[fam_idn]
                # if there are children in this family
                if family.family_connections is not None:
                    for c in family.family_connections:
                        children.add(c)
        return children

    def get_side_nodes(self, el, cur_origls_p, diff=None):
        originless = self.get_originless_partners(el.idn)
        if diff is not None:
            originless = originless.difference(diff)
        cur_origls_p = cur_origls_p.union(originless)
        return cur_origls_p

    def focus_children(self, children, value=0):
        if len(children) > 0:
            for child_id in children:
                child = self.data[child_id]
                child.focus = value
                self.focus_children(self.get_children(child, set()), value)

    def focus_parents(self, person, current_focus):
        if person.origin is not None:
            bloodline = self.data[person.origin]
            right_side = self.data[bloodline.head]
            if current_focus > -1:
                right_side.focus = current_focus + 1
            else:
                right_side.focus = current_focus
            self.focus_parents(right_side, current_focus + 1)
            left_side = self.data[bloodline.partner]
            left_side.focus = current_focus
            self.focus_parents(left_side, current_focus)

    def select_node(self, idn, deselect=False):
        selected = self.data[idn]
        if not deselect:
            selected.focus = 0
            selected.select = True
            self.focus_children(self.get_children(selected, set()))
            self.focus_parents(selected, 0)
        else:
            selected.focus = -1
            selected.select = False
            self.focus_children(self.get_children(selected, set()), -1)
            self.focus_parents(selected, -1)
        # self.data[idn] = selected

    def deselect(self):
        for entry in self.data.values():
            if isinstance(entry, p) and entry.select:
                self.select_node(entry.idn, deselect=True)
                break

    def get_mark_direction(self, person):
        children = self.get_children(person, set())
        for child_id in children:
            child = self.data[child_id]
            if child.focus > -1:
                child_fam = self.data[child.origin]
                if child_fam.head == person.idn:
                    partner = child_fam.partner
                    return ('R', partner, self.data[partner].origin)
        return ('?', '?', '?')

    # takes set of ids returns tuple(A,
    # A - Right_side siblings, with selected F on last place
    def sort_data(self, data):
        data = list(data)
        result = []
        tuples_to_sort = []
        selected_flag = False
        siblings = {}  # famid -> list[id]
        for p_id in data:
            person = self.data[p_id]
            if person.origin is not None:
                focus = person.focus
                if focus == -1:
                    print('pid', p_id)
                    sibs = siblings.get(person.origin, None)
                    if sibs is not None:
                        siblings[person.origin] = sibs.append(p_id)
                        print('add')
                    else:
                        siblings[person.origin] = [p_id]
                        print('new')
                elif not selected_flag:
                    # get marked children and check what is the connection
                    s, part, p_orig = self.get_mark_direction(person)
                    if s == 'R':
                        tup = (p_id, focus, person.origin, part, p_orig)
                        tuples_to_sort.append(tup)
                else:
                    result.append(p_id)
        for tup in tuples_to_sort:
            lst = siblings[tup[2]]
            lst.append(tup[0])
            lst.append(tup[3])
            if siblings.get(tup[4], None) is not None:
                lst += siblings[tup[4]]
            result += lst
        print("TPL:\n", tuples_to_sort)
        print("Res:\n", result)

    def create_node(self, orig, next_lv, guardian=None):
        if guardian is None:
            data = self.current_level
            self.sort_data(data)
        else:
            data = guardian
        # self.sort_data(data)
        # for el in data:
        while not len(data) == 0:
            el = self.data[data.pop()]
            orig = self.get_side_nodes(el, orig, guardian)
            next_lv = self.get_children(el, next_lv)
            self.draw_node(el)
        if guardian is None:
            self.current_level = set()
            return (orig, next_lv)
        return next_lv

    def create_nodes(self):
        # TODO make sure the children are under their parents
        # maybe change set to list or something
        print("Current lv:" + str(self.current_level))
        next_level = set()
        originless_part = set()
        self.subtree = Tree()
        self.subtree.attr(rank='same')
        o, nl = self.create_node(originless_part, next_level)
        originless_part, next_level = o, nl
        ptnrs_g = originless_part
        next_level = self.create_node(originless_part, next_level, ptnrs_g)
        self.tree.subgraph(self.subtree)
        if len(next_level) != 0:
            self.current_level = next_level
            self.create_nodes()

    def create_connections(self):
        for entry in self.data.values():
            if isinstance(entry, f):
                self.tree.edge(entry.head, entry.idn, arrowhead="none")
                self.tree.edge(entry.idn, entry.partner, arrowhead="none")
                if entry.family_connections is not None:
                    for c in entry.family_connections:
                        self.tree.edge(entry.idn, c)

    def show(self):
        self.tree = Tree()
        self.find_top()
        # sort by ranks
        self.create_nodes()
        self.create_connections()
        self.tree.view()
