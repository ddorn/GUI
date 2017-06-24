"""A module to make easy menus."""
import pygame
from pygame.constants import *

from GUI.draw import line
from GUI.font import Font, DEFAULT_FONT
from GUI.geo.basics import Rectangle
from GUI.base import BaseWidget
from GUI.colors import mix, bw_contrasted
from GUI.locals import TOPLEFT, CONCRETE, BLACK, LIGHT_GREY, WHITE
from GUI.text import SimpleText
from GUI.vracabulous import Separator as Sep


class Menu(BaseWidget):

    def __init__(self, pos, size, anchor=TOPLEFT, item_size=20, sep_color=CONCRETE):
        super().__init__(pos, size, anchor)
        self.structure = []
        self.item_size = item_size
        self.sep_color = sep_color

    def __repr__(self):
        return "<Menu({})>".format(self.structure)

    def _get_next_pos(self):
        if not self.structure:
            return self.topleft
        else:
            return self.structure[-1].bottomleft

    def _get_color_of_elt(self, color):
        if color is None:
            return [BLACK, mix(BLACK, WHITE, 0.7)][len(self.structure) % 2]
        else:
            return color

    def _get_background_color_of_elt(self):
        return [WHITE, (240, 240, 240)][1 - len(self.structure) % 2]

    def add_category(self, name, color=None):

        size = int(1.5*self.item_size)

        self.structure.append(MenuCategory(
            self,
            name,
            self._get_next_pos(),
            (self.width, size),
            TOPLEFT,
            self.item_size,
            self._get_color_of_elt(color),
            self.sep_color
        ))

        return self

    def add_item(self, name, color=None):
        if self.structure and isinstance(self.structure[-1], MenuCategory):
            self.structure[-1].add_item(name, color)

        else:
            self.structure.append(MenuElement(
                name,
                self._get_next_pos(),
                (self.width, self.item_size),
                self._get_color_of_elt(color),
                self._get_background_color_of_elt(),
                Font(self.item_size, unit=Font.PIXEL)
            ))

        return self

    def render(self, surf):
        # self.structure[0].render(surf)

        # i points to the last element, as we start the enumaration at one.
        for elt in self.structure:
            # line(surf,
            #      (self.left, self.structure[i].bottom),
            #      (self.right, self.structure[i].bottom),
            #      self.sep_color)
            elt.render(surf)
        # line(surf,
        #      (self.left, self.structure[-1].bottom),
        #      (self.right, self.structure[-1].bottom),
        #      self.sep_color)

        line(surf, self.topright, self.bottomright, self.sep_color)

    def update(self, event_or_list):
        event_or_list = super(Menu, self).update(event_or_list)

        mouse = pygame.mouse.get_pos()

        for e in event_or_list:
            if e.type == MOUSEBUTTONDOWN:
                if mouse in self:
                    for elt in self.structure:
                        if mouse in elt.rect:
                            elt.choose()
                            for elt2 in self.structure:
                                if elt2 != elt:
                                    elt2.stop_choose()

        if mouse in self:
            for elt in self.structure:
                if mouse in elt.rect:
                    elt.highlight()
                    for elt2 in self.structure:
                        if elt2 != elt:
                            elt2.stop_highlight()


class MenuElement(SimpleText):

    def __init__(self, name, pos, size, color=BLACK, bg_color=None, font=DEFAULT_FONT):
        self.rect = Rectangle(pos, size, bg_color)

        self.choosed = False
        self._true_color = bg_color
        super().__init__(name, pos, color, None, font, TOPLEFT)

    def __repr__(self):
        return "<MenuElement({})>".format(self.text)

    def choose(self):
        """Marks the item as the one the user is in."""
        if not self.choosed:
            self.choosed = True
            self.pos = self.pos + Sep(5, 0)

    def stop_choose(self):
        """Marks the item as the one the user is not in."""
        if self.choosed:
            self.choosed = False
            self.pos = self.pos + Sep(-5, 0)

    def highlight(self):
        self.rect.color = self.get_darker_color()

    def stop_highlight(self):
        self.rect.color = self._true_color

    def get_darker_color(self):
        """The color of the clicked version of the MenuElement. Darker than the normal one."""
        # we change a bit the color in one direction
        if bw_contrasted(self._true_color, 30) == WHITE:
            color = mix(self._true_color, WHITE, 0.9)
        else:
            color = mix(self._true_color, BLACK, 0.9)

        return color

    def render(self, screen):
        """Renders the MenuElement"""
        self.rect.render(screen)
        super(MenuElement, self).render(screen)



class MenuCategory(Menu):
    def __init__(self, parent, name, pos, size, anchor=TOPLEFT, item_size=20, color=CONCRETE, bg_color=WHITE,
                 sep_color=CONCRETE):

        super().__init__(pos, size, anchor, item_size, sep_color)

        self.parent = parent
        self.title = SimpleText(name, pos)#, color, bg_color, BoldFont(self.height, BoldFont.POINT), TOPLEFT)
        self.structure.append(self.title)

    def __repr__(self):
        return "<MenuCategory({})>".format(self.structure)
