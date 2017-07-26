# coding=utf-8

"""
The very bases of the GUI module.

Defines :BaseWidget:, the base class for any widget.
To create any new widget, you must extend BaseWidget.
"""

import pygame

from GUI.locals import CENTER, TOPLEFT, TOPRIGHT, MIDTOP, MIDLEFT, MIDRIGHT, BOTTOMRIGHT, MIDBOTTOM, BOTTOMLEFT
from pygame.event import EventType


class BaseWidget(pygame.Rect):
    """
    The base class for any widget

    The position of the widget (returned by .pos()) is always the coord at the anchor,
        even if the anchor changes. Every other position attribute is calculated according to this position
    """

    def __init__(self, pos, size, anchor=CENTER):
        """
        Creates a Basic Widget with... nothing

        The pos, size and anchor can be tuples or funcions that returns a tuple (an anchostr for the anchor)
        """

        self.__verify(pos)
        self.__verify(size)

        super().__init__((0, 0), (0, 0))

        self._anchor = anchor
        self._pos = pos
        self._size = size
        self._focus = False
        self.clicked = False

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '<BaseWidget({}, {})>'.format(self.topleft, self.size)

    def __contains__(self, item):
        """Test if a point is in the widget"""
        return self.left <= item[0] <= self.right and self.top <= item[1] <= self.bottom

    def __getattribute__(self, item):

        # we need to update the attrs in case they are defined with a callback
        # so all have the right value at anytime
        # TODO : cache them for the whole frame, so there wont be unnecessary calls

        # positions
        if item in "x y top left bottom right topleft bottomleft topright bottomright midtop midleft midbottom " \
                   "midright center centerx centery".split():
            self.__update()

        # size
        if item in "width height w h".split():
            self.__update()

        return super(BaseWidget, self).__getattribute__(item)

    def __setattr__(self, key, value):
        if key in (TOPLEFT, BOTTOMLEFT, TOPRIGHT, BOTTOMRIGHT, MIDTOP, MIDLEFT, MIDBOTTOM, MIDRIGHT, CENTER):
            self.anchor = key
            self.pos = value

        elif key in ('width', 'height', 'w', 'h'):
            raise AttributeError("Can't set the attribute")

        elif key in ('x', 'y', 'top', 'left', 'bottom', 'right', 'centerx', 'centery'):
            raise AttributeError("Can't set the attribute")

        else:
            super(BaseWidget, self).__setattr__(key, value)

    def __update(self):
        """
        This is called each time an attribute is asked, to be sure every params are updated, beceause of callbacks.
        """

        # I can not set the size attr because it is my property, so I set the width and height separately
        width, height = self.size
        super(BaseWidget, self).__setattr__("width", width)
        super(BaseWidget, self).__setattr__("height", height)
        super(BaseWidget, self).__setattr__(self.anchor, self.pos)

    @staticmethod
    def __verify(pos_or_size):
        if not callable(pos_or_size):
            assert isinstance(pos_or_size, tuple)
            assert len(pos_or_size) == 2
            assert isinstance(pos_or_size[0], int)
            assert isinstance(pos_or_size[1], int)

    def as_rect(self):
        """Returns the pos and the size of the rect like you can pass to the pygame.Rect constructor or any widget"""

        return self.pos, self.size

    @property
    def pos(self):
        if callable(self._pos):
            return self._pos()
        return self._pos

    @pos.setter
    def pos(self, value):
        if not callable(value):
            if not isinstance(value, tuple):
                raise TypeError("The pos must be a callable that returns 2-tuples or a 2-tuple")
            if len(value) != 2:
                raise ValueError("The pos must be a callable that returns 2-tuples or a 2-tuple")

        self._pos = value

    @property
    def size(self):
        if callable(self._size):
            return self._size()
        return self._size

    @size.setter
    def size(self, value):
        if not callable(value):
            if not isinstance(value, tuple):
                raise TypeError("The size must be a callable that returns 2-tuples or a 2-tuple")
            if len(value) != 2:
                raise ValueError("The size must be a callable that returns 2-tuples or a 2-tuple")

        self._size = value

    @property
    def anchor(self):
        if callable(self._anchor):
            return self._anchor()
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        if not callable(value):
            if value not in (TOPLEFT, TOPRIGHT, MIDTOP, MIDLEFT, MIDRIGHT, CENTER, BOTTOMRIGHT, MIDBOTTOM, BOTTOMLEFT):
                raise ValueError

        self._anchor = value

    def focus(self):
        """Gives the focus to the widget."""
        self._focus = True

    def unfocus(self):
        """Takes back the focus from the widget."""
        self._focus = False

    def click(self):
        """Makes the widget clicked."""
        self.clicked = True

    def release(self):
        """Unclick the widget."""
        self.clicked = False

    def get_focus(self):
        """Returns the current focus state."""
        return self._focus

    def update(self, event_or_list):
        if isinstance(event_or_list, EventType):
            return [event_or_list]
        else:

            return event_or_list

    def render(self, surf):
        raise NotImplementedError


__all__ = ['BaseWidget']

if __name__ == '__main__': help(BaseWidget)
