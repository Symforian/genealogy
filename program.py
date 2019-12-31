from graph import graph_representation as g_r
from gedcom_parser import GEDCOM_parser as ged_parse


class program:

    def __init__(self):
        self.env = None
        self.drawer = g_r()
        pass

    def import_gedcom_show_only(self, filename):
        parser = ged_parse(filename)
        self.env = parser.parse()
        self.drawer.upload_data(self.env.entries())
        self.drawer.show()


p = program()
p.import_gedcom_show_only('km.GED')
