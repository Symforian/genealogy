"""
    Environment's entry model, person.

    Is responsible for storing person's data
    and changing the form of displaying it.
"""
from entry import Entry


class Person(Entry):

    # idn None = not yet assigned, other None = unknown
    u = ['Unknown']

    def __init__(self, idn, name=u, sname=u, birt=u, deat=['']):
        self.depth = 0
        self.focus = -1
        self.select = False
        self.idn = idn  # string(idn)
        self.name = name  # list of string
        self.surname = sname  # list of string
        self.birth = birt  # list of string TODO change to tuple3/ PLACE?
        self.death = deat  # list of string TODO change to tuple3/ PLACE?
        self.origin = None  # string(idn_fam)
        self.family_connections = None  # list of string(idn_fam)

    def add_origin(self, origin):
        self.origin = origin

    def update_data(self, data, new_value):
        if data == "name":
            self.name = new_value
        elif data == "surname":
            self.surname = new_value
        elif data == "birth":
            self.birth = new_value
        elif data == "death":
            self.death = new_value
        elif data == "origin":
            self.origin = new_value

    def clean_display(self):
        ret = ""
        for names in self.name:
            ret += names + " "
        ret += self.surname[0] + "\n"
        date = ""
        for i in self.birth:
            date += i + " "
        date = date[:-1] + "-"
        ret += date
        if self.death is not None:
            date = ""
            for i in self.death:
                date += i + " "
            ret += date[:-1]
        return ret

    def desc(self):
        temp = self.name[0] + " " + self.surname[0]
        # temp += "\nOrigin: "+str(self.origin)+"Born:"+str(self.birth)
        return temp  # +"\nDied: "+str(self.death)+"]\n"

    def pdata(self):
        temp = [self.name, self.surname, self.birth, self.death]
        return temp + [self.origin]

    def __str__(self):
        temp = "[Person entry:\nName:"+str(self.name)+" "+str(self.surname)
        temp += "\nOrigin: "+str(self.origin)+"\nBorn:"+str(self.birth)
        return temp+"\nDied: "+str(self.death)+"]\n"
