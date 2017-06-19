# coding=utf-8

import pytest
from pygame.locals import *

from pygame.event import Event

from GUI.base import *
from GUI.locals import *


@pytest.fixture
def widget():
    return BaseWidget((100, 200), (50, 20))


@pytest.fixture
def widget2():
    return BaseWidget((0, 0), (100, 100), TOPLEFT)


@pytest.fixture
def screen():
    import pygame
    return pygame.Surface((100, 100))


@pytest.fixture
def screen_size():
    return 100, 100


def test_position(widget: BaseWidget):
    w = widget
    assert w.left == 75
    assert w.right == 125
    assert w.top == 190
    assert w.bottom == 210

    assert w.x == w.left
    assert w.y == w.top
    assert w.w == w.width == 50
    assert w.h == w.height == 20

    assert w.centery == w.y + w.h / 2
    assert w.centerx == w.x + w.w / 2

    assert w.topleft == (w.left, w.top)
    assert w.topright == (w.right, w.top)
    assert w.midtop == ((w.left + w.right) / 2, w.top)

    assert w.midleft == (w.left, (w.top + w.bottom) / 2)
    assert w.center == (100, 200)
    assert w.midright == (125, 200)

    assert w.midbottom == (w.centerx, w.bottom)
    assert w.bottomright == (w.right, w.bottom)
    assert w.bottomleft == (w.left, w.bottom)


def test_init_focus(widget: BaseWidget):
    assert not widget.get_focus()

    widget.focus()
    assert widget.get_focus() is True
    widget.unfocus()
    assert widget.get_focus() is False


def test_default_anchor(widget: BaseWidget):
    assert widget.anchor == CENTER


def test_change_anchor(widget: BaseWidget):
    w = widget

    assert w.center == (100, 200)
    w.anchor = TOPLEFT
    assert w.topleft == (100, 200)


def test_pos_callback(screen_size):
    def pos():
        return screen_size

    w = BaseWidget(pos, (10, 10), BOTTOMRIGHT)

    assert w.topleft == (90, 90)

    screen_size = 200, 200
    assert w.topleft == (190, 190)


def test_size_callback(screen_size):
    def size():
        return screen_size[0] / 2, screen_size[1] / 2

    w = BaseWidget((0, 0), size, TOPLEFT)

    assert w.size == (50, 50)

    screen_size = 200, 200

    assert w.bottomright == (100, 100)


@pytest.mark.parametrize('x, y', [
    (0, 0),
    (50, 50),
    (100, 100),
    (23, 0),
    (0, 23),
    (100, 23),
    (23, 100)
])
def test_point_in_widget(widget2, x, y):
    w = widget2

    assert (x, y) in w


@pytest.mark.parametrize('x, y', [
    (-1, -1),
    (101, 100),
    (23, -1),
    (0, 101),
    (24319741, 120438012410),
    (23, 101)
])
def test_point_not_in_widget(widget2, x, y):
    w = widget2

    assert (x, y) not in w


def test_set_attribute_of_sigle_pos_elt_fails(widget: BaseWidget):
    with pytest.raises(AttributeError):
        widget.left = 10

    with pytest.raises(AttributeError):
        widget.right = 10

    with pytest.raises(AttributeError):
        widget.w = 10

    with pytest.raises(AttributeError):
        widget.width = 10

    with pytest.raises(AttributeError):
        widget.x = 10

    with pytest.raises(AttributeError):
        widget.y = 10

    with pytest.raises(AttributeError):
        widget.h = 10

    with pytest.raises(AttributeError):
        widget.height = 10

    with pytest.raises(AttributeError):
        widget.bottom = 10

    with pytest.raises(AttributeError):
        widget.top = 10

    with pytest.raises(AttributeError):
        widget.centerx = 10

    with pytest.raises(AttributeError):
        widget.centery = 10


def test_anchor_and_pos_set(widget: BaseWidget):
    widget.topleft = 0, 0

    assert widget.anchor == TOPLEFT
    assert widget.center == (25, 10)


def test_bad_pos_set_raises(widget: BaseWidget):
    with pytest.raises(TypeError):
        widget.center = 0

    with pytest.raises(ValueError):
        widget.center = 0, 0, 0


def test_bad_size_set_raises(widget: BaseWidget):
    with pytest.raises(TypeError):
        widget.size = 0

    with pytest.raises(ValueError):
        widget.size = 0, 0, 0


def test_str_repr(widget):
    assert str(widget) == repr(widget)
    assert str(widget.x) in str(widget)
    assert str(widget.y) in str(widget)
    assert str(widget.w) in str(widget)
    assert str(widget.h) in str(widget)
    assert 'BaseWidget' in str(widget)


@pytest.mark.parametrize('anchor', [
    TOPLEFT, TOPRIGHT, MIDTOP, MIDLEFT, MIDRIGHT, CENTER, BOTTOMRIGHT, MIDBOTTOM, BOTTOMLEFT
])
def test_anchor_set_works(widget: BaseWidget, anchor):
    widget.anchor = anchor
    assert widget.anchor == anchor


@pytest.mark.parametrize('anchor', [
    TOPLEFT + ' ', 'BANANA', 42, 'TROL', 'CENTER', 'apolo'
])
def test_anchor_set_fails(widget: BaseWidget, anchor):
    with pytest.raises(ValueError):
        widget.anchor = anchor


def test_as_rect(widget: BaseWidget):
    assert widget.as_rect() == ((100, 200), (50, 20))


def test_render_raises(widget: BaseWidget, screen):
    with pytest.raises(NotImplementedError):
        widget.render(screen)


def test_update_returns_events(widget: BaseWidget):
    event = Event(KEYDOWN, {})
    ret = widget.update(event)

    assert ret == [event]

    ret = widget.update([event])

    assert ret == [event]


def test_set_size(widget2: BaseWidget):
    widget2.size = 10, 10

    assert widget2.width == 10
    assert widget2.height == 10
    assert widget2.pos == (0, 0)


def test_anchor_callback():
    anchor = CENTER
    w = BaseWidget((0, 0), (10, 10), lambda: anchor)

    assert w.anchor == CENTER
    anchor = TOPLEFT
    assert w.anchor == TOPLEFT


def test_click(widget: BaseWidget):
    assert widget.clicked is False

    widget.click()
    assert widget.clicked is True
    widget.release()
    assert widget.clicked is False
