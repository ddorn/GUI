import pygame
from pygame import gfxdraw


def circle(surf, x, y, r, color):
    x = round(x)
    y = round(y)
    r = round(r)
    
    gfxdraw.filled_circle(surf, x, y, r, color)
    gfxdraw.aacircle(surf, x, y, r, color)
    
    
__all__ = ['circle']
