# coding=utf-8

"""This module provides easy to use fonts."""
from math import floor
from pygame import font

from GUI.locals import GUI_PATH

font.init()


class Font(font.Font):
    """A pygame.font.Font font, with no aditionnal methods but provide a good default behavior."""

    PX_TO_PT = [
        1, 1, 1, 1, 2, 3, 3, 4, 5, 6, 7, 7, 8, 9, 10, 11, 11, 12, 12, 13, 14, 15, 15, 16, 17, 18, 19, 19, 20, 21, 22,
        23, 23, 24, 25, 25, 26, 27, 27, 28, 29, 30, 31, 31, 32, 33, 34, 35, 35, 36, 37, 38, 38, 39, 39, 40, 41, 42, 43,
        43, 44, 45, 46, 47, 47, 48, 49, 50, 50, 51, 51, 52, 53, 54, 55, 55, 56, 57, 58, 59, 59, 60, 61, 62, 63, 63, 63,
        64, 65, 66, 67, 67, 68, 69, 70, 71, 71, 72, 73, 74, 75, 75, 75, 76, 77, 78, 79, 79, 80, 81, 82, 83, 83, 84, 85,
        86, 87, 87, 88, 88, 89, 90, 91, 91, 92, 93, 94, 95, 95, 96, 97, 98, 99, 99, 100, 101, 101, 102, 103, 103, 104,
        105, 106, 107, 107, 108, 109, 110, 111, 111, 112, 113, 113, 114, 115, 115, 116, 117, 118, 119, 119, 120, 121,
        122, 123, 123, 124, 125, 126, 126, 127, 127, 128, 129, 130, 131, 131, 132, 133, 134, 135, 135, 136, 137, 138,
        139, 139, 139, 140, 141, 142, 143, 143, 144, 145, 146, 147, 147, 148, 149
    ]
    # MMMMMMMMMH WHAT A BEAUTIFULL WAY TO MAKE CONVERSIONS <3 <3 <3 <3 <3

    POINT = 42
    PIXEL = 69

    def __init__(self, size=20, file=GUI_PATH + r'/data/fonts/segoeuil.ttf', unit=POINT):
        """
        Creates a Font object.
        
        :param size: The font size (See http://www.pygame.org/docs/ref/font.html#pygame.font.Font for more infos)
        :param file: The file of the font file
        """

        if unit == self.PIXEL:
            size = self.px_to_pt(size)

        super(Font, self).__init__(file, size)
        self.font_size = size
        self.font_name = file

    def px_to_pt(self, px):
        """Convert a size in pxel to a size in points."""
        if px < 200:
            pt = self.PX_TO_PT[px]
        else:
            pt = int(floor((px - 1.21) / 1.332))

        return pt

    def set_size(self, pt=None, px=None):
        """
        Set the size of the font, in px or pt.

        The px method is a bit inacurate, there can be one or two px less, and max 4 for big numbers (like 503)
        but the size is never over-estimated. It makes almost the good value.
        """

        assert (pt, px) != (None, None)

        if pt is not None:
            self.__init__(pt, self.font_name)
        else:
            self.__init__(self.px_to_pt(px), self.font_name)


class BoldFont(Font):
    def __init__(self, size, unit=Font.POINT):
        super(BoldFont, self).__init__(size, GUI_PATH + r'/data/fonts/seguisbi.ttf', unit)


DEFAULT_FONT = Font(20)

__all__ = ['Font', 'DEFAULT_FONT']
