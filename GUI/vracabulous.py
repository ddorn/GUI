import pygame

from GUI.locals import FLASH_CREEN, TOPLEFT, MIDNIGHT_BLUE
from GUI.text import SimpleText


class FPSIndicator(SimpleText):
    def __init__(self, clock):
        self.clock = clock

        def text():
            return str(round(self.clock.get_fps()))

        super().__init__(text, (10, 14), FLASH_CREEN, MIDNIGHT_BLUE)

    def render(self, display):
        pygame.draw.rect(display, MIDNIGHT_BLUE, ((0, 0), (20, 28)))
        super().render(display)

        return (0, 0), (20, 28)
