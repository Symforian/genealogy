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
            self.id_entry_set = {}
            self.next_fam_id = 1
            self.next_indi_id = 1
        else:
            self.id_entry_set = env

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
        self.id_entry_set[new_entry_id] = new_entry_value

    def entries(self):
        """Return environment as dictionary."""
        return self.id_entry_set

    def get_partners(self, idn):
        """Return set of partners given person's identification number."""
        person_fam_con_idns = self.id_entry_set[idn].family_connections
        if person_fam_con_idns is None:
            return None
        else:
            ids = set()
            for person_fam_con_idn in person_fam_con_idns:
                family = self.id_entry_set[person_fam_con_idn]
                if family.head == idn:
                    if family.partner:
                        ids.add(family.partner)
                else:
                    if family.head:
                        ids.add(family.head)
        return ids

    def get_originless_partners(self, idn):
        """Return set of partners without origin given person's id number."""
        partners = self.get_partners(idn)
        result = list()
        if partners is not None:
            for partner_id in partners:
                partner = self.id_entry_set[partner_id]
                if partner.origin is None:
                    result.append(partner_id)
        return result

    def get_children(self, person):
        """Return set of children given person."""
        children = set()
        if person.family_connections is not None:
            for fam_idn in person.family_connections:
                family = self.id_entry_set[fam_idn]
                if family.family_connections is not None:
                    for child in family.family_connections:
                        children.add(child)
        return children

    def get_families(self, person: Person):
        """Return set of families given person."""
        families = set()
        if person.family_connections is not None:
            for fam_idn in person.family_connections:
                families.add(fam_idn)
        return families

    def get_children_from_family(self, family: Family):
        """Return set of children given family."""
        children = set()
        if family.family_connections is not None:
            for child in family.family_connections:
                children.add(child)
        return children

    def find_top(self):
        """Find topmost nodes of current environment."""
        current_level = list()
        current_level_set = set()
        for entry in self.id_entry_set.values():
            if isinstance(entry, Person) and entry.origin is None:
                if entry.idn in current_level_set:
                    continue
                part_with_origin = False
                partners = self.get_partners(entry.idn)
                if partners is not None:
                    for partner_id in list(partners):
                        partner = self.id_entry_set[partner_id]
                        if partner.origin is not None:
                            part_with_origin = True
                            break
                if not part_with_origin:
                    current_level.append(entry.idn)
                    current_level_set.add(entry.idn)
                    for partner_id in list(partners):
                        if partner_id not in current_level_set:
                            current_level.append(partner_id)
                            current_level_set.add(partner_id)
        for entry_idn in current_level:
            counter = 0
            e_idn = entry_idn
            while e_idn:
                entry = self.entries()[e_idn]
                if entry.family_connections:
                    fam_idn = next(iter(entry.family_connections))
                    family = self.entries()[fam_idn]
                    if family.family_connections:
                        e_idn = next(iter(family.family_connections))
                        counter += 1
                else:
                    break
            print(f"{entry_idn} + [{counter}]")
        return current_level

    def get_fam_ids_desc(self):
        """Return families' description in form

         `(id, description)`."""
        ret = []
        for (k, v) in self.id_entry_set.items():
            if isinstance(v, Family):
                desc = ""
                if v.head:
                    desc += self.id_entry_set[v.head].description()
                if v.head and v.partner:
                    desc += " & "
                if v.partner:
                    desc += self.id_entry_set[v.partner].description()
                desc += f"({v.idn})"
                i = int(k[1:])
                ret += [(i, k, desc)]
        ret.sort(key=lambda tup: tup[0])
        ret = list(map(lambda t: (t[1], t[2]), ret))
        return ret

    def get_indi_ids_desc(self):
        """Return people' description in form

         `(id, description)`."""
        ret = []
        for (k, v) in self.id_entry_set.items():
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
        for (k, v) in self.id_entry_set.items():
            ret += k + " " + str(v)
        return ret
