from pygame import font
try:
    from .locals import *
except ImportError:
    from locals import *
font.init()

class Font(font.Font):
    def __init__(self, size, file=GUI_PATH + '/segoeuil.ttf'):
        super(Font, self).__init__(file, size)

DEFAULT = Font(20)


__all__ = ['Font', 'DEFAULT']