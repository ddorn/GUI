from random import shuffle

import pytest

from GUI.geo.basics import Rectangle
from GUI.vracabulous import *
from GUI.locals import *

# ---------------------------- Testing FPSIndicator ---------------------------- #

pass


# ---------------------------- Testing FocusSelector --------------------------- #

@pytest.fixture
def focus():
    return FocusSelector(*[Rectangle((0, 0), (i, i), BLUE) for i in range(5)])


def test_init_all_not_focus_except_first(focus: FocusSelector):
    assert focus.selected() == focus.items[0]

    for i, elt in enumerate(focus.items):
        if i:
            assert not elt.get_focus()
        else:
            assert elt.get_focus()


def test_next(focus: FocusSelector):
    for i in range(5):
        assert focus.selected_index() == i
        focus.next()
    assert focus.selected_index() == 0


def test_prev(focus: FocusSelector):
    focus.select(4)

    for i in range(5):
        assert focus.selected_index() == 4 - i
        focus.prev()
    assert focus.selected_index() == 4


def test_select_and_selected():
    items = [Rectangle((0, 0), (i, i), BLUE) for i in range(5)]
    focus = FocusSelector(*items)

    order = list(range(5))
    shuffle(order)

    for item in order:
        focus.select(item)
        assert focus.selected() == items[item]
        for i in items:
            if i is focus.selected():
                assert i.get_focus()
            else:
                assert not i.get_focus()

    for item in items:
        focus.select(item)
        assert focus.selected() == item


# ----------------------------- Testing Separator ------------------------------ #

@pytest.fixture
def sep():
    return Separator(0, 1)

@pytest.fixture
def sep2():
    return Separator(3, 4)

@pytest.fixture
def sep3():
    return Separator(2, -1)

def test_init_tuple():
    v = Separator((1, 2))
    assert v.x == 1
    assert v.y == 2


def test_init_xy():
    v = Separator(3, 4)
    assert v.x == 3
    assert v.y == 4


def test_get_item(sep: Separator):
    assert sep[0] == 0
    assert sep[1] == 1

    with pytest.raises(IndexError):
        return sep[2]


def test_set_item(sep: Separator):
    sep[0] = 5
    assert sep.x == 5
    sep[1] = 3.12
    assert sep.y == 3.12

    with pytest.raises(IndexError):
        sep[2] = 4

    with pytest.raises(IndexError):
        sep['x'] = 4

    with pytest.raises(IndexError):
        sep['y'] = 4

    with pytest.raises(IndexError):
        sep[0.1] = 4


def test_neq(sep2: Separator):
    v = -sep2
    assert v == (-3, -4)
    assert isinstance(v, Separator)

def test_add_and_radd(sep2: Separator, sep3: Separator):
    assert sep2 + sep3 == (5, 3) == sep2 + (2, -1) == (2, -1) + sep2
    assert isinstance(sep2 + sep3, tuple)


def test_sub_and_rsub(sep2: Separator, sep3: Separator):
    assert sep2 - sep3 == (1, 5) == sep2 - (2, -1) == (3, 4) - sep3
    assert isinstance(sep2 - sep3, tuple)

def test_mul_and_rmul(sep2):
    assert sep2 * 3 == 3 * sep2 == (9, 12)
    assert isinstance(sep2 * 3, Separator)

def test_div(sep2):
    assert sep2 / 2 == (1.5, 2)
    assert isinstance(sep2, Separator)
