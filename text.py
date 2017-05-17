"""
A module to easily render text on the screen.
"""

import pygame

try:
    from .font import *
    from .locals import *
    from .base import BaseWidget
except ImportError:
    from font import *
    from locals import *
    from base import BaseWidget
pygame.font.init()


class SimpleText(BaseWidget):
    """ A simple brut text to draw on the screen """
    
    def __init__(self, text, pos, color=BLUE, font=DEFAULT, anchor='center'):
        """
        Creates a new SimpleText object.
        
        :param text: The string or a callable (no args) that returns the string to dislay
        :param pos: the position of the text
        :param color: the color of the text
        :param font: a pygame.Font object
        :param anchor: the anchor of the text. 
            See http://www.pygame.org/docs/ref/rect.html#pygame.Rect for a list of possible anchors.
        """
        
        super().__init__((0, 0, 0, 0))
        setattr(self, anchor, pos)

        self.anchor = anchor
        self.font = font
        self._color = color
        self._last_text = ...
        self._text = text
        self._surface = pygame.Surface((1, 1))  # placeholder

        self._render()

    def __str__(self):
        return self.text

    @property
    def text(self):
        """ Returns the string to render """
        
        if callable(self._text):
            return self._text()
        return str(self._text)

    @text.setter
    def text(self, value):
        """ Sets the text to a new string or callable. Renders the text if needed. """

        if value != self._text:
            self._text = value
            self._render()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        """ Sets the color to a new value (tuple). Renders the text if needed. """
        
        if value != self.color:
            self._color = value
            self._render()

    def _render(self):
        """ Render the text. 
            Avoid using this fonction too many time as it is slow as it is low to render text and blit it. """
        
        self._last_text = self.text

        self._surface = self.font.render(self.text, True, self.color)
        rect = self._surface.get_rect()

        anchor = getattr(self, self.anchor)
        self.w = rect.w
        self.h = rect.h
        setattr(self, self.anchor, anchor)

    def render(self, display):
        """ Render basicly the text """

        # to handle changing objects / callable
        if self.text != self._last_text:
            self._render()

        display.blit(self._surface, self)


__all__ = ['SimpleText']
