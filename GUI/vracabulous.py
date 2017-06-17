# coding=utf-8

import pygame

from collections import defaultdict

from GUI.locals import FLASH_CREEN, TOPLEFT, MIDNIGHT_BLUE
from GUI.text import SimpleText


class FPSIndicator(SimpleText):
    """ A small text on the top right corner of the screen shoing the fps """
    def __init__(self, clock):
        self.clock = clock

        def text():
            return str(round(self.clock.get_fps()))

        super().__init__(text, (10, 14), FLASH_CREEN, MIDNIGHT_BLUE)

    def render(self, display):
        pygame.draw.rect(display, MIDNIGHT_BLUE, ((0, 0), (20, 28)))
        super().render(display)

        return (0, 0), (20, 28)


class FocusSelector:
    """ A tool to navigate between many objects easily """

    def __init__(self, *items):
        assert len(items) > 0

        self.items = items
        self._selected = 0
        def a():
            return a

        self._on_select = defaultdict(a)
        self._on_unselect = defaultdict(a)

    def __len__(self):
        return len(self.items)

    def next(self):
        """ Selects the next item """

        self.select(self._selected + 1)

    def prev(self):
        """ Selects the previous item """

        self.select(self._selected - 1)

    def select(self, item):
        """ Select an arbitrary item, by possition or by reference """

        self._on_unselect[self._selected]()

        if isinstance(item, int):
            self._selected = item % len(self)
        else:
            self._selected = self.items.index(item)

        self._on_select[self._selected]()

    def selected(self):
        """ Returns the curently focused object """

        return self.items[self._selected]

    def is_selected(self, item):
        """ True is the object is focused """

        return self.items.index(item) == self._selected

    def on_select(self, item, action):
        """ Adds an action to make when an object is selected """

        if not isinstance(item, int):
            item = self.items.index(item)

        self._on_select[item] = action

    def on_unselect(self, item, action):
        """ Adds an action to make when an object is unfocused """

        if not isinstance(item, int):
            item = self.items.index(item)

        self._on_unselect[item] = action


__all__ = ['FocusSelector', 'FPSIndicator']
