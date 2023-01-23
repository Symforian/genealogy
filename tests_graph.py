from graph import GraphRepresentation as g_r
from tree_env import Env as env
from person import Person as per
from family import Family as fam
from unittest import TestCase as test_case, main


class test_current_level(test_case):
    def test_empty_env(self):
        g = g_r()
        e = env()
        g.send_data(e)
        g.current_level = e.find_top()
        self.assertEqual(g.current_level, set())

    def test_1_person_env(self):
        g = g_r()
        e = env()
        p = per(e.generate_idn('person'), name=['Adam'])
        e.add_entry(p.idn, p)
        g.send_data(e)
        g.current_level = e.find_top()
        self.assertEqual(g.current_level, {p.idn})

    def test_2_unrelated_people_env(self):
        g = g_r()
        e = env()
        p1 = per(e.generate_idn('person'), name=['Adam'])
        p2 = per(e.generate_idn('person'), name=['Eve'])
        e.add_entry(p1.idn, p1)
        e.add_entry(p2.idn, p2)
        g.send_data(e)
        g.current_level = e.find_top()
        possibility1 = g.current_level == {p1.idn, p2.idn}
        possibility2 = g.current_level == {p2.idn, p1.idn}
        self.assertTrue(possibility1 | possibility2)

    def test_2_connected_people_env(self):
        g = g_r()
        e = env()
        p1 = per(e.generate_idn('person'), name=['Adam'])
        p2 = per(e.generate_idn('person'), name=['Eve'])
        f = fam(e.generate_idn('family'), head=p1.idn, part=p2.idn)
        p1.add(f.idn)
        p2.add(f.idn)
        e.add_entry(p1.idn, p1)
        e.add_entry(p2.idn, p2)
        e.add_entry(f.idn, f)
        g.send_data(e)
        g.select_node(p1.idn)
        g.current_level = e.find_top()
        self.assertEqual(g.current_level, {p1.idn, p2.idn})

    def test_selected_parents_order(self):
        g = g_r()
        e = env()
        p1 = per(e.generate_idn('person'), name=['Adam'])
        p2 = per(e.generate_idn('person'), name=['Eve'])
        p3 = per(e.generate_idn('person'), name=['Aaron'])
        f1 = fam(e.generate_idn('family'), head=p1.idn, part=p2.idn)
        f1.add(p3.idn)
        p1.add(f1.idn)
        p2.add(f1.idn)
        p3.add_origin(f1.idn)
        e.add_entry(p1.idn, p1)
        e.add_entry(p2.idn, p2)
        e.add_entry(p3.idn, p3)
        e.add_entry(f1.idn, f1)
        g.send_data(e)
        g.select_node(p3.idn)
        g.current_level = e.find_top()
        self.assertEqual(g.current_level, {p1.idn, p2.idn})

    def test_selected_has_siblings_and_partner(self):
        return'''TODO FIX'''
        g = g_r()
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
        p3.add_origin(f1.idn)
        p4.add_origin(f1.idn)
        p5.add_origin(f1.idn)
        e.add_entry(p1.idn, p1)
        e.add_entry(p2.idn, p2)
        e.add_entry(p3.idn, p3)
        e.add_entry(p4.idn, p4)
        e.add_entry(p5.idn, p5)
        e.add_entry(p6.idn, p6)
        e.add_entry(f1.idn, f1)
        e.add_entry(f2.idn, f2)
        g.send_data(e)
        g.select_node(p4.idn)
        g.current_level = e.find_top()
        g.current_level = g.return_next_level()
        possibility1 = g.current_level == {p3.idn, p5.idn, p4.idn, p6.idn}
        possibility2 = g.current_level == {p5.idn, p3.idn, p4.idn, p6.idn}
        print(g.current_level)
        self.assertTrue(possibility1 | possibility2)


if __name__ == '__main__':
    main()
