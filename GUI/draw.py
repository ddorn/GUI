# coding=utf-8

"""
This is a module for easy drawings.
Every function provides anti-aliased shapes.
"""

import pygame
from pygame import gfxdraw

from GUI.math import V2, merge_rects
from GUI.locals import BLACK, ROUNDED, FLAT


def line(surf, start, end, color=BLACK, width=1, style=FLAT):
    """Draws an antialiased line on the surface."""

    width = round(width, 1)
    if width == 1:
        # return pygame.draw.aaline(surf, color, start, end)
        return gfxdraw.line(surf, *start, *end, color)

    start = V2(*start)
    end = V2(*end)

    line_vector = end - start
    half_side = line_vector.normnorm() * width / 2

    point1 = start + half_side
    point2 = start - half_side
    point3 = end - half_side
    point4 = end + half_side

    liste = [
        (point1.x, point1.y),
        (point2.x, point2.y),
        (point3.x, point3.y),
        (point4.x, point4.y)
    ]

    rect = polygon(surf, liste, color)

    if style == ROUNDED:
        _ = circle(surf, start, width / 2, color)
        rect = merge_rects(rect, _)
        _ = circle(surf, end, width / 2, color)
        rect = merge_rects(rect, _)

    return rect


def circle(surf, xy, r, color=BLACK):
    """Draw an antialiased filled circle on the given surface"""

    x, y = xy

    x = round(x)
    y = round(y)
    r = round(r)

    gfxdraw.filled_circle(surf, x, y, r, color)
    gfxdraw.aacircle(surf, x, y, r, color)

    r += 1
    return pygame.Rect(x - r, y - r, 2 * r, 2 * r)


def ring(surf, xy, r, width, color):
    """Draws a ring"""

    r2 = r - width

    x0, y0 = xy
    x = r2
    y = 0
    err = 0

    # collect points of the inner circle
    right = {}
    while x >= y:
        right[x] = y
        right[y] = x
        right[-x] = y
        right[-y] = x

        y += 1
        if (err <= 0):
            err += 2 * y + 1
        if (err > 0):
            x -= 1
            err -= 2 * x + 1

    def h_fill_the_circle(surf, color, x, y, right):
        if -r2 <= y <= r2:
            pygame.draw.line(surf, color, (x0 + right[y], y0 + y), (x0 + x, y0 + y))
            pygame.draw.line(surf, color, (x0 - right[y], y0 + y), (x0 - x, y0 + y))
        else:
            pygame.draw.line(surf, color, (x0 - x, y0 + y), (x0 + x, y0 + y))

    x = r
    y = 0
    err = 0

    while x >= y:

        h_fill_the_circle(surf, color, x, y, right)
        h_fill_the_circle(surf, color, x, -y, right)
        h_fill_the_circle(surf, color, y, x, right)
        h_fill_the_circle(surf, color, y, -x, right)

        y += 1
        if (err < 0):
            err += 2 * y + 1
        if (err >= 0):
            x -= 1
            err -= 2 * x + 1

    gfxdraw.aacircle(surf, x0, y0, r, color)
    gfxdraw.aacircle(surf, x0, y0, r2, color)


def polygon(surf, points, color):
    """Draw an antialiased filled polygon on a surface"""

    gfxdraw.aapolygon(surf, points, color)
    gfxdraw.filled_polygon(surf, points, color)

    x = min([x for (x, y) in points])
    y = min([y for (x, y) in points])
    xm = max([x for (x, y) in points])
    ym = max([y for (x, y) in points])

    return pygame.Rect(x, y, xm - x, ym - y)


__all__ = ['circle', 'line', 'polygon', 'ring']
