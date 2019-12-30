class env:

    def __init__(self, env=None):
        if env is None:
            self.used_ids = {}
            self.next_fam_id = 1
            self.next_indi_id = 1
        else:
            self.used_ids = env

    def generateIdn(self):
        new_idn = 0
        self.used_ids.add(new_idn)
        return new_idn

    def addEntry(self, eid, value):
        self.used_ids[eid] = value

    def __str__(self):
        ret = ""
        for (k, v) in self.used_ids.items():
            ret += k + " " + str(v)
        return ret
