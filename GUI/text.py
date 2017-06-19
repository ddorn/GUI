# coding=utf-8

"""
A module to easily render text on the screen.
"""
import os
import pygame
import tempfile
from pygame.locals import *
from random import randint

from pygame.event import EventType

from GUI.draw import line

from GUI.locals import *
from GUI.font import DEFAULT
from GUI.base import BaseWidget

pygame.font.init()


class SimpleText(BaseWidget):
    """ A simple brut text to draw on the screen """

    def __init__(self, text, pos, color=BLUE, bg_color=None, font=DEFAULT, anchor='center'):
        """
        Creates a new SimpleText object.
        
        :param text: The string or a callable (no args) that returns the string to dislay
        :param pos: the position of the text
        :param color: the color of the text
        :param bg_color: the background color of the text
        :param font: a pygame.Font object
        :param anchor: the anchor of the text.
            See http://www.pygame.org/docs/ref/rect.html#pygame.Rect for a list of possible anchors.
        """

        super().__init__(pos, (0, 0), anchor)

        self.font = font
        self._color = color
        self._bg_color = bg_color
        self._last_text = ...
        self._text = text
        self._surface = pygame.Surface((1, 1))  # placeholder

        self._render()

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)

    @property
    def text(self):
        """ Returns the string to render """

        if callable(self._text):
            return str(self._text())
        return str(self._text)

    @text.setter
    def text(self, value):
        """ Sets the text to a new string or callable. """

        self._text = value

    @property
    def color(self):
        return self._color

    @property
    def bg_color(self):
        return self._bg_color

    @color.setter
    def color(self, value):
        """ Sets the color to a new value (tuple). Renders the text if needed. """

        if value != self.color:
            self._color = value
            self._render()

    @bg_color.setter
    def bg_color(self, value):
        """ Sets the color to a new value (tuple). Renders the text if needed. """

        if value != self.bg_color:
            self._bg_color = value
            self._render()

    def _render(self):
        """ Render the text.
            Avoid using this fonction too many time as it is slow as it is low to render text and blit it. """

        self._last_text = self.text

        self._surface = self.font.render(self.text, True, self.color, self.bg_color)
        rect = self._surface.get_rect()

        self.size = rect.size

    def render(self, display):
        """ Render basicly the text """

        # to handle changing objects / callable
        if self.text != self._last_text:
            self._render()

        display.blit(self._surface, (self.topleft, self.size))


class InLineTextBox(SimpleText):
    """ A textbox with scrolling in one line """

    RIGHT = 1
    LEFT = -1

    def __init__(self, pos, size, color=BLUE, bg_color=None, font=DEFAULT, anchor='center', default_text=''):
        """
        Creates a new InLineTextBox object.

        Shortcuts with Ctrl for moving the cursor and the deletion are implemented

        :param pos: the position of the text
        :size: The maximum width the text can take. This is the width of the textbox
        :param color: the color of the text
        :param bg_color: the background color of the text
        :param font: a pygame.Font object
        :param anchor: the anchor of the text.
            See http://www.pygame.org/docs/ref/rect.html#pygame.Rect for a list of possible anchors.
        """

        self.default_text = font.render(default_text, True, LIGHT_GREY, bg_color)

        super().__init__('', pos, color, bg_color, font, anchor)
        self.size = size, 42
        self._cursor = 0

        self._render()

    @property
    def cursor(self):
        """ The position of the cursor in the text """

        if self._cursor < 0:
            self.cursor = 0

        if self._cursor > len(self):
            self.cursor = len(self)

        return self._cursor

    @cursor.setter
    def cursor(self, value):
        if value < 0:
            self._cursor = 0
        elif value > len(self):
            self._cursor = len(self)
        else:
            self._cursor = value

    def cursor_pos(self):
        """ The cursor position in pixels """

        if len(self) == 0:
            return self.left + self.default_text.get_width()

        papy = self._surface.get_width()
        if papy > self.w:
            shift = papy - self.width
        else:
            shift = 0

        return self.left + self.font.size(self.text[:self.cursor])[0] - shift

    def move_cursor_one_letter(self, letter=RIGHT):
        """ Moves the cursor of one letter to the right (1) or the the left"""
        assert letter in (self.RIGHT, self.LEFT)

        if letter == self.RIGHT:
            self.cursor += 1
            if self.cursor > len(self.text):
                self.cursor -= 1
        else:
            self.cursor -= 1
            if self.cursor < 0:
                self.cursor += 1

    def move_cursor_one_word(self, word=LEFT):
        assert word in (self.RIGHT, self.LEFT)

        if word == self.RIGHT:
            papy = self.text.find(' ', self.cursor) + 1
            if not papy:
                papy = len(self)
            self.cursor = papy
        else:
            papy = self.text.rfind(' ', 0, self.cursor)
            if papy == -1:
                papy = 0
            self.cursor = papy

    def delete_one_letter(self, letter=RIGHT):
        assert letter in (self.RIGHT, self.LEFT)

        if letter == self.LEFT:
            papy = self.cursor
            self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]
            self.cursor = papy - 1

        else:
            self.text = self.text[:self.cursor] + self.text[self.cursor + 1:]

    def delete_one_word(self, word=RIGHT):
        assert word in (self.RIGHT, self.LEFT)

        if word == self.RIGHT:
            papy = self.text.find(' ', self.cursor) + 1
            if not papy:
                papy = len(self.text)
            self.text = self.text[:self.cursor] + self.text[papy:]

        else:
            papy = self.text.rfind(' ', 0, self.cursor)
            if papy == -1:
                papy = 0
            self.text = self.text[:papy] + self.text[self.cursor:]
            self.cursor = papy

    def add_letter(self, letter):
        assert isinstance(letter, str)
        assert len(letter) == 1

        self.text = self.text[:self.cursor] + letter + self.text[self.cursor:]
        self.cursor += 1

    def update(self, event_or_list):
        """ Updates the text and position of cursor according to the event passed """

        event_or_list = super().update(event_or_list)

        for e in event_or_list:
            if e.key == K_RIGHT:
                if e.mod * KMOD_CTRL:
                    self.move_cursor_one_word(self.RIGHT)
                else:
                    self.move_cursor_one_letter(self.RIGHT)

            elif e.key == K_LEFT:
                if e.mod * KMOD_CTRL:
                    self.move_cursor_one_word(self.LEFT)
                else:
                    self.move_cursor_one_letter(self.LEFT)

            elif e.key == K_BACKSPACE:
                if self.cursor == 0:
                    continue

                if e.mod & KMOD_CTRL:
                    self.delete_one_word(self.LEFT)
                else:
                    self.delete_one_letter(self.LEFT)

            elif e.key == K_DELETE:
                if e.mod & KMOD_CTRL:
                    self.delete_one_word(self.RIGHT)
                else:
                    self.delete_one_letter(self.RIGHT)

            elif e.unicode != '':
                self.add_letter(e.unicode)

    def _render(self):
        """ Render the text.
            Avoid using this fonction too many times as it is slow as it is slow to render text and blit it. """

        self._last_text = self.text

        self._surface = self.font.render(self.text, True, self.color, self.bg_color)
        size = self.w, self._surface.get_height()
        self.size = size

    def render(self, display):
        """ Render basicly the text """

        # to handle changing objects / callable
        if self.text != self._last_text:
            self._render()

        if self.text:
            papy = self._surface.get_width()
            if papy <= self.width:
                display.blit(self._surface, (self.topleft, self.size))
            else:
                display.blit(self._surface, (self.topleft, self.size), ((papy - self.w, 0), self.size))

        else:
            display.blit(self.default_text, (self.topleft, self.size))

        if self._focus:
            groom = self.cursor_pos()
            line(display, (groom, self.top), (groom, self.bottom), CONCRETE)


class InLinePassBox(InLineTextBox):
    """ TextBow that doesn't show the text but other thing or some dots """

    STRANGE = 42
    DOTS = 69

    def __init__(self, pos, size, color=BLUE, bg_color=None, font=DEFAULT, anchor='center', default_text='',
                 style=DOTS):
        """
        TextBow that doesn't show the text but other thing or some dots
        See also InLineTextBox.

        :param style: STRANGE or DOTS
        """

        self._shawn_text = ''
        self.style = style

        super().__init__(pos, size, color, bg_color, font, anchor, default_text)

    @property
    def shawn_text(self):
        """ The text displayed instead of the real one """

        if len(self._shawn_text) == len(self):
            return self._shawn_text

        if self.style == self.DOTS:
            return chr(0x2022) * len(self)

        ranges = [
            (902, 1366),
            (192, 683),
            (33, 122)
        ]

        s = ''
        while len(s) < len(self.text):
            apolo = randint(33, 1366)
            for a, b in ranges:
                if a <= apolo <= b:
                    s += chr(apolo)
                    break

        self._shawn_text = s
        return s

    def cursor_pos(self):
        """ The cursor position in pixels """
        if len(self) == 0:
            return self.left + self.default_text.get_width()

        papy = self._surface.get_width()
        if papy > self.w:
            shift = papy - self.width
        else:
            shift = 0

        return self.left + self.font.size(self.shawn_text[:self.cursor])[0] - shift

    def _render(self):
        """ Render the text.
            Avoid using this fonction too many times as it is slow as it is slow to render text and blit it. """

        self._last_text = self.shawn_text

        self._surface = self.font.render(self.shawn_text, True, self.color, self.bg_color)
        size = self.w, self._surface.get_height()
        self.size = size

    def render(self, display):
        """ Render basicly the text """

        # to handle changing objects / callable
        if self.shawn_text != self._last_text:
            self._render()

        if self.text:
            papy = self._surface.get_width()
            if papy <= self.width:
                display.blit(self._surface, (self.topleft, self.size))
            else:
                display.blit(self._surface, (self.topleft, self.size), ((papy - self.w, 0), self.size))
        else:
            display.blit(self.default_text, (self.topleft, self.size))

        if self._focus:
            groom = self.cursor_pos()
            line(display, (groom, self.top), (groom, self.bottom), CONCRETE)


class LaText(SimpleText):
    """ This class provides a nice rendering for maths equations based on latex. """

    def __init__(self, text, pos, color=BLUE, bg_color=None, font=DEFAULT, anchor='center'):
        """
        The latex _interface_ provides a well looking display of math exquations.
        
        However, you can NOT use function that are not in the amsmath/amsfont or standard package.
        
        :param text: The string or a callable (no args) that returns the string to dislay. The string must be a valid
            LaTex text, without the headers (only the document environement.
        :param pos: the position of the text
        :param color: the color of the text
        :param font: a pygame.Font object. Its size will be chosent for the LeTeX size.
            Too big sizes (> 24.88) does not work
        :param anchor: the anchor of the text.
            See http://www.pygame.org/docs/ref/rect.html#pygame.Rect for a list of possible anchors.
        """

        super().__init__(text, pos, color, bg_color, font, anchor)

    @staticmethod
    def latex_to_img(tex):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(tmpdirname + r'\tex.tex', 'w') as f:
                f.write(tex)

            os.system(r"latex {0}\tex.tex -halt-on-error -interaction=batchmode -disable-installer -aux-directory={0} "
                      r"-output-directory={0}".format(tmpdirname))
            os.system(r"dvipng -T tight -z 9 --truecolor -o {0}\tex.png {0}\tex.dvi".format(tmpdirname))
            # os.system(r'latex2png ' + tmpdirname)

            image = pygame.image.load(tmpdirname + r'\tex.png')

        return image

    def _render(self):
        # TODO : transparent background
        self._last_text = self.text

        name = GUI_PATH + '/.temp/matheq' + str(id(self)) + '.png'

        # generates the LaTeX text
        preamble = r"""\documentclass[40pt]{article}\pagestyle{empty}""" + \
                   r"\usepackage{color}" + \
                   r"\usepackage{amsmath}" + \
                   r"\usepackage{amsfonts}" + \
                   r"\definecolor{kkolor}{RGB}{%i, %i, %i}" % self.color + \
                   r"\begin{document}"

        print(self.font)
        font_setter = r"\fontsize{%i pt}{%i pt}\selectfont" % (self.font.font_size, self.font.font_size * 1.2)
        color_setter = r"{\color{kkolor}"
        end_color_setter = '}'
        end = r'\end{document}'
        text = preamble + font_setter + color_setter + self.text + end_color_setter + end

        # generates the LaTeX png
        self._surface = self.latex_to_img(text)

        # load it
        rect = self._surface.get_rect()

        self.size = rect.size

        try:
            os.remove(name)
        except FileNotFoundError:
            pass


__all__ = ['SimpleText', 'LaText', 'InLineTextBox', 'InLinePassBox']

if __name__ == '__main__':
    from GUI.gui_examples.text import gui

    gui()
