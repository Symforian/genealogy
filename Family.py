class Family:

    def __init__(self, head=None, partner=None, relation=None, children=None):
        self.head = head
        self.partner = partner
        self.relation_type = relation
        self.children = children

    def updateData(self, data, new_value):
        if data == "head":
            self.name = new_value
        elif data == "partner":
            self.surname = new_value
        elif data == "relation_type":
            self.relation_type = new_value
        elif data == "children":
            self.death = new_value

    def addChild(self, child):
        self.children.append(child)

    def flip(self):
        temp = self.head
        self.head = self.partner
        self.partner = temp
