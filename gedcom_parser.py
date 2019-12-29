import TreeEnv

# GEDCOM standard 5.5
# http://homepages.rootsweb.com/~pmcbride/gedcom/55gcch1.htm
class GEDCOM_parser:
    def __init__(self, filename):
        self.file = filename
        self.env = TreeEnv()

    def get_data(self):
        return self.parsed_data

    def parse(self):
        # open file
          #  parse tags 
          #  create new families and individuals
          #  with correct data
        return get_data(self)


