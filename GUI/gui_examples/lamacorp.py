import pygame

import colour
from pygame.constants import NOFRAME

from GUI.buttons import Button, RoundButton
from GUI.colors import name2rgb, mix
from GUI.font import Font, BoldFont
from GUI.geo.basics import Rectangle, Line
from GUI.locals import TOPLEFT, BLUE, BOTTOMRIGHT, GOLD, WHITESMOKE, WHITE, BLACK, CONCRETE, RED, TOPRIGHT
from GUI.text import SimpleText
from GUI.vracabulous import Window, Separator as Sep


class Lamacorp(Window):

    VIDEO_OPTIONS = NOFRAME
    SCREEN_SIZE = 970, 600
    BACKGROUND = WHITESMOKE

    def __init__(self):
        super(Lamacorp, self).__init__()

        header_size = 60
        h_color = BLUE
        nb_button = 7
        button_size = (self.SCREEN_SIZE[0] - 40) / nb_button

        self.tab = None
        self.header = self.add(Rectangle((0, 0), lambda: (self.SCREEN_SIZE[0], header_size), h_color))
        self.line = self.add(Line((0, header_size), lambda: (self.SCREEN_SIZE[0], header_size), GOLD))
        self.title = self.add(
            SimpleText('Llamas & Co.', (16, 8), GOLD, h_color, BoldFont(header_size - 16, Font.PIXEL, BoldFont.LIGHT),
                       TOPLEFT)
        )

        def action(color):
            def _func():
                rgb = name2rgb(color)
                rgb_light = mix(WHITESMOKE, rgb, 0.6)
                self.line.color = rgb_light
                self.border.color = rgb_light
                self.header.color = rgb
                self.title.bg_color = rgb
                self.die.color = 255 - rgb[0], 255 - rgb[1], 255 - rgb[2]
                self.title.color = WHITESMOKE
                self.tab = color
                print(color, color.rgb, color.hex)

            return _func

        start = colour.Color("red")
        end = colour.Color('blue')
        texts = "That's some beautiful colors man ! :P".split()
        for i, color in enumerate(start.range_to(end, nb_button)):
            self.add(
                Button(action(color), (int(20 + button_size * i), header_size + 6), (int(button_size - 6), 30),
                            texts[i % len(texts)], name2rgb(color), TOPLEFT)
            )

        self.die = self.add(
            RoundButton(pygame.display.iconify, lambda: self.SCREEN_SIZE + Sep(-10, -10), 40, 'Die', h_color,
                        BOTTOMRIGHT), lambda: self.tab
        )

        self.quit = self.add(
            RoundButton(quit, lambda:(self.SCREEN_SIZE[0] -8, 8), header_size // 2 - 8, 'X', RED, TOPRIGHT, Button.NO_MOVE | Button.NO_SHADOW)
        )

        self.choose_hint = self.add(
            SimpleText('Choose your color !', (self.SCREEN_SIZE[0] // 2, (self.SCREEN_SIZE[1] + header_size) // 2),
                       CONCRETE, self.BACKGROUND, Font(50)),
            lambda: self.tab is None
        )
        self.border = self.add(Rectangle((0, 0), lambda: self.SCREEN_SIZE, GOLD, Rectangle.BORDER))


if __name__ == '__main__':
    Lamacorp().run()
