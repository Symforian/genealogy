from graph import GraphRepresentation as g_r
from tree_env import Env as env
from person import Person as per
from family import Family as fam
from unittest import TestCase as test_case, main


def prepare_empty_env():
    g = g_r()
    e = env()
    g.send_data(e)
    return g, e


def prepare_1_person_env():
    g, e = prepare_empty_env()
    p = per(e.generate_idn('person'), name=['Adam'])
    e.add_entry(p.idn, p)
    g.send_data(e)
    return g, e, p


def prepare_2_unrelated_people_env():
    g, e, p1 = prepare_1_person_env()
    p2 = per(e.generate_idn('person'), name=['Eve'])
    e.add_entry(p2.idn, p2)
    g.send_data(e)
    return g, e, p1, p2


def prepare_2_connected_people_env():
    g, e, p1, p2 = prepare_2_unrelated_people_env()
    f = fam(e.generate_idn('family'), head=p1.idn, part=p2.idn)
    p1.add(f.idn)
    p2.add(f.idn)
    e.add_entry(f.idn, f)
    g.send_data(e)
    return g, e, p1, p2, f


def prepare_family_of_3_people_env():
    g, e, p1, p2, f = prepare_2_connected_people_env()
    p3 = per(e.generate_idn('person'), name=['Aaron'])
    f.add(p3.idn)
    p3.add_origin(f.idn)
    e.add_entry(p3.idn, p3)
    g.send_data(e)
    return g, e, p1, p2, p3, f


class test_current_level(test_case):
    def test_empty_env(self):
        g, e = prepare_empty_env()
        g.current_level = e.find_top()
        self.assertEqual(g.current_level, [])

    def test_1_person_env(self):
        g, e, p = prepare_1_person_env()
        g.current_level = e.find_top()
        self.assertEqual(g.current_level, [p.idn])

    def test_2_unrelated_people_env(self):
        g, e, p1, p2 = prepare_2_unrelated_people_env()
        g.current_level = e.find_top()
        possibility1 = g.current_level == [p1.idn, p2.idn]
        possibility2 = g.current_level == [p2.idn, p1.idn]
        self.assertTrue(possibility1 | possibility2)

    def test_2_connected_people_env(self):
        g, e, p1, p2, _ = prepare_2_connected_people_env()
        g.select_node(p1.idn)
        g.current_level = e.find_top()
        self.assertEqual(g.current_level, [p1.idn, p2.idn])

    def test_selected_parents_order(self):
        g, e, p1, p2, p3, _ = prepare_family_of_3_people_env()
        g.select_node(p3.idn)
        g.current_level = e.find_top()
        self.assertEqual(g.current_level, [p1.idn, p2.idn])

    def test_selected_has_siblings_and_partner(self):
        return '''TODO FIX'''
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


class test_sort_current_level(test_case):
    def test_empty_env(self):
        g, e = prepare_empty_env()
        g.current_level = e.find_top()
        g.sort_current_level()
        self.assertEqual(g.current_level, [])

    def test_1_person_env(self):
        g, e, p = prepare_1_person_env()
        g.current_level = e.find_top()
        g.sort_current_level()
        self.assertEqual(g.current_level, [p.idn])


if __name__ == '__main__':
    main()
