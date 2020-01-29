"""
    Environment's entry model.
"""


class Entry:

    def get_idn(self):
        return self.idn

    def add(self, arg):
        if self.family_connections is None:
            self.family_connections = [arg]
        else:
            self.family_connections.append(arg)

    def update_data(self, data, new_value):
        pass
