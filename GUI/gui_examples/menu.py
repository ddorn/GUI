
from pygame.constants import MOUSEBUTTONDOWN, KEYDOWN, QUIT

from GUI.locals import BLACK, PUMPKIN, PINK, WHITE, RED, GREEN
from GUI.menu import Menu
from GUI.vracabulous import Windows


class MenuExample(Windows):

    """An example of usage of Menu."""

    NAME = 'Menu Example'
    SCREEN_SIZE = 300, 300
    EVENT_ALLOWED = MOUSEBUTTONDOWN|KEYDOWN|QUIT

    def   __init__(self):
        super().__init__()
        self.menu = Menu((0, 0), lambda:(150, self.SCREEN_SIZE[0]))\
            .add_item('Kubrick', RED)\
            .add_item('Disney')\
            .add_item('The Pink Panthere')\
            .add_item('E.T.')\
            .add_item('2001')\
            .add_item('Pirates of Caribeans', GREEN)\
            .add_item('Oui-oui')

    def render(self):
        self.screen.fill(WHITE)
        self.menu.render(self.screen)
        # self.fps.render(self.screen)

    def update_on_event(self, e):
        super(MenuExample, self).update_on_event(e)
        self.menu.update(e)


if __name__ == '__main__':
    MenuExample().run()

