# coding=utf-8

"""This module provides simle shapes to draw or attach to widgets."""

import pygame

from GUI.base import BaseWidget
from GUI.draw import circle, line, roundrect
from GUI.locals import TURQUOISE, PINK, TOPLEFT, PURPLE, PIXEL
from GUI.math import V2


class Point(BaseWidget):

    CIRCLE = 0
    CROSS = 1

    def __init__(self, pos, size, color=TURQUOISE, shape=CIRCLE):
        self.rad = size
        super().__init__(pos, (self.rad, self.rad))
        self.color = color
        self.shape = shape

    def render(self, surf):
        if self.shape == self.CIRCLE:
            circle(surf, self.pos, self.rad, self.color)

        elif self.shape == self.CROSS:
            line(surf, self.midleft, self.midright, self.color, 1)
            line(surf, self.midtop, self.midbottom, self.color, 1)

        else:
            raise NotImplementedError

    def dist_to(self, pos):
        pos = V2(*pos)
        return (pos - self.pos).norm()


class Line(BaseWidget):
    def __init__(self, pos1, pos2, color=PURPLE, line_width=1):
        self.line_width = line_width
        self.color = color

        self._pos1 = pos1
        self._pos2 = pos2

        def _pos():
            return min(self.pos1[0], self.pos2[0]), min(self.pos1[1], self.pos2[1])

        def _size():
            return max(self.pos1[0], self.pos2[0]) - _pos()[0], max(self.pos1[1], self.pos2[1]) - _pos()[1]

        super().__init__(_pos, _size, TOPLEFT)

    @property
    def pos1(self):
        return self._pos1 if not callable(self._pos1) else self._pos1()

    @pos1.setter
    def pos1(self, value):
        self._pos1 = value

    @property
    def pos2(self):
        return self._pos2 if not callable(self._pos2) else self._pos2()

    @pos2.setter
    def pos2(self, value):
        self._pos2 = value

    def render(self, surf):
        line(surf, self.pos1, self.pos2, self.color, self.line_width)


class Rectangle(BaseWidget):

    FILLED = 3
    ROUNDED = 42
    BORDER = 69

    def __init__(self, pos, size, color=PINK, style=FILLED, anchor=TOPLEFT, **params):
        super().__init__(pos, size, anchor)
        self.style = style
        self.color = color
        self.params = params

    def render(self, surf):
        if self.style == self.FILLED:
            return pygame.draw.rect(surf, self.color, self.as_rect())

        elif self.style == self.BORDER:
            papy = self.params.get('width', 1)
            return pygame.draw.rect(surf, self.color, self.as_rect(), papy)

        elif self.style == self.ROUNDED:
            rounding = self.params.get('rounding', 5)
            unit = self.params.get('unit', PIXEL)
            roundrect(surf, self, self.color, rounding, unit)

        else:
            raise ValueError('Style not supported.')


__all__ = ['Rectangle', 'Point', 'Line']
