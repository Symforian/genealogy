from tree_env import Env
from person import Person
from family import Family
from unittest import TestCase, main, mock


class test_find_top(TestCase):

    def test_empty_env(self):
        self.assertEqual(Env().find_top(), set())

    def test_1_person_env(self):
        p1 = mock.create_autospec(Person, idn='I1', origin=None,
                                  family_connections=None)
        e = Env({p1.idn: p1})
        self.assertEqual(e.find_top(), {p1.idn})

    def test_2_unrelated_people_env(self):
        p1 = mock.create_autospec(Person, idn='I1', origin=None,
                                  family_connections=None)
        p2 = mock.create_autospec(Person, idn='I2', origin=None,
                                  family_connections=None)
        e = Env({p1.idn: p1, p2.idn: p2})
        self.assertTrue(e.find_top(), {p1.idn, p2.idn})

    def test_2_connected_people_env(self):
        p1 = mock.create_autospec(Person, idn='I1', origin=None,
                                  family_connections=['F1'])
        p2 = mock.create_autospec(Person, idn='I2', origin=None,
                                  family_connections=['F1'])
        f1 = mock.create_autospec(Family, idn='F1', head='I1',
                                  partner='I2')
        e = Env({p1.idn: p1, p2.idn: p2, f1.idn: f1})
        self.assertEqual(e.find_top(), {p1.idn, p2.idn})

    def test_selected_parents_order(self):
        p1 = mock.create_autospec(Person, idn='I1', origin=None,
                                  family_connections=['F1'])
        p2 = mock.create_autospec(Person, idn='I2', origin=None,
                                  family_connections=['F1'])
        f1 = mock.create_autospec(Family, idn='F1', head='I1',
                                  partner='I2', family_connections=['I3'])
        p3 = mock.create_autospec(Person, idn='I3', origin='F1',
                                  family_connections=None)
        e = Env({p1.idn: p1, p2.idn: p2, p3.idn: p3, f1.idn: f1})
        self.assertEqual(e.find_top(), {p1.idn, p2.idn})

    def test_selected_has_siblings_and_partner(self):
        p1 = mock.create_autospec(Person, idn='I1', origin=None,
                                  family_connections=['F1'])
        p2 = mock.create_autospec(Person, idn='I2', origin=None,
                                  family_connections=['F1'])
        p3 = mock.create_autospec(Person, idn='I3', origin='F1',
                                  family_connections=None)
        p4 = mock.create_autospec(Person, idn='I4', origin='F1',
                                  family_connections=['F2'])
        p5 = mock.create_autospec(Person, idn='I5', origin='F1',
                                  family_connections=None)
        p6 = mock.create_autospec(Person, idn='I6', origin=None,
                                  family_connections=['F2'])
        f1 = mock.create_autospec(Family, idn='F1', head='I1',
                                  partner='I2', family_connections=['I3'])
        f2 = mock.create_autospec(Family, idn='F2', head='I4',
                                  partner='I6', family_connections=None)
        e = Env({p1.idn: p1, p2.idn: p2, p3.idn: p3, p4.idn: p4,
                p5.idn: p5, p6.idn: p6, f1.idn: f1, f2.idn: f2})
        self.assertEqual(e.find_top(), {p1.idn, p2.idn})

    def test_selected_has_siblings_and_partner_and_child(self):
        p1 = mock.create_autospec(Person, idn='I1', origin=None,
                                  family_connections=['F1'])
        p2 = mock.create_autospec(Person, idn='I2', origin=None,
                                  family_connections=['F1'])
        p3 = mock.create_autospec(Person, idn='I3', origin='F1',
                                  family_connections=None)
        p4 = mock.create_autospec(Person, idn='I4', origin='F1',
                                  family_connections=['F2'])
        p5 = mock.create_autospec(Person, idn='I5', origin='F1',
                                  family_connections=None)
        p6 = mock.create_autospec(Person, idn='I6', origin=None,
                                  family_connections=['F2'])
        p7 = mock.create_autospec(Person, idn='I7', origin='F2',
                                  family_connections=None)
        f1 = mock.create_autospec(Family, idn='F1', head='I1',
                                  partner='I2', family_connections=['I3'])
        f2 = mock.create_autospec(Family, idn='F2', head='I4',
                                  partner='I6', family_connections=['I7'])
        e = Env({p1.idn: p1, p2.idn: p2, p3.idn: p3, p4.idn: p4, p5.idn: p5,
                 p6.idn: p6, p7.idn: p7, f1.idn: f1, f2.idn: f2})
        self.assertEqual(e.find_top(), {p1.idn, p2.idn})


class test_get_children(TestCase):

    def test_no_children(self):
        p1 = mock.create_autospec(Person, idn='I1', family_connections=None)
        e = Env({p1.idn: p1})
        self.assertEqual(e.get_children(p1), set())

    def test_one_child_head(self):
        p1 = mock.create_autospec(Person, idn='I1', family_connections=['F1'])
        p2 = mock.create_autospec(Person, idn='I2', family_connections=['F1'])
        f1 = mock.create_autospec(Family, idn='F1', head='I1',
                                  partner='I2', family_connections=['I3'])
        p3 = mock.create_autospec(Person, idn='I3', origin='F1',
                                  family_connections=None)
        e = Env({p1.idn: p1, p2.idn: p2, p3.idn: p3, f1.idn: f1})
        self.assertEqual(e.get_children(p1), {p3.idn})

    def test_one_child_partner(self):
        p1 = mock.create_autospec(Person, idn='I1', family_connections=['F1'])
        p2 = mock.create_autospec(Person, idn='I2', family_connections=['F1'])
        f1 = mock.create_autospec(Family, idn='F1', head='I1',
                                  partner='I2', family_connections=['I3'])
        p3 = mock.create_autospec(Person, idn='I3', origin='F1',
                                  family_connections=None)
        e = Env({p1.idn: p1, p2.idn: p2, p3.idn: p3, f1.idn: f1})
        self.assertEqual(e.get_children(p2), {p3.idn})

    def test_one_child_child(self):
        p1 = mock.create_autospec(Person, idn='I1', family_connections=['F1'])
        p2 = mock.create_autospec(Person, idn='I2', family_connections=['F1'])
        f1 = mock.create_autospec(Family, idn='F1', head='I1',
                                  partner='I2', family_connections=['I3'])
        p3 = mock.create_autospec(Person, idn='I3', origin='F1',
                                  family_connections=None)
        e = Env({p1.idn: p1, p2.idn: p2, p3.idn: p3, f1.idn: f1})
        self.assertEqual(e.get_children(p3), set())


if __name__ == '__main__':
    main()
