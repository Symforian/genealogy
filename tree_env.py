from person import Person as p
from family import Family as f


class Env:

    def __init__(self, env=None):
        if env is None:
            self.used_ids = {}
            self.next_fam_id = 1
            self.next_indi_id = 1
        else:
            self.used_ids = env

    def generate_idn(self, id_type):
        if id_type == 'person':
            new_id = 'I'+str(self.next_indi_id)
            self.next_indi_id += 1
            return new_id
        elif id_type == 'family':
            new_id = 'F'+str(self.next_fam_id)
            self.next_fam_id += 1
            return new_id

    def addEntry(self, eid, value):
        self.used_ids[eid] = value

    def entries(self):
        return self.used_ids

    def get_partners(self, idn):
        fam_c_ids = self.used_ids[idn].family_connections
        if fam_c_ids is None:
            return None
        else:
            ids = set()
            for fam_c_id in fam_c_ids:
                family = self.used_ids[fam_c_id]
                if family.head == idn:
                    ids.add(family.partner)
                else:
                    ids.add(family.head)
        return ids

    def get_originless_partners(self, idn):
        partners = self.get_partners(idn)
        result = set()
        if partners is not None:
            for partner_id in partners:
                partner = self.used_ids[partner_id]
                if partner.origin is None:
                    result.add(partner_id)
        return result

    def get_children(self, el):
        children = set()
        # if they have a family
        if el.family_connections is not None:
            for fam_idn in el.family_connections:
                family = self.used_ids[fam_idn]
                # if there are children in this family
                if family.family_connections is not None:
                    for c in family.family_connections:
                        children.add(c)
        return children

    def find_top(self):
        current_level = set()
        for entry in self.used_ids.values():
            if isinstance(entry, p) and entry.origin is None:
                part_with_origin = False
                partners = self.get_partners(entry.idn)
                if partners is not None:
                    for partner_id in list(partners):
                        partner = self.used_ids[partner_id]
                        if partner.origin is not None:
                            part_with_origin = True
                            break
                if not part_with_origin:
                    current_level.add(entry.idn)
        return current_level

    def get_fam_ids_desc(self):
        ret = []
        for (k, v) in self.used_ids.items():
            if isinstance(v, f):
                desc = self.used_ids[v.head].desc() + '&'
                desc += self.used_ids[v.partner].desc()
                i = int(k[1:])
                ret += [(i, k, desc)]
        ret.sort(key=lambda tup: tup[0])
        ret = list(map(lambda t: (t[1], t[2]), ret))
        return ret

    def get_indi_ids_desc(self):
        ret = []
        for (k, v) in self.used_ids.items():
            if isinstance(v, p):
                desc = v.desc()
                i = int(k[1:])
                ret += [(i, k, desc)]
        ret.sort(key=lambda tup: tup[0])
        ret = list(map(lambda t: (t[1], t[2]), ret))
        return ret

    def __str__(self):
        ret = ""
        for (k, v) in self.used_ids.items():
            ret += k + " " + str(v)
        return ret
