from Entry import Entry as ent


class Family(ent):

    def __init__(self, idn=None, head=None, part=None, rel=None):
        self.idn = idn  # string(idn)
        self.head = head  # string (idn)
        self.partner = part  # string(idn)
        self.relation_type = rel  # string
        self.family_connections = None  # list of string(idn)

    def getId(self):
        return self.idn

    def updateData(self, data, new_value):
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
