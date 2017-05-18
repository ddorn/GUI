"""
This is a module for easy drawings.
"""

import pygame
from pygame import gfxdraw

try:
    from locals import BLACK
except ImportError:
    from .locals import BLACK


def line(surf, start, end, color=BLACK, width=1):
    """ Draws an antialiased on the surface. """
    
    x1, y1 = start
    x2, y2 = end
    
    for i in range(width):
        pygame.draw.aaline(surf, color, (x1, y1 + i), (x2, y2 + i))


def circle(surf, xy, r, color=BLACK):
    """ Draw an antialiased filled circle on the given surface """
    
    x, y = xy
    
    x = round(x)
    y = round(y)
    r = round(r)
    
    gfxdraw.filled_circle(surf, x, y, r, color)
    gfxdraw.aacircle(surf, x, y, r, color)
    
    
def polygon(surf, points, color):
    """ Draw an antialiased filled polygon on a surfae """
    
    gfxdraw.filled_polygon(surf, points, color)
    gfxdraw.aapolygon(surf, points, color)

 
__all__ = ['circle', 'line', 'polygon']
