import pygame
from pygame import gfxdraw


try:
    from .base import BaseWidget
    from .locals import *
    from .draw import *
    from .math import V2

except ImportError:
    from GUI.base import BaseWidget
    from GUI.colors import bw_contrasted
    from GUI.locals import *
    from GUI.math import V2, comb


class Bezier(BaseWidget):
    def __init__(self, pos, size, points, color=GREEN, width=1, reso=2000):
        super().__init__(pos, size)

        self.points = [V2(*p) for p in points]
        self.color = GREEN
        self.line_width = width
        self.reso = reso

    def render(self, surf: pygame.Surface):
        color = self.color
        n = len(self.points) - 1

        i = 0
        last_pos = None
        for t in range(self.reso):
            t /= self.reso
            tt = 1 - t

            end = V2(0, 0)
            for k, p in enumerate(self.points):
                end += comb(n, k) * p * t ** k * tt ** (n-k)

            if end.ti == last_pos:
                i += 1
                continue
            else:
                last_pos = end.ti

            if callable(self.color):
                color = self.color(t)

            if self.line_width < 2:
                surf.set_at(end.ti, color)
            else:
                x, y = end.ti
                gfxdraw.aacircle(surf, x, y, round(self.line_width/2), color)
                gfxdraw.filled_circle(surf, x, y, round(self.line_width/2), color)

        print(i, self.reso, sep='/')


if __name__ == '__main__':
    from GUI.gui_examples import gui

    gui()
