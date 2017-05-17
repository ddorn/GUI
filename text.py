import pygame
from .font import *
from .locals import *
pygame.font.init()


class SimpleText(pygame.Rect):
    def __init__(self, text, pos, color=BLUE, font=DEFAULT, anchor='center'):
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
        if callable(self._text):
            return self._text()
        return str(self._text)

    @text.setter
    def text(self, value):
        if value != self._text:
            self._text = value
            self._render()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value != self.color:
            self._color = value
            self._render()

    def _render(self):
        self._last_text = self.text

        self._surface = self.font.render(self.text, True, self.color)
        rect = self._surface.get_rect()

        anchor = getattr(self, self.anchor)
        self.w = rect.w
        self.h = rect.h
        setattr(self, self.anchor, anchor)

    def render(self, display):
        # to handle changing objects
        if self.text != self._last_text:
            self._render()

        display.blit(self._surface, self)


__all__ = ['SimpleText']
