from tree_env import Env as env
from person import Person as per
from family import Family as fam
from unittest import TestCase as test_case, main


class test_find_top(test_case):
    def test_empty_env(self):
        self.assertEqual(env().find_top(), set())

    def test_1_person_env(self):
        e = env()
        p = per(e.generate_idn('person'), name=['Adam'])
        e.addEntry(p.idn, p)
        self.assertEqual(e.find_top(), {p.idn})

    def test_2_unrelated_people_env(self):
        e = env()
        p1 = per(e.generate_idn('person'), name=['Adam'])
        p2 = per(e.generate_idn('person'), name=['Eve'])
        e.addEntry(p1.idn, p1)
        e.addEntry(p2.idn, p2)
        self.assertTrue(e.find_top() | {p1.idn, p2.idn})

    def test_2_connected_people_env(self):
        e = env()
        p1 = per(e.generate_idn('person'), name=['Adam'])
        p2 = per(e.generate_idn('person'), name=['Eve'])
        f = fam(e.generate_idn('family'), head=p1.idn, part=p2.idn)
        p1.add(f.idn)
        p2.add(f.idn)
        e.addEntry(p1.idn, p1)
        e.addEntry(p2.idn, p2)
        e.addEntry(f.idn, f)
        self.assertEqual(e.find_top(), {p1.idn, p2.idn})

    def test_selected_parents_order(self):
        e = env()
        p1 = per(e.generate_idn('person'), name=['Adam'])
        p2 = per(e.generate_idn('person'), name=['Eve'])
        p3 = per(e.generate_idn('person'), name=['Aaron'])
        f1 = fam(e.generate_idn('family'), head=p1.idn, part=p2.idn)
        f1.add(p3.idn)
        p1.add(f1.idn)
        p2.add(f1.idn)
        p3.addOrigin(f1.idn)
        e.addEntry(p1.idn, p1)
        e.addEntry(p2.idn, p2)
        e.addEntry(p3.idn, p3)
        e.addEntry(f1.idn, f1)
        self.assertEqual(e.find_top(), {p1.idn, p2.idn})

    def test_selected_has_siblings_and_partner(self):
        e = env()
        p1 = per(e.generate_idn('person'), name=['Adam'])
        p2 = per(e.generate_idn('person'), name=['Eve'])
        p3 = per(e.generate_idn('person'), name=['Aaron'])
        p4 = per(e.generate_idn('person'), name=['Bob'])
        p5 = per(e.generate_idn('person'), name=['Caroline'])
        p6 = per(e.generate_idn('person'), name=['Dorothy'])
        f1 = fam(e.generate_idn('family'), head=p1.idn, part=p2.idn)
        f2 = fam(e.generate_idn('family'), head=p4.idn, part=p6.idn)
        f1.add(p3.idn)
        f1.add(p4.idn)
        f1.add(p5.idn)
        p1.add(f1.idn)
        p2.add(f1.idn)
        p4.add(f2.idn)
        p6.add(f2.idn)
        p3.addOrigin(f1.idn)
        p4.addOrigin(f1.idn)
        p5.addOrigin(f1.idn)
        e.addEntry(p1.idn, p1)
        e.addEntry(p2.idn, p2)
        e.addEntry(p3.idn, p3)
        e.addEntry(p4.idn, p4)
        e.addEntry(p5.idn, p5)
        e.addEntry(p6.idn, p6)
        e.addEntry(f1.idn, f1)
        e.addEntry(f2.idn, f2)
        self.assertEqual(e.find_top(), {p1.idn, p2.idn})

    def test_selected_has_siblings_and_partner_and_child(self):
        e = env()
        p1 = per(e.generate_idn('person'), name=['Adam'])
        p2 = per(e.generate_idn('person'), name=['Eve'])
        p3 = per(e.generate_idn('person'), name=['Aaron'])
        p4 = per(e.generate_idn('person'), name=['Bob'])
        p5 = per(e.generate_idn('person'), name=['Caroline'])
        p6 = per(e.generate_idn('person'), name=['Dorothy'])
        p7 = per(e.generate_idn('person'), name=['Ethan'])
        f1 = fam(e.generate_idn('family'), head=p1.idn, part=p2.idn)
        f2 = fam(e.generate_idn('family'), head=p4.idn, part=p6.idn)
        f1.add(p3.idn)
        f1.add(p4.idn)
        f1.add(p5.idn)
        f2.add(p7.idn)
        p1.add(f1.idn)
        p2.add(f1.idn)
        p4.add(f2.idn)
        p6.add(f2.idn)
        p3.addOrigin(f1.idn)
        p4.addOrigin(f1.idn)
        p5.addOrigin(f1.idn)
        p7.addOrigin(f2.idn)
        e.addEntry(p1.idn, p1)
        e.addEntry(p2.idn, p2)
        e.addEntry(p3.idn, p3)
        e.addEntry(p4.idn, p4)
        e.addEntry(p5.idn, p5)
        e.addEntry(p6.idn, p6)
        e.addEntry(p7.idn, p7)
        e.addEntry(f1.idn, f1)
        e.addEntry(f2.idn, f2)
        self.assertEqual(e.find_top(), {p1.idn, p2.idn})


if __name__ == '__main__':
    main()
