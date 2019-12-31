from Entry import Entry as ent


class Person(ent):

    # idn None = not yet assigned, other None = unknown

    def __init__(self, idn=None, name=None, sname=None, birt=None, deat=None):
        self.idn = idn
        self.name = name
        self.surname = sname
        self.birth = birt
        self.death = deat
        self.origin = None
        self.family_connections = None

    def addOrigin(self, origin):
        self.origin = origin

    def updateData(self, data, new_value):
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
            for i in self.birth:
                date += i + " "
            ret += date[:-1]
        return ret

    def __str__(self):
        temp = "[Person entry:\nName:"+str(self.name)+" "+str(self.surname)
        temp += "\nOrigin: "+str(self.origin)+"\nBorn:"+str(self.birth)
        return temp+"\nDied: "+str(self.death)+"]\n"
