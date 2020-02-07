"""
    Environment's entry model, family.

    Is responsible for storing family's data
    and changing the form of displaying it.
"""
from entry import Entry


class Family(Entry):

    def __init__(self, idn=None, head=None, part=None, rel=None):
        super().__init__()
        self.idn = idn  # string(idn)
        self.head = head  # string (idn)
        self.partner = part  # string(idn)
        self.relation_type = rel  # string
        self.family_connections = None  # list of string(idn)

    def getId(self):
        return self.idn

    def update_data(self, data, new_value):
        if data == "head":
            self.head = new_value
        elif data == "partner":
            self.partner = new_value
        elif data == "relation_type":
            self.relation_type = new_value
        elif data == "children":
            self.children = new_value

    def flip(self):
        temp = self.head
        self.head = self.partner
        self.partner = temp

    def __str__(self):
        temp = "[Family entry:\nHead:"+str(self.head)+" partner:"
        temp += str(self.partner)+"\nRelation:"+str(self.relation_type)
        return temp+"\nChildren: "+str(self.family_connections)+"]"
