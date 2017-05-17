"""
This is a module for easy drawings.
"""

from pygame import gfxdraw


def circle(surf, x, y, r, color):
    """ Draw an antialiased filled circle on the given surface """
    
    x = round(x)
    y = round(y)
    r = round(r)
    
    gfxdraw.filled_circle(surf, x, y, r, color)
    gfxdraw.aacircle(surf, x, y, r, color)
    
    
def polygon(surf, points, color):
    """ Draw an antialiased filled polygon on a surfae """
    
    gfxdraw.filled_polygon(surf, points, color)
    gfxdraw.aapolygon(surf, points, color)

 
__all__ = ['circle']
