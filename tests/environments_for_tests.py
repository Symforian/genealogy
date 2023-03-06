from graph import GraphRepresentation as g_r
from tree_env import Env as env
from person import Person as per
from family import Family as fam


def fill_env_with_graph(function):
    def wrapper():
        func = function()
        func[0].send_data(func[1])
        return func

    return wrapper


def prepare_empty_env():
    return g_r(), env()


@fill_env_with_graph
def prepare_1_person_env():
    g, e = prepare_empty_env()
    p = per(e.generate_idn('person'), name=['Adam'])
    e.add_entry(p.idn, p)
    return g, e, p


@fill_env_with_graph
def prepare_2_unrelated_people_env():
    g, e, p1 = prepare_1_person_env()
    p2 = per(e.generate_idn('person'), name=['Eve'])
    e.add_entry(p2.idn, p2)
    return g, e, p1, p2


@fill_env_with_graph
def prepare_2_connected_people_env():
    g, e, p1, p2 = prepare_2_unrelated_people_env()
    f = fam(e.generate_idn('family'), head=p1.idn, part=p2.idn)
    p1.add(f.idn)
    p2.add(f.idn)
    e.add_entry(f.idn, f)
    return g, e, p1, p2, f


@fill_env_with_graph
def prepare_family_of_3_people_env():
    g, e, p1, p2, f = prepare_2_connected_people_env()
    p3 = per(e.generate_idn('person'), name=['Aaron'])
    f.add(p3.idn)
    p3.add_origin(f.idn)
    e.add_entry(p3.idn, p3)
    return g, e, p1, p2, p3, f
