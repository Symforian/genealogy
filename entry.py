"""
    Environment's entry model.
"""


class Entry:

    def __init__(self):
        self.idn = None
        self.family_connections = set()

    def get_idn(self):
        return self.idn

    def add(self, arg):
        self.family_connections.add(arg)

    def update_data(self, data, new_value):
        pass
