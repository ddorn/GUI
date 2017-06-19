"""
This module provides a few buttons for an easy pygame GUI.
"""

import pygame
from _thread import start_new_thread
from time import time, sleep

from GUI.locals import GREEN, CENTER, BLUE, LIGHT_GREY
from GUI.font import DEFAULT, Font
from GUI.draw import circle
from GUI.text import SimpleText
from GUI.base import BaseWidget
from GUI.colors import bw_contrasted


class BaseButton(BaseWidget):
    """ Abstract base class for any button """

    def __init__(self, func, pos, size, anchor):
        """
        Creates a new BaseButton object.
        
        :param func: calback function that takes no argument
        :param pos: the widget pos. Can be a callable or a 2-tuple
        :size: the width size. Can be a callable or a 2-tuple
        """
        super().__init__(pos, size, anchor)
        self.func = func

    def click(self, milis=None):
        """
        Call when the button is pressed. This start the callback function in a thread
        If :milis is given, will release the button after :milis miliseconds
        """
        start_new_thread(self.func, ())
        super().click()

        if milis is not None:
            start_new_thread(self.release, (milis,))

    def release(self, milis=0):
        """
        Call this when the button is released
        Blocks for :milis miliseconds (used by .press() for auto release)
        """
        if milis:
            sleep(milis / 1000)

        super().release()

    def render(self, display):
        raise NotImplementedError


class Button(BaseButton):
    """ A basic button. """

    def __init__(self, func, pos, size, text='', color=GREEN, color_pressed=None, anchor=CENTER):
        """
        Creates a clickable button.
        
        :param func: callback function wih no arguments
        :param size: widget size. Can be a callable or a 2-tuple.
        :param pos: widget position. Can be a callable or a 2-tuple.
        :param anchor: widget anchor
        :param text: Text to be displayed on the button
        :param color: the natural color of the button
        :param color_pressed: color of the button when it is pressed
        """

        super().__init__(func, pos, size, anchor)

        self.text = text
        self.color = color

        if color_pressed is None:
            x, y, z = color
            color_pressed = x // 2, y // 2, z // 2
        self.color_pressed = color_pressed

    def render(self, display):
        if self.clicked:
            color = self.color_pressed
        else:
            color = self.color

        pygame.draw.rect(display, color, self)

        text_color = bw_contrasted(color)

        text_surf = DEFAULT.render(self.text, True, text_color, color)
        text_rect = text_surf.get_rect()
        text_rect.center = self.center

        display.blit(text_surf, text_rect)


class IconButton(BaseButton):
    """ A button with a **square** icon intead of a text. """

    def __init__(self, func, pos, size: int, icon_path, anchor=CENTER):
        """
        Creates an IconButton.
        
        :param size: widget size. Can be a callable or a 2-tuple.
        :param pos: widget position. Can be a callable or a 2-tuple.
        :param anchor: widget anchor
        :param func: callback function
        :param icon_path: path to the icon to display
        """

        # making the rect a square
        super().__init__(func, pos, (size, size), anchor)

        icon = pygame.image.load(icon_path)
        icon = pygame.transform.smoothscale(icon, self.size)
        icon_pressed = icon.copy()

        for x in range(self.w):
            for y in range(self.h):
                r, g, b, *_ = tuple(icon.get_at((x, y)))
                const = 0.8
                r = int(const * r)
                g = int(const * g)
                b = int(const * b)
                icon_pressed.set_at((x, y), (r, g, b))

        self.icon = icon
        self.icon_pressed = icon_pressed

    def render(self, display):
        """ Render the button """

        if self.clicked:
            icon = self.icon_pressed
        else:
            icon = self.icon

        display.blit(icon, self)


class SlideBar(BaseWidget):
    """
    A slide bar to bick a value in a range.
    
    Don't forget to call focus() and unfocus() when the user click on the SlideBar
    """

    def __init__(self, func, pos, size, min_=0, max_=100, step=1, color=BLUE, *, bg_color=LIGHT_GREY, show_val=True,
                 interval=1, anchor=CENTER, inital=None, rounding=2, v_type=int):
        """
        Creates a SlideBar.
        
        Use focus() when the user selects the bar and unfous() when he release the SB.
        
        :param size: widget size. Can be a callable or a 2-tuple.
        :param pos: widget position. Can be a callable or a 2-tuple.
        :param anchor: widget anchor
        :param show_val: if False, doesn't display the value on the cursor
        :param func: Callback function when a value is changed
        :param min_: The eminimum value of the picker
        :param max_: The maximum value of the picker
        :param step: The step
        :param color: color of the cursor
        :param bg_color: color of the background
        :param interval: minimum milisec elapsed between two calls to *func*
        :param inital: initial value for the SB
        :param rounding: number of digits to round values
        :param v_type: type of value. Can be float/int/Decimal/Fraction etc.
            you will have an object of this type using get()
        """

        super().__init__(pos, size, anchor)

        self.color = color
        self.bg_color = bg_color
        self.func = func
        self._value = inital if inital is not None else min_
        self.min = min_
        self.max = max_
        self.step = step
        self.show_val = show_val
        self.rounding = rounding
        self.v_type = v_type

        font = Font(self.height // 2)
        self.text_val = SimpleText(self.get, lambda: (self.value_px, self.centery), bw_contrasted(self.color), font)

        self.interval = interval

    def __repr__(self):
        # return f'SlideBar({self.min}:{self.max}:{self.step}; {super().__repr__()}, Value: {self.get()})'
        return 'SlideBar({}:{}:{}; {}, Value: {})'.format(self.min, self.max, self.step, super().__repr__(), self.get())

    def get(self):
        """ The current value of the bar """
        return round(self.v_type(self._value), self.rounding)

    def set(self, value):
        """ Set the value of the bar. If the value is out of bound, sets it to an extremum """
        value = min(self.max, max(self.min, value))
        self._value = value
        start_new_thread(self.func, (self.get(),))

    def _start(self):
        """ Starts checking if the SB is shifted """

        last_call = 42
        while self._focus:
            sleep(1 / 100)

            mouse = pygame.mouse.get_pos()
            last_value = self.get()
            self.value_px = mouse[0]

            # we do not need to do anything when it the same value
            if self.get() == last_value:
                continue

            if last_call + self.interval / 1000 < time():
                last_call = time()
                self.func(self.get())

    def focus(self):
        """ Gives the focus to the widget """
        self._focus = True

        start_new_thread(SlideBar._start, (self,))

    @property
    def value_px(self):
        """ The position in pixels of the cursor """
        step = self.w / (self.max - self.min)
        return self.x + step * (self.get() - self.min)  # -self.min so self.x is the minimum possible place

    @value_px.setter
    def value_px(self, value):
        value = min(self.right, max(self.left, value))

        delta_x = value - self.x
        prop = delta_x / self.width
        real = prop * (self.max - self.min)
        self._value = self.min + round(real / self.step) * self.step

    def render(self, display):
        """ Renders the bar on the display """

        # the bar
        bar_rect = pygame.Rect(0, 0, self.width, self.height // 3)
        bar_rect.center = self.center
        display.fill(self.bg_color, bar_rect)

        # the cursor
        circle(display, (self.value_px, self.centery), self.height // 2, self.color)

        # the value
        if self.show_val:
            self.text_val.render(display)


__all__ = ["Button", "IconButton", "SlideBar"]

if __name__ == '__main__':
    from GUI.gui_examples.buttons import gui
    gui()
