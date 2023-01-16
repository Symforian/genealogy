"""
    Represents the program's tree environment.
    Is responsible for:

    Finding desired members of family.

    Managing the identification numbers' namespace.

    Storing the data connected with the identyfication number.

    Changing the environment dictonary representation to displayable data.
"""
from person import Person
from family import Family


class Env:

    def __init__(self, env=None):
        """Create a new environment.

        If `env` is `None`, the environment is empty.
        """
        if env is None:
            self.used_ids = {}
            self.next_fam_id = 1
            self.next_indi_id = 1
        else:
            self.used_ids = env

    def generate_idn(self, id_type):
        """Generate a new identification number.

        If `id_type` is `'person'`, generate new person number.

        If `id_type` is `'family'`, generate new family number.
        """
        if id_type == 'person':
            new_id = 'I'+str(self.next_indi_id)
            self.next_indi_id += 1
            return new_id
        elif id_type == 'family':
            new_id = 'F'+str(self.next_fam_id)
            self.next_fam_id += 1
            return new_id

    def add_entry(self, new_entry_id, new_entry_value):
        """Add entry to environment."""
        self.used_ids[new_entry_id] = new_entry_value

    def entries(self):
        """Return environment as dictionary."""
        return self.used_ids

    def get_partners(self, idn):
        """Return set of partners given person's identification number."""
        person_fam_con_idns = self.used_ids[idn].family_connections
        if person_fam_con_idns is None:
            return None
        else:
            ids = set()
            for person_fam_con_idn in person_fam_con_idns:
                family = self.used_ids[person_fam_con_idn]
                if family.head == idn:
                    ids.add(family.partner)
                else:
                    ids.add(family.head)
        return ids

    def get_originless_partners(self, idn):
        """Return set of partners without origin given person's id number."""
        partners = self.get_partners(idn)
        result = set()
        if partners is not None:
            for partner_id in partners:
                partner = self.used_ids[partner_id]
                if partner.origin is None:
                    result.add(partner_id)
        return result

    def get_children(self, el):
        """Return set of children given person."""
        children = set()
        if el.family_connections is not None:
            for fam_idn in el.family_connections:
                family = self.used_ids[fam_idn]
                if family.family_connections is not None:
                    for child in family.family_connections:
                        children.add(child)
        return children

    def find_top(self):
        """Find topmost nodes of current environment."""
        current_level = set()
        for entry in self.used_ids.values():
            if isinstance(entry, Person) and entry.origin is None:
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
        """Return families' description in form

         `(id, description)`."""
        ret = []
        for (k, v) in self.used_ids.items():
            if isinstance(v, Family):
                desc = self.used_ids[v.head].description() + '&'
                desc += self.used_ids[v.partner].description()
                i = int(k[1:])
                ret += [(i, k, desc)]
        ret.sort(key=lambda tup: tup[0])
        ret = list(map(lambda t: (t[1], t[2]), ret))
        return ret

    def get_indi_ids_desc(self):
        """Return people' description in form

         `(id, description)`."""
        ret = []
        for (k, v) in self.used_ids.items():
            if isinstance(v, Person):
                desc = v.description()
                i = int(k[1:])
                ret += [(i, k, desc)]
        ret.sort(key=lambda tup: tup[0])
        ret = list(map(lambda t: (t[1], t[2]), ret))
        return ret

    def __str__(self):
        """Return representation for debugging."""
        ret = ""
        for (k, v) in self.used_ids.items():
            ret += k + " " + str(v)
        return ret
