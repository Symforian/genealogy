# libs: Matplotlib, PyQt, Seaborn, Pandas
# graphviz?
from graphviz import Digraph as Tree
from Person import Person as p
from Family import Family as f


class graph_representation:

    def __init__(self, data=None):
        self.data = data
        self.current_level = set()

    def upload_data(self, data):
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

    def draw_nodes(self, el):
        # if they have a family
        if el.family_connections is not None:
            for fam_idn in el.family_connections:
                self.subtree.node(fam_idn, shape="point")
                self.subtree.node(el.idn, el.clean_display())
        else:
            self.subtree.node(el.idn, el.clean_display())

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

    def create_node(self, orig, next_lv, guardian=None):
        if guardian is None:
            data = self.current_level
        else:
            data = guardian
        while not len(data) == 0:
            el = self.data[data.pop()]
            orig = self.get_side_nodes(el, orig, guardian)
            next_lv = self.get_children(el, next_lv)
            self.draw_nodes(el)
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
        # self.create_nodes()
        self.create_connections()
        self.tree.view()
