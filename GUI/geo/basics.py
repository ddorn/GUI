import pygame

from GUI.draw import circle, line

try:
    from .base import BaseWidget
    from .locals import *
    from .draw import *
    from .math import V2

except ImportError:
    from GUI.base import BaseWidget
    from GUI.colors import bw_contrasted
    from GUI.locals import *
    from GUI.math import V2

CIRCLE = 0
CROSS = 1

class Point(BaseWidget):
    def __init__(self, pos, size, color=TURQUOISE, shape=CIRCLE):
        self.rad = size
        super().__init__(pos, (self.rad, self.rad))
        self.color = color
        self.shape = shape

    def render(self, surf):
        if self.shape == CIRCLE:
            circle(surf, self.pos, self.rad, self.color)

        elif self.shape == CROSS:
            line(surf, self.midleft, self.midright, self.color, 1)
            line(surf, self.midtop, self.midbottom, self.color, 1)

        else:
            raise NotImplementedError

    def dist_to(self, pos):
        pos = V2(*pos)
        return (pos-self.pos).norm()


class Rectangle(BaseWidget):
    FILLED = 3
    ROUNDED = 42
    BORDER = 69

    def __init__(self, pos, size, color=PINK, style=FILLED, **params):
        super().__init__(pos, size)
        self.style = style
        self.color = color
        self.params = params

    def render(self, surf):
        if self.style == self.FILLED:
            return pygame.draw.rect(surf, self.color, self.as_rect())
        elif self.style == self.BORDER:
            papy = self.params.get('width', 1)
            return pygame.draw.rect(surf, self.color, self.as_rect(), papy)

        else:
            print('fail')

__all__ = ['Rectangle', 'Point']
