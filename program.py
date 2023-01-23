"""
    Connects GraphRepresentation, Environment, GUI, CLI.
    Is responsible for:

    Importing and exporting Gedcom data.

    Communication between modules.

    Running CLI.
"""
from argparse import ArgumentParser as AP
from tree_env import Env
from graph import GraphRepresentation as GR
from gedcom_parser import GedcomParser as GP
from cli import CommandLineInterface
from gedcom_exporter import GedcomExporter as GE
from person import Person
from family import Family


class Program:

    def __init__(self):
        """Create a new program state.

        With empty environment and empty graph representation.
        """
        self.env = Env()
        self.drawer = GR()

    def import_gedcom(self, name):
        """Import and parse gedcom data."""
        parser = GP(name)
        self.env = parser.parse()

    def export_gedcom(self, name):
        """Parse and export gedcom data."""
        GE(name, self.env.entries()).export()

    def get_ids_desc(self, type):
        """Return list of tuples of id numbers and descriptions of data"""
        if type == 'person':
            return self.env.get_indi_ids_desc()
        elif type == 'family':
            return self.env.get_fam_ids_desc()

    def show(self):
        """Return the tree representation."""
        self.drawer.send_data(self.env)
        return self.drawer.show()

    def add_entry(self, name, surname, birth, death, origin):
        """Generate id number to given data and `create_person_entry`."""
        idn = self.env.generate_idn('person')
        self.create_person_entry(idn, name, surname, birth, death, origin)

    def mod_entry(self, idn, name, surname, birth, death, origin):
        """Modify person entry in the environment."""
        old_entry = self.env.entries()[idn]
        fam_cons = old_entry.family_connections
        self.env.entries().pop(idn)
        self.create_person_entry(idn, name, surname, birth, death, origin)
        self.env.entries()[idn].family_connections = fam_cons

    def create_person_entry(self, idn, name, surname, birth, death, origin):
        """Create new person entry, and add to the environment."""
        new_person = Person(idn, name, sname=surname, birt=birth, deat=death)
        if origin != 0:
            new_person.add_origin(origin)
            self.env.entries()[origin].add(idn)
        self.env.add_entry(idn, new_person)

    def rem_entry(self, person_id):
        """Remove person entry and it's families from the environment."""
        person = self.env.entries()[person_id]
        if person.origin is not None:
            origin_fam = self.env.entries()[person.origin].family_connections
            if origin_fam is not None:
                origin_fam.remove(person_id)
        if person.family_connections is not None:
            for family in person.family_connections:
                self.rem_family(family)
        self.env.entries().pop(person_id)

    def rem_family(self, family_id):
        """Remove family entry from the environment."""
        family = self.env.entries()[family_id]
        if family.family_connections is not None:
            for child in family.family_connections:
                self.env.entries()[child].origin = None
        head_fam_con = self.env.entries()[family.head].family_connections
        if head_fam_con is not None:
            head_fam_con.pop(family_id)
        partner_famcon = self.env.entries()[family.partner].family_connections
        if partner_famcon is not None:
            partner_famcon.pop(family_id)
        self.env.entries().pop(family_id)

    def get_person_data(self, person_id):
        return self.env.entries()[person_id].pdata()

    def select(self, person_id=None):
        """Select person changing it's color."""
        self.drawer.send_data(self.env)
        self.drawer.deselect()
        if person_id is not None:
            self.drawer.select_node(person_id)

    def connect(self, head_id, partner_id):
        """Connect two people (partnerish relation only)."""
        entries = self.env.entries()
        family_id = self.env.generate_idn('family')
        entries[family_id] = Family(family_id, head_id, partner_id, "Marriage")
        entries[head_id].add(family_id)
        entries[partner_id].add(family_id)


def main_cli():
    """Run program with CLI."""
    p = CommandLineInterface()
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
    """Deprecated."""
    print("Run 'python3 application.py' to run with GUI")
    return 0


if __name__ == "__main__":
    parser = AP(description='Choose program mode')
    parser.add_argument('--command_line', '-c', action='store_const',
                        const=True, default=False,
                        help='enter CLI mode (default: GUI mode)')
    args = parser.parse_args()
    if vars(args)['command_line']:
        main_cli()
    else:
        main_gui()
