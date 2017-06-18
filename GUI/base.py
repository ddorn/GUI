""" The very bases of the GUI module """

import pygame

try:
    from .locals import *
except ImportError:
    from GUI.locals import *


class BaseWidget(pygame.Rect):
    """ The base class for any widget """

    def __init__(self, pos, size, anchor=CENTER):
        """
        Creates a Basic Widget with... nothing
        """
        super().__init__((0, 0), (0, 0))

        self._anchor = anchor
        self._pos = pos
        self._size = size
        self._focus = False

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '<BaseWidget({}, {})>'.format(self.topleft, self.size)

    def __contains__(self, item):
        """ Test if a point is in the widget """
        x, y = item

        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def __getattribute__(self, item):

        # positions
        if item in "x y top left bottom right topleft bottomleft topright bottomright midtop midleft midbottom midright center".split():
            self.__update()

        # size
        if item in "width height w h".split():
            self.__update()

        return super(BaseWidget, self).__getattribute__(item)

    def __setattr__(self, key, value):
        if key in "topleft bottomleft topright bottomright midtop midleft midbottom midright center".split():
            self.anchor = key
            self._pos = value

        elif key in "width height w h".split():
            raise AttributeError

        elif key in "x y top left bottom right".split():
            raise AttributeError

        else:
            super(BaseWidget, self).__setattr__(key, value)

    def __update(self):
        """ 
        This is called each time an attribute is asked, to be sure every params are updated, beceause of callbacks
        """

        # I can not set the size attr because it is my property, so I set the width and height separately
        w, h = self.size
        super(BaseWidget, self).__setattr__("width", w)
        super(BaseWidget, self).__setattr__("height", h)
        super(BaseWidget, self).__setattr__(self.anchor, self.pos)

    @property
    def pos(self):
        if callable(self._pos):
            return self._pos()
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def size(self):
        if callable(self._size):
            return self._size()
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def anchor(self):
        if callable(self._anchor):
            return self._anchor()
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        self._anchor = value

    def focus(self):
        """ Gives the focus to the widget """
        self._focus = True

    def unfocus(self):
        """ Takes back the focus from the widget """
        self._focus = False

    def update(self, event_or_list):
        pass

    def render(self, surf):
        pass


__all__ = ['BaseWidget']

if __name__ == '__main__':
    from time import time


    def size_f():
        return time() // 1 % 60, 60 - time() // 1 % 60


    w = BaseWidget((0, 0), size_f)

    assert size_f()[0] == w.width
    assert (0, 0) in w
    assert (60, 60) not in w

    w = BaseWidget((1, 1), (10, 10), TOPLEFT)
    assert w.center == (6, 6)
    assert w.height == 10
