# coding=utf-8

"""This module provides functions to manipulate colors"""

from GUI.locals import WHITE, BLACK
    
    
def bw_contrasted(color, threshold=200):
    """Return a color (B or W) of oposite balance : it will be easy to distinguish both"""
    return [WHITE, BLACK][sum(color) / 3 > threshold]


def mix(color1, color2, pos=0.5):
    """
    Return the mix of two colors at a state of :pos:

    Retruns color1 * pos + color2 * (1 - pos)
    """
    opp_pos = 1 - pos

    red = color1[0] * pos + color2[0] * opp_pos
    green = color1[1] * pos + color2[1] * opp_pos
    blue = color1[2] * pos + color2[2] * opp_pos
    return int(red), int(green), int(blue)


__all__ = ['bw_contrasted', 'mix']
