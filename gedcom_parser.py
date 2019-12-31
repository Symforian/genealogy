from tree_env import env as id_env
from Person import Person as person
from Family import Family as family
# GEDCOM standard 5.5
# http://homepages.rootsweb.com/~pmcbride/gedcom/55gcch1.htm


class GEDCOM_parser:

    map_tag_to_data = {
        "FAMC": "origin",
        "HUSB": "head",
        "WIFE": "partner",
        "BIRT": "birth",
        "DEAT": "death",
        "SURN": "surname",
        "GIVN": "name"
        }

    def __init__(self, filename):
        self.file = filename
        self.env = id_env()
        self.data_holder = None
        self.current_tag = None

    def get_data(self):
        return self.env

    def line_to_tuple(line):
        ret = line.split()
        if len(ret) > 0:
            ret[0] = int(ret[0])
            if len(ret) > 2 and ret[0] == 0:
                temp = ret[1][1:-1]
                ret[1] = ret[2]
                ret[2] = temp
            return ret

    def create_entry(self):
        if self.data_holder is not None:
            idn = str(self.data_holder.get_idn())
            self.env.addEntry(idn, self.data_holder)
            # self.data_holder = None

    # def fam_tag()
    #    self.data_holder.add(value[1:-1])
    def assign_child_to_family(self):
        return 0

    def assign_person_to_family(self, per):
        self.data_holder.add(per)

    def set_birth_tag(self):
        self.current_tag = "birth"

    def set_death_tag(self):
        self.current_tag = "death"

    '''parse_tag = {
        # "INDI": lambda x: person(idn=x),
        "NAME":
        "GIVN":
        "SURN":
        "BIRT": self.set_birth_tag,
        "DEAT": self.set_death_tag,
        "FAMC":
        "FAM": lambda x: family(idn=x),
        "HUSB":
        "WIFE":
        "CHIL":
        "MARR":
        "DATE":
        "PLAC":
    }'''
    def parse_tag_after_0(self, tag, value):
        if tag == "INDI":
            self.data_holder = person(idn=value[0])
        elif tag == "FAM":
            self.data_holder = family(idn=value[0])
        # else "not_yet_implemented"
# TODO switcher:
# https://jaxenter.com/implement-switch-case-statement-python-138315.html

    def parse_tag_after_1(self, tag, value):
        # if tag == "NAME":
        if tag == "FAM" or tag == "CHIL":
            self.data_holder.add(value[0][1:-1])
        elif tag in ["FAMC", "HUSB", "WIFE"]:
            data_type = GEDCOM_parser.map_tag_to_data[tag]
            self.data_holder.updateData(data_type, value[0][1:-1])
        elif tag == "BIRT" or tag == "DEAT":
            self.current_tag = GEDCOM_parser.map_tag_to_data[tag]
        elif tag == "MARR":
            self.data_holder.updateData("relation_type", "marriage")
        else:
            return "not_yet_implemented"  # DIV

    def parse_tag_after_2(self, tag, value):
        if tag == "DATE":
            self.data_holder.updateData(self.current_tag, value)
        elif tag == "GIVN" or tag == "SURN":
            data_type = GEDCOM_parser.map_tag_to_data[tag]
            self.data_holder.updateData(data_type, value)
        # elif tag == "PLACE":
        #   self.data_holder.updateData(self.current_tag, value)
        # else "not_yet_implemented"

    def parse_tup(self, tup):
        if tup is not None:
            if tup[0] == 0:
                self.create_entry()
                self.parse_tag_after_0(tup[1], tup[2:])
            elif tup[0] == 1:
                self.parse_tag_after_1(tup[1], tup[2:])
            elif tup[0] == 2:
                self.parse_tag_after_2(tup[1], tup[2:])
            # indidata
            # sex
            # famdata
            # DIV
            return 0

    def parse(self):
        with open('km.GED', 'r') as reader:
            line = reader.readline()
            while line != '':
                # print(GEDCOM_parser.parse_line(line), end='')
                tup = GEDCOM_parser.line_to_tuple(line)
                self.parse_tup(tup)
            #  create new families and individuals
            #  with correct data
                line = reader.readline()

        return self.get_data()


# gp = GEDCOM_parser("f")
# print(gp.parse())
