# coding=utf-8
from math import sqrt

import pygame


def merge_rects(rect1, rect2):
    """ Returns the smallest rect containning two rects """
    r = pygame.Rect(rect1)
    t = pygame.Rect(rect2)

    right = max(r.right, t.right)
    bot = max(r.bottom, t.bottom)
    x = min(t.x, r.x)
    y = min(t.y, r.y)

    return pygame.Rect(x, y, right - x, bot - y)


class V2:
    """ A vector """

    def __init__(self, x, y):
        """ A basic vector for calculus and positionning """

        # noinspection PyArgumentList
        self.x = x
        self.y = y

    def __repr__(self):
        return "V2({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return V2(self.x + other[0], self.y + other[1])

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise IndexError
        if not item in [0, 1]:
            raise IndexError

        if item:
            return self.y
        return self.x

    def __sub__(self, other):
        return V2(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return V2(-self.x, -self.y)

    def __mul__(self, other):
        return V2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return V2(self.x / other, self.y / other)

    def squared_norm(self):
        """ Returns the squared norm of the vector """

        return self.x ** 2 + self.y ** 2

    def norm(self):
        """ Returns the norm of the vector """
        return sqrt(self.squared_norm())

    def normnorm(self):
        """
        Returns a vecor noraml to this one with a norm of one

        :return: V2
        """
        n = self.norm()
        return V2(-self.y / n, self.x / n)


__all__ = ['V2', 'merge_rects']
