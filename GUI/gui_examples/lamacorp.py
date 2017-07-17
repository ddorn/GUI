import pygame

import colour
from pygame.constants import RESIZABLE

from GUI.base import BaseWidget

from GUI.buttons import Button, RoundButton
from GUI.colors import name2rgb, mix
from GUI.font import Font, BoldFont
from GUI.geo.basics import Rectangle, Line
from GUI.locals import TOPLEFT, BLUE, BOTTOMRIGHT, GOLD, WHITESMOKE, CONCRETE, TOPRIGHT, WHITE, CENTER
from GUI.text import SimpleText
from GUI.vracabulous import Window, Separator as Sep

pygame.init()


class List(BaseWidget):
    def __init__(self, pos, size, anchor=CENTER):
        super().__init__(pos, size, anchor)

        self._cells = []

    def render(self, surf):
        for cell in self.visible_cells():
            cell.render(surf)

    def update(self, event_or_list):
        pass


class ListCell(BaseWidget):
    pass


class Lamacorp(Window):

    NAME = 'Llama & Co.'
    VIDEO_OPTIONS = RESIZABLE
    SCREEN_SIZE = 970, 600
    BACKGROUND_COLOR = WHITE
    BORDER_COLOR = GOLD
    FPS = 1000
    SHOW_FPS = 1

    def __init__(self):
        super(Lamacorp, self).__init__()

        header_size = 60
        h_color = BLUE
        nb_button = 8
        button_size = lambda:(self.SCREEN_SIZE[0] - 40) / nb_button

        self.tab = None
        self.header = self.add(Rectangle((0, 0), lambda: (self.SCREEN_SIZE[0], header_size), h_color))
        self.line = self.add(Line((0, header_size), lambda: (self.SCREEN_SIZE[0], header_size), GOLD))
        self.title = self.add(
            SimpleText(self.NAME, (16, 8), GOLD, h_color, BoldFont(header_size - 16, Font.PIXEL, BoldFont.LIGHT),
                       TOPLEFT)
        )

        def get_funcs(color, i, row):
            def _pos():
                return int(20 + button_size() * i), header_size + 8 + 38 * row

            def _size():
                return int(button_size() - 6), 30

            def _action():
                rgb = name2rgb(color)
                rgb_light = mix(WHITESMOKE, rgb, 0.6)
                self.line.color = rgb_light
                self.BORDER_COLOR = rgb
                self.header.color = rgb
                self.title.bg_color = rgb
                self.die.color = 255 - rgb[0], 255 - rgb[1], 255 - rgb[2]
                self.title.color = WHITESMOKE
                self.choose_hint.text = str(color.hex).capitalize()
                self.choose_hint.color = rgb
                self.quit.color = rgb
                self.tab = color
                print(color, color.rgb, color.hex)

            text = texts[row][i % len(texts[row])]

            return _action, _pos, _size, text

        start = colour.Color("green"), colour.Color("#00caca")
        end = colour.Color('gold'), colour.Color('navy')
        texts = [
            "That's some beautiful colors and buttons man ! :P Yolooo".split(),
            'There is 64 differents types of buttons ! :o :P'.split()
        ]

        # the buttons
        for row in range(2):
            for i, color in enumerate(start[row].range_to(end[row], nb_button)):
                self.add(Button(*get_funcs(color, i, row), name2rgb(color), TOPLEFT, 4 * i + 32 * row))

        self.die = self.add(
            RoundButton(pygame.display.iconify, lambda: self.SCREEN_SIZE + Sep(-10, -10), 40, 'Die', h_color,
                        BOTTOMRIGHT), lambda: self.tab
        )

        self.quit = self.add(
            RoundButton(quit, lambda: (self.SCREEN_SIZE[0] - 8, 8), header_size // 2 - 8, 'X', h_color, TOPRIGHT,
                        Button.NO_MOVE | Button.NO_SHADOW)
        )

        self.choose_hint = self.add(
            SimpleText('Choose your color !', lambda:(self.SCREEN_SIZE[0] // 2, (self.SCREEN_SIZE[1] + header_size) // 2),
                       CONCRETE, self.BACKGROUND_COLOR, Font(50)),
            # lambda: False
        )

        self.rounded = self.add(
            Rectangle((120, 40), (300, 300), color=(0, 0, 255, 120), style=Rectangle.ROUNDED)
        )


if __name__ == '__main__':
    Lamacorp().run()
