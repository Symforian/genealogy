from person import Person as per
from tests.environments_for_tests import (prepare_1_person_env,
                                          prepare_family_of_3_people_env)
from unittest import TestCase as test_case, main


class test_update_data(test_case):

    def test_name_changed(self):
        environment = prepare_1_person_env()
        value_before = environment[2].name
        environment[2].update_data("name", "Mario")
        self.assertNotEqual(value_before, environment[2].name)

    def test_name_changed_properly(self):
        environment = prepare_1_person_env()
        environment[2].update_data("name", "Mario")
        self.assertEquals("Mario", environment[2].name)

    def test_surname_changed(self):
        environment = prepare_1_person_env()
        value_before = environment[2].surname
        environment[2].update_data("surname", "Bond")
        self.assertNotEqual(value_before, environment[2].surname)

    def test_surname_changed_properly(self):
        environment = prepare_1_person_env()
        environment[2].update_data("surname", "Bond")
        self.assertEquals("Bond", environment[2].surname)

    def test_birth_changed(self):
        environment = prepare_1_person_env()
        value_before = environment[2].birth
        environment[2].update_data("birth", ["1", "1", "1"])
        self.assertNotEqual(value_before, environment[2].birth)

    def test_birth_changed_properly(self):
        environment = prepare_1_person_env()
        environment[2].update_data("birth", ["1", "1", "1"])
        self.assertEquals(["1", "1", "1"], environment[2].birth)

    def test_death_changed(self):
        environment = prepare_1_person_env()
        value_before = environment[2].death
        environment[2].update_data("death", ["1", "1", "1"])
        self.assertNotEqual(value_before, environment[2].death)

    def test_death_changed_properly(self):
        environment = prepare_1_person_env()
        environment[2].update_data("death", ["1", "1", "1"])
        self.assertEquals(["1", "1", "1"], environment[2].death)

    def test_origin_changed(self):
        environment = prepare_family_of_3_people_env()
        value_before = environment[4].origin
        environment[4].update_data("origin", None)
        self.assertNotEqual(value_before, environment[4].origin)

    def test_origin_changed_properly(self):
        environment = prepare_family_of_3_people_env()
        environment[4].update_data("origin", None)
        self.assertEquals(None, environment[4].origin)


class test_clean_display(test_case):

    def test_empty(self):
        clean_display = per("I0").clean_display()
        result = "Unknown Unknown\nUnknown-"
        self.assertEquals(clean_display, result)

    def test_only_name(self):
        clean_display = per("I0", ["Bob", "Rob"]).clean_display()
        result = "Bob Rob Unknown\nUnknown-"
        self.assertEquals(clean_display, result)

    def test_only_surname(self):
        clean_display = per("I0", sname=["Bobbson"]).clean_display()
        result = "Unknown Bobbson\nUnknown-"
        self.assertEquals(clean_display, result)

    def test_only_name_surname(self):
        clean_display = per("I0", ["Bob"], ["Bobbson"]).clean_display()
        result = "Bob Bobbson\nUnknown-"
        self.assertEquals(clean_display, result)

    def test_name_surname_dob(self):
        clean_display = per("I0", ["Bob"], ["Bobbson"],
                            ["1", "2", "1980"]).clean_display()
        result = "Bob Bobbson\n1 2 1980-"
        self.assertEquals(clean_display, result)

    def test_full_info(self):
        clean_display = per("I0", ["Bob"], ["Bobbson"],
                            ["1", "II", "1980"],
                            ["3", "IV", "2022"]).clean_display()
        result = "Bob Bobbson\n1 II 1980-3 IV 2022"
        self.assertEquals(clean_display, result)


class test_description(test_case):

    def test_empty(self):
        description = per("I0").description()
        result = "Unknown Unknown"
        self.assertEquals(description, result)

    def test_name(self):
        description = per("I0", ["Bob"]).description()
        result = "Bob Unknown"
        self.assertEquals(description, result)

    def test_surname(self):
        description = per("I0", sname=["Bobbson"]).description()
        result = "Unknown Bobbson"
        self.assertEquals(description, result)

    def test_fullname(self):
        description = per("I0", ["Bob"], ["Bobbson"]).description()
        result = "Bob Bobbson"
        self.assertEquals(description, result)

    def test_fullname_with_extra(self):
        description = per("I0", ["Bob"], ["Bobbson"],
                          ["1", "II", "1980"],
                          ["3", "IV", "2022"]).description()
        result = "Bob Bobbson"
        self.assertEquals(description, result)


if __name__ == '__main__':
    main()
