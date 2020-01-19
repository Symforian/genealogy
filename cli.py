from gedcom_parser import GEDCOM_parser as ged_parse
from gedcom_exporter import GEDCOM_exporter as ged_export
from graph import graph_representation as g_r
from person import Person as per
from family import Family as fam


class command_line_interface:
    def __init__(self):
        self.env = None
        self.drawer = g_r()
        self.running = True

    def import_gedcom(self):
        parser = ged_parse(input("Enter filename\n"))
        self.env = parser.parse()

    def export_gedcom(self):
        if self.env is not None:
            msg = "Enter filename\n"
            ged_export(input(msg), self.env.entries()).export()
        else:
            print("No data to export\n")

    def show(self):
        self.drawer.send_data(self.env)
        self.drawer.show()

    def select(self):
        self.drawer.send_data(self.env)
        self.drawer.deselect()
        select = input("Enter idn:\n")
        if select != '':
            self.drawer.select_node(select)

    def list_env(self):
        part = input("What do you want to list?\n")
        if self.env is None:
            print("Empty")
        if part is None:
            return self.env.entries()
        items = list(self.env.entries().items())
        if part in ('p', 'person', 'persons'):
            print(list(filter(lambda t: isinstance(t[1], per), items)))
        elif part in ('f', 'family', 'families'):
            print(list(filter(lambda t: isinstance(t[1], fam), items)))

    def enter_date():
        d = input("Enter day:\n")
        m = input("Enter month:\n")
        y = input("Enter year:\n")
        date = [d, m, y]
        if all(data == '' for data in date):
            date = per.u
        return date

    def add_entry(self):
        i = self.env.generate_idn('person')
        n = input("Enter name:\n").split()
        s = input("Enter surname:\n").split()
        print("Birth:")
        b = command_line_interface.enter_date()
        d = input("Is alive?[enter = yes]:\n")
        if d == '':
            d = ['']
        else:
            print("Death:")
            d = command_line_interface.enter_date()

        new_person = per(idn=i, name=n, sname=s, birt=b, deat=d)
        self.env.entries()[i] = new_person

    def check_entry(self):
        idn = input("Enter idn:\n")
        print(self.env.entries()[idn])

    def remove_entry(self):
        idn = input("Enter idn:\n")
        self.env.entries().pop(idn)

    def connect(self):
        idn = self.env.generate_idn('family')
        h = input("Enter head id:\n")
        p = input("Enter partner id:\n")
        r = input("Enter relation name:\n")
        entries = self.env.entries()
        h_d = entries[h].depth
        p_d = entries[p].depth
        if h_d > p_d:
            entries[p].depth = h_d
        elif p_d > h_d:
            entries[h].depth = p_d
        entries[idn] = fam(idn, h, p, r)
        entries[h].add(idn)
        entries[p].add(idn)

    def update_entry(self):
        idn = input("Enter idn:\n")
        data = input("Enter data:\n")
        value = input("Enter value:\n")
        if data in ('name', 'surname', 'birth', 'death'):
            if value == '':
                value = per.u
            else:
                value = value.split()
        elif data == 'origin':
            origin = self.env.entries()[value]
            # not safe - need to checn if ^ exists
            origin.add(idn)
            n_depth = self.env.entries()[origin.head].depth + 1
            # also not safe    V  might not exist
            self.env.entries()[idn].depth = n_depth
        # need to check if V exists
        self.env.entries()[idn].updateData(data, value)

    def quit(self):
        self.running = False

    def error():
        print("Unknown command")
    commands = {
                'i': import_gedcom,
                'e': export_gedcom,
                's': show,
                'l': list_env,
                'f': select,
                'a': add_entry,
                'c': check_entry,
                'r': remove_entry,
                'u': update_entry,
                'm': connect,
                'q': quit,
                }
