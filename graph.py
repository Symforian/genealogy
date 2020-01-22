'''
    Contains graph representation.
    Is responsible for:
    Drawing nodes and edges.
    Sorting nodes.
    Focus select.
    Using graphviz to generate image.
'''
from graphviz import Digraph as Tree
from person import Person as p
from family import Family as f


class graph_representation:

    node_color = {
        "default": '#E2C94B',
        "focused": '#764141',
        "selected": '#A94949',
    }

    def get_color(focus, selected):
        '''
            Maps focus integer from person to color
        '''
        if selected:
            return graph_representation.node_color['selected']
        if focus >= 0:
            return graph_representation.node_color['focused']
        return graph_representation.node_color['default']

    def __init__(self, data=None):
        self.data = data
        self.current_level = set()
        self.selected = False

    def send_data(self, data):
        self.data = data

    def draw_node(self, el):
        '''
            Draws node from person class element. Also draws family node.
        '''
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

    def get_current_level_originless_partners(self):
        '''
            Returns set of people who do not have origin family specified.
        '''
        result = set()
        for p_id in self.current_level:
            originless_partners = self.data.get_originless_partners(p_id)
            result |= originless_partners
        return result

    def focus_children(self, children, value=0):
        '''
            Change focus value of children to the given value.
            Then the same to children's children and so on.
        '''
        if len(children) > 0:
            for child_id in children:
                child = self.data.entries()[child_id]
                child.focus = value
                self.focus_children(self.data.get_children(child), value)

    def focus_parents(self, person, current_focus):
        '''
            Change focus value of ascendants to the proper value.
            Then the same to ascendants's ascendants and so on.
        '''
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
        '''
            Focuses on node changing it's color.
            Colors straight line ascendants and descendants.
        '''
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
        # self.data.entries()[idn] = selected

    def deselect(self):
        '''
            Clears focus value.
        '''
        for entry in self.data.entries().values():
            if isinstance(entry, p) and entry.select:
                self.select_node(entry.idn, deselect=True)
                break

    def get_mark_direction(self, person):
        '''
            Checks person's position to the selected node.
        '''
        children = self.data.get_children(person)
        if len(children) == 0:
            return ('R', '?', '?')
        for child_id in children:
            child = self.data.entries()[child_id]
            if child.focus > -1:
                child_fam = self.data.entries()[child.origin]
                if child_fam.head == person.idn:
                    partner = child_fam.partner
                    return ('R', partner, self.data.entries()[partner].origin)
                else:
                    return ('L', '?', '?')
        return ('?', '?', '?')

    def tuples_to_list(tuples_to_sort, siblings):
        '''
            Takes tuples of 3 and 5 and changes them to the list.
        '''
        result = []
        for tup in tuples_to_sort:
            lst = siblings.get(tup[2], [])
            siblings.pop(tup[2], None)
            lst += [tup[0]]
            if len(tup) > 3:
                lst += [tup[3]]
                lst += siblings.get(tup[4], [])
                siblings.pop(tup[4], None)
            result += lst
        for (fam_id, sibs_id_list) in siblings.items():
            result += sibs_id_list
        return result

    # takes set of ids returns tuple(A,
    # A - Right_side siblings, with selected F on last place
    def get_pos_row_partners(self, pid, row):
        '''
            Returns position of person, and partners.
        '''
        partn_list = []
        sp_pos = 'R'
        selected_person = self.data.entries()[pid]
        if selected_person.family_connections is not None:
            any_fc_id = selected_person.family_connections[0]
            any_fc = self.data.entries()[any_fc_id]
            if any_fc.partner == pid:
                sp_pos = 'L'
            for fc in selected_person.family_connections:
                if sp_pos == 'R':
                    partn_list += [fc.partner]
                    row.remove(fc.partner)
                else:
                    partn_list += [fc.head]
                    row.remove(fc.head)
        return (sp_pos, row, partn_list)

    def get_siblings(self, spidn, row):
        '''
            Returns siblings of person, and the rest of the row.
        '''
        sibs = []
        selected_person = self.data.entries()[spidn]
        if selected_person.origin is not None:
            sp_fam = self.data.entries()[selected_person.origin]
            for p_id in row:
                if self.data.entries()[p_id].origin == sp_fam:
                    sibs += [p_id]
            row -= sibs
        return (sibs, row)

    def sort_selected_row(self, spidn):
        '''
            Sorts the row in which, there is the selected person
        '''
        self.current_level -= spidn
        rest = list(self.current_level)
        (rest, ssibs) = self.get_siblings(spidn, rest)
        (pos, rest, par) = self.get_pos_row_partners(spidn, rest)
        result = []
        if pos == 'R':
            r = list(map(lambda x: [self.data.get_partners(x)]+[x], ssibs))

        else:
            r = list(map(lambda x: [x]+[self.data.get_partners(x)], ssibs))
        result = (lambda l: [item for sublist in l for item in sublist])(r)
        rest -= result
        result += [spidn]
        #TODO
        partn_list = par
        result += rest
        return result

    def sort_current_level(self):
        '''
            Sorts current row of nodes to:
            [SHS] SH SP [SPS]
            SH - selected head node
            SP - selected partner node
            [Sx] - siblings of x
        '''
        print('Start:', list(self.current_level))
        was_selected_person_printed = self.selected
        (result, tuples_to_sort) = ([], [])
        siblings = {}  # famid -> list[id]
        for p_id in list(self.current_level):
            person = self.data.entries()[p_id]
            if (person.focus, person.origin) == (-1, None):
                result.append(p_id)
            elif person.focus == -1:
                sibs = siblings.get(person.origin, []) + [p_id]
                siblings.update({person.origin: sibs})
            elif not was_selected_person_printed:
                # get marked children and check what is the connection
                pos, part, p_orig = self.get_mark_direction(person)
                if (pos, part, person.origin) == ('R', '?', None):
                    if p_orig is not None:
                        sibs = siblings.get(p_orig, []) + [p_id]
                        siblings.update({p_orig: sibs})
                    else:
                        result.append(p_id)
                elif (pos, part) == ('R', '?'):
                    sibs = siblings.get(person.origin, []) + [p_id]
                    siblings.update({person.origin: sibs})
                elif pos == 'R':
                    tup = (p_id, person.focus, person.origin, part, p_orig)
                    tuples_to_sort.append(tup)
                else:
                    tup = (p_id, person.focus, person.origin)
                    tuples_to_sort.append(tup)
            else:
                result.append(p_id)
            if person.select:
                self.selected = True
        print(tuples_to_sort)
        tups = sorted(tuples_to_sort, key=lambda t: t[1])
        print(tups)
        result += graph_representation.tuples_to_list(tups, siblings)
        self.current_level = result

    def draw_level_return_next(self):
        '''
            Draws current row of nodes.
        '''
        next_lv = set()
        # print("bef:", self.current_level)
        self.sort_current_level()
        # print("aft:", self.current_level)
        for el_id in self.current_level:
            el = self.data.entries()[el_id]
            next_lv |= self.data.get_children(el)
            self.draw_node(el)
        # print('next', next_lv)
        return next_lv

    def create_nodes(self):
        '''
            Creates nodes. Manages subtrees (rows).
        '''
        # TODO make sure the children are under their parents
        # maybe change set to list or something
        # print("Current lv:" + str(self.current_level))
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
        '''
        Draws edges.
        '''
        for entry in self.data.entries().values():
            if isinstance(entry, f):
                # print(entry.idn)
                self.tree.edge(entry.head, entry.idn, arrowhead="none")
                self.tree.edge(entry.idn, entry.partner, arrowhead="none")
                if entry.family_connections is not None:
                    for c in entry.family_connections:
                        self.tree.edge(entry.idn, c)

    def show(self, just_show=False):
        '''
        Main method to display proper tree.
        '''
        self.tree = Tree()
        self.current_level = self.data.find_top()
        # sort by ranks
        self.selected = False
        self.create_nodes()
        self.create_connections()
        # print(self.data.next_indi_id)

        if just_show:
            self.tree.view()
        else:
            return self.tree.render(format='jpeg')
