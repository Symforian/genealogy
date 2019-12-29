class Person:

    def generateIdn():
        return 0

    # idn None = not yet assigned, other None = unknown

    def __init__(self, idn=None, name=None, sname=None, birt=None, deat=None):
        if idn is None:
            self.idn = Person.generateIdn()
        self.name = name
        self.surname = sname
        self.birth = birt
        self.death = deat
        self.origin = None

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

    def __str__(self):
        temp = "["+str(self.name)+" "+str(self.surname)+"\n"+str(self.birth)
        return temp+" "+str(self.death)+"]"
