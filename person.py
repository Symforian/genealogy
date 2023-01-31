"""
    Environment's entry model, person.

    Is responsible for storing person's data
    and changing the form of displaying it.
"""
from entry import Entry


class Person(Entry):

    UNKNOWN = 'Unknown'
    # idn None = not yet assigned, other None = unknown
    u = [UNKNOWN]

    def __init__(self, idn, name=u, sname=u, birt=u, deat=[''], origin=None):
        self.depth = 0
        self.focus = -1
        self.select = False
        self.idn = idn  # string(idn)
        self.name = name  # list of string
        self.surname = sname  # list of string
        self.birth = birt  # list of string TODO change to tuple3/ PLACE?
        self.death = deat  # list of string TODO change to tuple3/ PLACE?
        self.add_origin(origin)  # string(idn_fam)
        self.family_connections = set()  # list of string(idn_fam)

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
        if not self.name:
            ret = Person.UNKNOWN + " "
        else:
            for names in self.name:
                ret += names + " "
        if self.surname:
            ret += self.surname[0] + "\n"
        else:
            ret += Person.UNKNOWN + "\n"
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

    def description(self):
        if (self.name):
            temp = self.name[0]
        else:
            temp = Person.UNKNOWN
        temp += " "
        if (self.surname):
            temp += self.surname[0]
        else:
            temp += Person.UNKNOWN
        # temp += "\nOrigin: "+str(self.origin)+"Born:"+str(self.birth)
        return temp  # +"\nDied: "+str(self.death)+"]\n"

    def pdata(self):
        temp = [self.name, self.surname, self.birth, self.death]
        return temp + [self.origin]

    def __str__(self):
        temp = "[Person entry:\nName:"+str(self.name)+" "+str(self.surname)
        temp += "\nOrigin: "+str(self.origin)+"\nBorn:"+str(self.birth)
        return temp+"\nDied: "+str(self.death)+"]\n"
