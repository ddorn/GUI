"""
This module provides a few buttons for an easy pygame GUI.
"""

import pygame
from _thread import start_new_thread
from time import time

try:
    from .base import BaseWidget
    from .locals import *
    from .font import *
    from .draw import *
except ImportError:
    from base import *
    from locals import *
    from font import *
    from draw import *


class BaseButton(BaseWidget):
    """ Abstract base class for any button """
    
    def __init__(self, func, rect):
        """
        Creates a new BaseButton object.
        
        :param func: calback function that takes no argument
        :param rect: the widget rect
        """
        super().__init__(rect)
        self.func = func
        self.pressed = False

    def press(self):
        """ Call when the button is pressed. This start the callback function in a thread """
        start_new_thread(self.func, ())
        self.pressed = True

    def release(self):
        """ Call this when the button is released """
        self.pressed = False


class Button(BaseButton):
    """ A basic button. """
    
    def __init__(self, func, rect, text='', color=GREEN, color_pressed=None):
        """
        Creates a clickable button.
        
        :param func: callback function wih no arguments
        :param rect: widget rect
        :param text: Text to be displayed on the button
        :param color: the natural color of the button
        :param color_pressed: color of the button when it is pressed 
        """
        
        super().__init__(func, rect)
        
        self.text = text
        self.color = color

        if color_pressed is None:
            x, y, z = color
            color_pressed = x // 2, y // 2, z // 2
        self.color_pressed = color_pressed

    def render(self, display):
        if self.pressed:
            color = self.color_pressed
        else:
            color = self.color

        pygame.draw.rect(display, color, self)

        text_color = [WHITE, BLACK][sum(color) / 3 > 200]

        text_surf = DEFAULT.render(self.text, True, text_color, color)
        text_rect = text_surf.get_rect()
        text_rect.center = self.center

        display.blit(text_surf, text_rect)


class IconButton(BaseButton):
    """ A button with a **square** icon intead of a text. """

    def __init__(self, func, rect, icon_path):
        """
        Creates an IconButton.
        
        :param func: callback function
        :param rect: widget rect
        :param icon_path: path to the icon to display
        """
        
        super().__init__(func, rect)

        # making the rect a square
        center = self.center
        self.w = self.h = min(self.size)
        self.center = center

        icon = pygame.image.load(icon_path)
        icon = pygame.transform.smoothscale(icon, self.size)
        icon_pressed = icon.copy()

        for x in range(self.w):
            for y in range(self.h):
                r, g, b, *a = tuple(icon.get_at((x, y)))
                const = 0.8
                r = int(const * r)
                g = int(const * g)
                b = int(const * b)
                icon_pressed.set_at((x, y), (r, g, b))

        self.icon = icon
        self.icon_pressed = icon_pressed

    def render(self, display):
        """ Render the button """
        
        if self.pressed:
            icon = self.icon_pressed
        else:
            icon = self.icon

        display.blit(icon, self)


class SlideBar(BaseWidget):
    """
    A slide bar to bick a value in a range. 
    
    Don't forget to call focus() and unfocus() when the user click on the SlideBar
    """

    def __init__(self, func, rect, min_=0., max_=100., step=1., color=LIGHT_GREY, bg_color=BLUE, interval: "ms" = 1,
                 autostart=True):
        """
        Creates a SlideBar.
        
        :param func: Callback function when a value is changed
        :param rect: The SlideBar rectangle where it will be drawn
        :param min_: The eminimum value of the picker
        :param max_: The maximum value of the picker
        :param step: The step
        :param color: color of the cursor
        :param bg_color: color of the background
        :param interval: minimum interval to call *func*
        :param autostart: starts looking directly if it receives inputs
        """
        super().__init__(rect)

        self.color = color
        self.bg_color = bg_color
        self.func = func
        self.value = 0
        self.min = min_
        self.max = max_
        self.step = step

        self.interval = interval

        if autostart:
            self.start()

    def __repr__(self):
        return f'SlideBar({self.min}:{self.max}:{self.step}; {super().__repr__(self)}, Value: {self.value})'

    def _start(self):
        """ Starts checking forever if the button is clicked """

        last_call = 42
        while True:

            mouse = pygame.mouse.get_pos()
            if (mouse in self) and self._focus:
                self.value_px = mouse[0]

                if last_call + self.interval / 1000 < time():
                    last_call = time()
                    start_new_thread(self.func, (self.value,))

    def start(self):
        """ Starts the checking function in a thread. Don't call this twice. """
        start_new_thread(self._start, ())

    @property
    def value_px(self):
        """ The position in pixels of the cursor """
        return self.x + self.width / (self.max - self.min) * self.value

    @value_px.setter
    def value_px(self, value):
        assert self.x <= value <= self.x + self.width

        delta_x = value - self.x
        prop = delta_x / self.width
        real = prop * (self.max - self.min)
        self.value = round(real / self.step) * self.step

    def render(self, display):
        """ Renders the bar on the display """
        
        # the bar
        bar_rect = pygame.Rect(0, 0, self.width, self.height // 3)
        bar_rect.center = self.center
        display.fill(self.bg_color, bar_rect)

        # the cursor
        circle(display, self.value_px, self.centery, self.height // 2, self.color)


__all__ = ["Button", "IconButton", "SlideBar"]


if __name__ == '__main__':
    display = pygame.display.set_mode((300, 200))

    sb = SlideBar(print, (0, 0, 200, 30), -5, 5, 0.1, interval=200)
    sb.center = (150, 100)

    def func():
        sb.color = RED

    red = Button(func, (0, 0, 40, 40), 'RED')
    red.bottomright = (300, 200)

    run = True
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse in sb:
                    sb.focus()

                if mouse in red:
                    red.press()

            if event.type == pygame.MOUSEBUTTONUP:
                red.release()
                sb.unfocus()

        display.fill(WHITE)
        sb.render(display)
        red.render(display)
        pygame.display.flip()
