"""
    Gedcom exporter module.

    Is responsible for exporting environment as gedcom file.
"""
from person import Person
from family import Family
from functools import reduce
# GEDCOM standard 5.5
# http://homepages.rootsweb.com/~pmcbride/gedcom/55gcch1.htm


class GedcomExporter:

    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def header(self):
        h = '''0 HEAD
1 GEDC
2 VERS 5.5.5
2 FORM LINEAGE-LINKED
3 VERS 5.5.5
1 CHAR UTF-8
1 SOUR gedcom.org
0 @U@ SUBM
1 NAME gedcom.org
'''
        return h

    def tail():
        t = '''0 TRLR\n'''
        return t

    def write_name(name, surname):
        if(len(name) == 0 ):
            name = Person.UNKNOWN
        if(len(surname) == 0):
            surname = Person.UNKNOWN
        ent = '1 NAME ' + reduce(lambda a, b: a + ' ' + b, name)
        ent += ' /' + reduce(lambda a, b: a + ' ' + b, surname) + '/\n2 SURN '
        ent += reduce(lambda a, b: a + ' ' + b, surname) + '\n2 GIVN '
        return ent + reduce(lambda a, b: a + ' ' + b, name) + '\n'

    def write_event(date, event):
        if date != []:
            ent = '1 ' + event + '\n2 DATE '
            ent += reduce(lambda a, b: a + ' ' + b, date)
            return ent + '\n'
        return ''

    def write_origin(origin):
        if origin is not None:
            return '1 FAMC @' + origin + '@\n'
        return ''

    def write_families(families):
        ent = ''
        if families is not None:
            for fam in families:
                ent += '1 FAM @' + fam + '@\n'
        return ent

    def write_indi(self, entry):
        ent = 'INDI\n'
        ent += GedcomExporter.write_name(entry.name, entry.surname)
        ent += GedcomExporter.write_event(entry.birth, 'BIRT')
        ent += GedcomExporter.write_event(entry.death, 'DEAT')
        ent += GedcomExporter.write_origin(entry.origin)
        ent += GedcomExporter.write_families(entry.family_connections)
        return ent

    def write_head(head):
        return '1 HUSB @' + head + '@\n'

    def write_partner(partner):
        return '1 WIFE @' + partner + '@\n'

    def write_children(children):
        ent = ''
        if children is not None:
            for child in children:
                print(child)
                ent += '1 CHIL @' + child + '@\n'
        return ent

    def write_fam(self, entry):
        ent = 'FAM\n'
        ent += GedcomExporter.write_head(entry.head)
        ent += GedcomExporter.write_partner(entry.partner)
        # ent += GedcomExporter.write_marriage(entry.?)
        # ent += GedcomExporter.write_divorce(entry.?)
        ent += GedcomExporter.write_children(entry.family_connections)
        return ent

    def write_data(self):
        data = ''
        for entry in self.data.values():
            data += '0 @' + entry.idn + '@ '
            if isinstance(entry, Person):
                data += self.write_indi(entry)
            elif isinstance(entry, Family):
                data += self.write_fam(entry)
        return data

    def export(self):
        with open(self.filename, 'w+') as writer:
            writer.write(self.header())
            writer.write(self.write_data())
            writer.write(GedcomExporter.tail())
