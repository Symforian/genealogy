from argparse import ArgumentParser as ap
from tree_env import Env as env
from graph import graph_representation as g_r
from gedcom_parser import GEDCOM_parser as ged_parse
from cli import command_line_interface
from gedcom_exporter import GEDCOM_exporter as ged_export
from person import Person as per
from family import Family as fam
# from PyQt5.QtWidgets import QApplication
# from application import app_window
# import sys


class program:

    def __init__(self):
        self.env = env()
        self.drawer = g_r()
        self.running = True

    def import_gedcom(self, name):
        parser = ged_parse(name)
        self.env = parser.parse()

    def export_gedcom(self, name):
        ged_export(name, self.env.entries()).export()

    def get_ids_desc(self, type):
        if type == 'person':
            return self.env.get_indi_ids_desc()
        elif type == 'family':
            return self.env.get_fam_ids_desc()

    def show(self):
        self.drawer.send_data(self.env)
        self.drawer.show()

    def add_entry(self, n, s, b, d, o):
        i = self.env.generate_idn('person')
        self.create_person_entry(i, n, s, b, d, o)

    def mod_entry(self, i, n, s, b, d, o):
        self.rem_entry(i)
        self.create_person_entry(i, n, s, b, d, o)

    def create_person_entry(self, i, n, s, b, d, o):
        new_person = per(idn=i, name=n, sname=s, birt=b, deat=d)
        if o != 0:
            new_person.addOrigin(o)
            self.env.entries()[o].add(i)
        self.env.addEntry(i, new_person)

    def rem_entry(self, pid):
        person = self.env.entries()[pid]
        if person.origin is not None:
            orig = self.env.entries()[person.origin].family_connections
            if orig is not None:
                orig.remove(pid)
        if person.family_connections is not None:
            for family in person.family_connections:
                self.rem_family(family)
        self.env.entries().pop(pid)

    def rem_family(self, fid):
        family = self.env.entries()[fid]
        if family.family_connections is not None:
            for child in family.family_connections:
                self.env.entries()[child].origin = None
        head_fc = self.env.entries()[family.head].family_connections
        if head_fc is not None:
            head_fc.remove(fid)
        partner_fc = self.env.entries()[family.partner].family_connections
        if partner_fc is not None:
            partner_fc.remove(fid)
        self.env.entries().pop(fid)

    def get_person_data(self, pid):
        return self.env.entries()[pid].pdata()

    def select(self, pid=None):
        self.drawer.send_data(self.env)
        self.drawer.deselect()
        if pid is not None:
            self.drawer.select_node(pid)

    def connect(self, hid, pid):
        entries = self.env.entries()
        fid = self.env.generate_idn('family')
        entries[fid] = fam(fid, hid, pid, "Marriage")
        entries[hid].add(fid)
        entries[pid].add(fid)


def main_cli():
    p = command_line_interface()
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
    print("Run 'python3 application.py' to run with GUI")
    # app = QApplication(sys.argv)
    # window = app_window()
    # window.show()
    # sys.exit(app.exec_())
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
