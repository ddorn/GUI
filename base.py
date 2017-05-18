""" The very bases of the GUI module """

import pygame

try:
    from locals import CENTER
except ImportError:
    from .locals import CENTER


class BaseWidget(pygame.Rect):
    """ The base class for any widget """

    def __init__(self, pos, size, anchor=CENTER):
        """
        Creates a 
        :param rect: A pygame Rect-like object (can be a tuple of 4 values.
        """
        super().__init__((0, 0), (0, 0))

        self.anchor = anchor
        self._pos = pos
        self._size = size
        self._focus = False

    def __repr__(self):
        return f'<BaseWidget({self.anchor}:{self.pos}, {self.size})>'

    def __contains__(self, item):
        """ Test if a point is in the widget """
        x, y = item

        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def __getattribute__(self, item):

        # positions
        if item in "x y top left bottom right topleft bottomleft topright bottomright midtop midleft midbottom midright center".split():
            super(BaseWidget, self).__setattr__(self.anchor, self.pos)  # update 

        # size
        if item in "width height w h".split():
            w, h = self.size
            super(BaseWidget, self).__setattr__("width", w)  # update
            super(BaseWidget, self).__setattr__("height", h)  # update

        return super(BaseWidget, self).__getattribute__(item)

    def __setattr__(self, key, value):
        if key in "topleft bottomleft topright bottomright midtop midleft midbottom midright center".split():
            print('SET', key, value)
            self.anchor = key
            self._pos = value

        elif key in "width height w h".split():
            raise NotImplemented

        elif key in "x y top left bottom right".split():
            raise NotImplementedError

        else:
            super(BaseWidget, self).__setattr__(key, value)

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

    def focus(self):
        """ Gives the focus to the widget """
        self._focus = True

    def unfocus(self):
        """ Takes back the focus from the widget """
        self._focus = False


__all__ = ['BaseWidget']


if __name__ == '__main__':
    from time import time


    def size_f():
        return time() // 1 % 60, 60 - time() // 1 % 60


    w = BaseWidget((0, 0), size_f)

    assert size_f()[0] == w.width
    assert (0, 0) in w
    assert (60, 60) not in w
