class TreeEnv:

    def __init__(self, env=None):
        if env is None:
            self.used_ids = set([])
            self.next_fam_id = 1
            self.next_indi_id = 1
        else:
            self.used_ids = env

    def generateIdn(self):
        new_idn = 0
        self.used_ids.add(new_idn)
        return new_idn
