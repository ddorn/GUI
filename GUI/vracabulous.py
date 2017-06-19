# coding=utf-8
import os
import pygame
from pygame.locals import *
from collections import defaultdict

from GUI import WHITE
from GUI.locals import FLASH_CREEN, MIDNIGHT_BLUE, TOPLEFT
from GUI.text import SimpleText


class FPSIndicator(SimpleText):
    """ A small text on the top right corner of the screen shoing the fps """

    def __init__(self, clock):
        self.clock = clock

        def text():
            return str(round(self.clock.get_fps()))

        super().__init__(text, (0, 0), FLASH_CREEN, MIDNIGHT_BLUE, anchor=TOPLEFT)

    def render(self, display):
        pygame.draw.rect(display, MIDNIGHT_BLUE, ((0, 0), (20, 28)))
        super().render(display)

        return (0, 0), (20, 28)


class FocusSelector:
    """ A tool to navigate between many objects easily """

    def __init__(self, *items):
        assert len(items) > 0

        self.items = items
        for i in items:
            i.unfocus()
        self.items[0].focus()

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
        self.selected().unfocus()

        if isinstance(item, int):
            self._selected = item % len(self)
        else:
            self._selected = self.items.index(item)

        self.selected().focus()
        self._on_select[self._selected]()

    def selected(self):
        """ Returns the curently focused object """

        return self.items[self._selected]

    def selected_index(self):
        """ The index of the selected item in the item list """
        return self._selected

    def is_selected(self, item):
        """ True is the object is focused """

        return self.items.index(item) == self._selected

    def on_select(self, item, action):
        """
        Adds an action to make when an object is selected
        Only one action can be stored this way
        """

        if not isinstance(item, int):
            item = self.items.index(item)

        self._on_select[item] = action

    def on_unselect(self, item, action):
        """ Adds an action to make when an object is unfocused """

        if not isinstance(item, int):
            item = self.items.index(item)

        self._on_unselect[item] = action


class Separator:
    """
    A positionning tool.

    Like a V2, but gives tuples when added or substrayed. This is usefull for functions that take only tuples
    Gives still a Separator when mul/divided
    """

    def __init__(self, x, y=None):
        if y is None:
            self.x = x[0]
            self.y = x[1]

        else:
            self.x = x
            self.y = y

    def __repr__(self):
        return "<Sep({}, {})>".format(self.x, self.y)

    def __getitem__(self, item):

        if item == 0:
            return self.x

        if item == 1:
            return self.y

        raise IndexError

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
            return

        if key == 1:
            self.y = value
            return

        raise IndexError

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __neg__(self):
        return Separator(-self.x, -self.y)

    def __add__(self, other):
        return self.x + other[0], self.y + other[1]

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.x - other[0], self.y - other[1]

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        return Separator(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * (1 / other)


class Windows:
    """
    This is a base class for a small pygame project, you should implement
        - the __init__(): where you create all widgets
        - the update_on_event() to listen to event the way you want
        - the render() to draw your widgets
        Don't forget to call super() on those methods

    class variable to customise the project : FPS, VIDEO_OPTION, SCREEN_SIZE, NAME
    """

    SCREEN_SIZE = 800, 500
    NAME = 'Empty project'
    VIDEO_OPTIONS = DOUBLEBUF | VIDEORESIZE
    FPS = 60

    def __init__(self):
        """
        This is a base class for a small pygame project, you should implement
            - the __init__(): where you create all widgets
            - the update_on_event() to listen to event the way you want
            - the render() to draw your widgets
            Don't forget to call super() on those methods

        class variable to customise the project : FPS, VIDEO_OPTION, SCREEN_SIZE, NAME
        """

        self.running = True
        self.screen = self.new_screen()
        self.clock = pygame.time.Clock()

        self.fps = FPSIndicator(self.clock)

    def update_on_event(self, e):
        """ Deals with a single event """
        if e.type == QUIT:
            self.running = False

        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                self.running = False

            elif e.key == K_F4 and e.mod & KMOD_ALT:  # Alt+F4 --> quits
                self.running = False

        elif e.type == VIDEORESIZE:
            self.SCREEN_SIZE = e.size
            self.screen = self.new_screen()

    def update(self):
        """ Gets all events and deal with then by calling update_on_event() """

        for e in pygame.event.get():
            self.update_on_event(e)

    def render(self):
        """ Renders the screen. Here you must draw everything """

        self.screen.fill(WHITE)
        self.fps.render(self.screen)

    def update_screen(self):
        """ Refreshes the screen. You don't need to override this except to update only small portins of the screen """

        self.clock.tick(self.FPS)
        pygame.display.update()

    def destroy(self):
        """ Clean what is needed at the end and returns what run() returns """
        pass

    def run(self):
        """ The run loop. Returns self.destroy() """

        while self.running:
            self.update()
            self.render()
            self.update_screen()

        return self.destroy()

    def new_screen(self):
        """ Makes a new screen with a size of SCREEN_SIZE, and VIDEO_OPTION as flags. Sets the windows name to NAME """

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption(self.NAME)

        return pygame.display.set_mode(self.SCREEN_SIZE, self.VIDEO_OPTIONS)


__all__ = ['FocusSelector', 'FPSIndicator', 'Separator', 'Windows']
