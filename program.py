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

    def show(self):
        self.drawer.send_data(self.env)
        self.drawer.show()

    def add_entry(self, n, s, b, d, o):
        i = self.env.generate_idn('person')
        new_person = per(idn=i, name=n, sname=s, birt=b, deat=d)
        if o != 'Unknown':
            new_person.addOrigin(o)
        self.env.entries()[i] = new_person

    def select(self):
        self.drawer.send_data(self.env)
        self.drawer.deselect()
        select = input("Enter idn:\n")
        if select != '':
            self.drawer.select_node(select)


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
