"""
This module provides a few buttons for an easy pygame GUI.
"""

import pygame
from _thread import start_new_thread
from time import time, sleep

from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

from GUI.base import BaseWidget
from GUI.colors import bw_contrasted, mix
from GUI.draw import circle, roundrect
from GUI.font import Font
from GUI.locals import CENTER, BLUE, LIGHT_GREY, BLACK, ORANGE, GREEN
from GUI.text import SimpleText
from GUI.vracabulous import Separator


class BaseButton(BaseWidget):
    """Abstract base class for any button"""

    CALL_ON_PRESS = 1
    THREADED_CALL = 2

    def __init__(self, func, pos, size, anchor, flags=0):
        """
        Creates a new BaseButton object.
        
        :param func: calback function that takes no argument
        :param pos: the widget pos. Can be a callable or a 2-tuple
        :param size: the width size. Can be a callable or a 2-tuple
        :param flags: Can be:
            - CALL_ON_PRESS if you want func to be call when the button is pressed instead of when it's released
            - THREADED_CALL if you want func to be called in a thread
            You can pass multiple flags with the pipe operator |
        """
        super().__init__(pos, size, anchor)
        self.func = func
        self.flags = flags

    def click(self, force_no_call=False, milis=None):
        """
        Call when the button is pressed. This start the callback function in a thread
        If :milis is given, will release the button after :milis miliseconds
        """

        if self.clicked:
            return False

        if not force_no_call and self.flags & self.CALL_ON_PRESS:
            if self.flags & self.THREADED_CALL:
                start_new_thread(self.func, ())
            else:
                self.func()

        super().click()

        if milis is not None:
            start_new_thread(self.release, (), {'milis': milis})

    def release(self, force_no_call=False, milis=0):
        """
        Call this when the button is released
        Blocks for :milis miliseconds (used by .press() for auto release)
        """
        if not self.clicked:
            return False

        if milis:
            sleep(milis / 1000)

        super().release()

        if force_no_call:
            return

        if not self.flags & self.CALL_ON_PRESS:
            if self.flags & self.THREADED_CALL:
                start_new_thread(self.func, ())
            else:
                self.func()

    def render(self, surf):
        raise NotImplementedError


class Button(BaseButton):
    """A basic button."""

    NO_MOVE = 4
    NO_SHADOW = 8
    NO_ROUNDING = 16
    NO_HOVER = 32

    def __init__(self, func, pos, size, text='', color=ORANGE, anchor=CENTER, flags=0):
        """
        Creates a clickable button.
        
        :param func: callback function with no arguments
        :param size: widget size. Can be a callable or a 2-tuple.
        :param pos: widget position. Can be a callable or a 2-tuple.
        :param anchor: widget anchor
        :param text: Text to be displayed on the button
        :param color: the natural color of the button
        :param flags: see BaseButton
        """

        super().__init__(func, pos, size, anchor, flags)

        self.color = color
        self.hovered = False
        self.hover_enabled = True
        self.pressed = False
        self.text = SimpleText(text, lambda: self.center, bw_contrasted(self.color), self.color,
                               Font(self.height - 6, unit=Font.PIXEL))

    def _get_color(self):
        """Return the color of the button, depending on its state"""
        if self.clicked and self.hovered:  # the mouse is over the button
            color = mix(self.color, BLACK, 0.8)

        elif self.hovered and not self.flags & self.NO_HOVER:
            color = mix(self.color, BLACK, 0.93)

        else:
            color = self.color

        self.text.bg_color = color
        return color

    @property
    def _front_delta(self):
        """Return the offset of the colored part."""
        if self.flags & self.NO_MOVE:
            return Separator(0, 0)

        if self.clicked and self.hovered:  # the mouse is over the button
            delta = 2

        elif self.hovered and not self.flags & self.NO_HOVER:
            delta = 0

        else:
            delta = 0

        return Separator(delta, delta)

    @property
    def _bg_delta(self):
        """Return the offset of the shadow."""
        if self.flags and self.NO_MOVE:
            return Separator(2, 2)

        if self.clicked and self.hovered:  # the mouse is over the button
            delta = 2

        elif self.hovered and not self.flags & self.NO_HOVER:
            delta = 2

        else:
            delta = 2

        return Separator(delta, delta)

    def update(self, event_or_list):
        """Update the button with the events."""

        for e in super().update(event_or_list):
            if e.type == MOUSEBUTTONDOWN:
                if e.pos in self:
                    self.click()
                else:
                    self.release(force_no_call=True)

            elif e.type == MOUSEBUTTONUP:
                self.release(force_no_call=e.pos not in self)

            elif e.type == MOUSEMOTION:
                if e.pos in self:
                    self.hovered = True
                else:
                    self.hovered = False

    def render(self, surf):
        """Render the button on a surface."""
        pos, size = self.topleft, self.size

        if not self.flags & self.NO_SHADOW:
            if self.flags & self.NO_ROUNDING:
                pygame.draw.rect(surf, LIGHT_GREY, (pos + self._bg_delta, size))
            else:
                roundrect(surf, (pos + self._bg_delta, size), LIGHT_GREY + (100,), 5)

        if self.flags & self.NO_ROUNDING:
            pygame.draw.rect(surf, self._get_color(), (pos + self._front_delta, size))
        else:
            roundrect(surf, (pos + self._front_delta, size), self._get_color(), 5)

        self.text.center = self.center + self._front_delta
        self.text.render(surf)


class RoundButton(Button):
    def __init__(self, func, pos, radius: int, text='', color=GREEN, anchor=CENTER, flags=0):
        super().__init__(func, pos, (radius * 2, radius * 2), text, color, anchor, flags)

        self.text = SimpleText(text, lambda: self.center, bw_contrasted(self.color), self.color,
                               Font(self.height // 2, unit=Font.PIXEL))

    def render(self, surf):
        """Draw the button on the surface."""
        if not self.flags & self.NO_SHADOW:
            circle(surf, self.center + self._bg_delta, self.width / 2, LIGHT_GREY)
        circle(surf, self.center + self._front_delta, self.width / 2, self._get_color())

        self.text.center = self.center + self._front_delta
        self.text.render(surf)


class IconButton(BaseButton):
    """A button with a **square** icon intead of a text."""

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

        self.icon = icon
        self.icon_pressed = self.get_darker_image()

    def get_darker_image(self):
        """Returns an icon 80% more dark"""
        icon_pressed = self.icon.copy()

        for x in range(self.w):
            for y in range(self.h):
                r, g, b, *_ = tuple(self.icon.get_at((x, y)))
                const = 0.8
                r = int(const * r)
                g = int(const * g)
                b = int(const * b)
                icon_pressed.set_at((x, y), (r, g, b))

        return icon_pressed

    def render(self, surf):
        """Render the button"""

        if self.clicked:
            icon = self.icon_pressed
        else:
            icon = self.icon

        surf.blit(icon, self)


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
        """The current value of the bar"""
        return round(self.v_type(self._value), self.rounding)

    def set(self, value):
        """Set the value of the bar. If the value is out of bound, sets it to an extremum"""
        value = min(self.max, max(self.min, value))
        self._value = value
        start_new_thread(self.func, (self.get(),))

    def _start(self):
        """Starts checking if the SB is shifted"""

        # TODO : make an update method instead

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
        """Gives the focus to the widget"""
        self._focus = True

        start_new_thread(SlideBar._start, (self,))

    @property
    def value_px(self):
        """The position in pixels of the cursor"""
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
        """Renders the bar on the display"""

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
