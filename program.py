from argparse import ArgumentParser as ap
from graph import graph_representation as g_r
from gedcom_parser import GEDCOM_parser as ged_parse
from Person import Person as per
from Family import Family as fam


class program:

    def __init__(self):
        self.env = None
        self.drawer = g_r()
        self.running = True

    def import_gedcom(self):
        parser = ged_parse(input("Enter filename\n"))
        self.env = parser.parse()

    def show(self):
        self.drawer.upload_data(self.env.entries())
        self.drawer.show()

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

    def add_entry(self):
        i = input("Enter idn:\n")
        n = [input("Enter name:\n")]
        s = [input("Enter surname:\n")]
        bd = input("Enter birth day:\n")
        bm = input("Enter birth month:\n")
        by = input("Enter birth year:\n")
        b = [bd, bm, by]
        d = input("Enter death day:\n")
        new_person = per(idn=i, name=n, sname=s, birt=b, deat=d)
        self.env.entries()[i] = new_person

    def check_entry(self):
        idn = input("Enter idn:\n")
        print(self.env.entries()[idn])

    def remove_entry(self):
        idn = input("Enter idn:\n")
        self.env.entries().pop(idn)

    def connect(self):
        idn = input("Enter idn:\n")
        h = input("Enter head id:\n")
        p = input("Enter partner id:\n")
        r = input("Enter relation name:\n")
        self.env.entries()[idn] = fam(idn, h, p, r)
        # TODO if one of h p is None, create Unknown <- but only one
        self.env.entries()[h].add(idn)
        self.env.entries()[p].add(idn)

    def update_entry(self):
        idn = input("Enter idn:\n")
        data = input("Enter data:\n")
        value = input("Enter value:\n")
        if data in ('birth', 'death'):
            value = value.split()
        elif data == 'origin':
            self.env.entries()[value].add(idn)
        self.env.entries()[idn].updateData(data, value)

    def quit(self):
        self.running = False

    def error():
        print("Unknown command")
    commands = {
                'i': import_gedcom,
                's': show,
                'l': list_env,
                'a': add_entry,
                'c': check_entry,
                'r': remove_entry,
                'u': update_entry,
                'm': connect,
                'q': quit,
                }


def main_cli():
    p = program()
    DEFINED_GEDFILE = 'km.GED'
    current_command = None
    while(p.running):
        if current_command is None:
            current_command = p.commands.get(input("Enter command:"), p.error)
            if current_command.__name__ == 'error':
                current_command = None
            if current_command is not None:
                getattr(p, current_command.__name__)()
                current_command = None


def main_gui():
    # TODO implementu GUI
    print("Not yet implemented")
    return 0


if __name__ == "__main__":
    parser = ap(description='Choose program mode')
    parser.add_argument('--command_line', '-c', action='store_const',
                        const=True, default=False,
                        help='enter CLI mode (default: GUI mode)')
    args = parser.parse_args()
    if vars(args)['command_line']:
        main_cli()
    else:
        main_gui()

