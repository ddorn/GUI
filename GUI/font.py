from pygame import font

try:
    from .locals import *
except ImportError:
    from GUI.locals import *
font.init()


class Font(font.Font):
    """ A pygame.font.Font font, with no aditionnal methodes but provide a good default behavior. """

    def __init__(self, size=20, file=GUI_PATH + '/segoeuil.ttf'):
        """
        Creates a Font object.
        
        :param size: The font size (See http://www.pygame.org/docs/ref/font.html#pygame.font.Font for more infos)
        :param file: The file of the font file
        """
        super(Font, self).__init__(file, size)
        self.font_size = size
        self.font_name = file


DEFAULT = Font(20)

__all__ = ['Font', 'DEFAULT']
