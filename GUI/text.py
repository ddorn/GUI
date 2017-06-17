"""
A module to easily render text on the screen.
"""
import os
import pygame
import tempfile

try:
    from .font import *
    from .locals import *
    from .base import BaseWidget
except ImportError:
    from GUI.font import *
    from GUI.locals import *
    from GUI.base import BaseWidget
pygame.font.init()


class SimpleText(BaseWidget):
    """ A simple brut text to draw on the screen """

    def __init__(self, text, pos, color=BLUE, bg_color=None, font=DEFAULT, anchor='center'):
        """
        Creates a new SimpleText object.
        
        :param text: The string or a callable (no args) that returns the string to dislay
        :param pos: the position of the text
        :param color: the color of the text
        :param font: a pygame.Font object
        :param anchor: the anchor of the text.
            See http://www.pygame.org/docs/ref/rect.html#pygame.Rect for a list of possible anchors.
        """

        super().__init__(pos, (0, 0), anchor)

        self.font = font
        self._color = color
        self._bg_color = bg_color
        self._last_text = ...
        self._text = text
        self._surface = pygame.Surface((1, 1))  # placeholder

        self._render()

    def __str__(self):
        return self.text

    @property
    def text(self):
        """ Returns the string to render """

        if callable(self._text):
            return str(self._text())
        return str(self._text)

    @text.setter
    def text(self, value):
        """ Sets the text to a new string or callable. Renders the text if needed. """

        if value != self._text:
            self._text = value

    @property
    def color(self):
        return self._color

    @property
    def bg_color(self):
        return self._bg_color

    @color.setter
    def color(self, value):
        """ Sets the color to a new value (tuple). Renders the text if needed. """

        if value != self.color:
            self._color = value
            self._render()

    @bg_color.setter
    def bg_color(self, value):
        """ Sets the color to a new value (tuple). Renders the text if needed. """

        if value != self.bg_color:
            self._bg_color = value
            self._render()

    def _render(self):
        """ Render the text.
            Avoid using this fonction too many time as it is slow as it is low to render text and blit it. """

        self._last_text = self.text

        self._surface = self.font.render(self.text, True, self.color, self.bg_color)
        rect = self._surface.get_rect()

        self.size = rect.size

    def render(self, display):
        """ Render basicly the text """

        # to handle changing objects / callable
        if self.text != self._last_text:
            self._render()

        display.blit(self._surface, (self.topleft, self.size))


class LaText(SimpleText):
    """ This class provides a nice rendering for maths equations based on latex. """

    def __init__(self, text, pos, color=BLUE, font=DEFAULT, anchor='center'):
        """
        The latex _interface_ provides a well looking display of math exquations.
        
        However, you can NOT use function that are not in the amsmath/amsfont or standard package.
        
        :param text: The string or a callable (no args) that returns the string to dislay. The string must be a valid
            LaTex text, without the headers (only the document environement.
        :param pos: the position of the text
        :param color: the color of the text
        :param font: a pygame.Font object. Its size will be chosent for the LeTeX size.
            Too big sizes (> 24.88) does not work
        :param anchor: the anchor of the text.
            See http://www.pygame.org/docs/ref/rect.html#pygame.Rect for a list of possible anchors.
        """

        super().__init__(text, pos, color, font, anchor)

    @staticmethod
    def latex_to_img(tex):
        with tempfile.TemporaryDirectory() as tmpdirname:
            
            with open(tmpdirname + r'\tex.tex', 'w') as f:
                f.write(tex)
            os.system('latex2png ' + tmpdirname)

            image = pygame.image.load(tmpdirname + r'\tex.png')
        
        return image

    def _render(self):

        self._last_text = self.text

        name = GUI_PATH + '/.temp/matheq' + str(id(self)) + '.png'

        # generates the LaTeX text
        preamble = r"""\documentclass[40pt]{article}\pagestyle{empty}""" + \
                   r"\usepackage{color}" + \
                   r"\usepackage{amsmath}" + \
                   r"\usepackage{amsfonts}" + \
                   r"\definecolor{kkolor}{RGB}{%i, %i, %i}" % self.color + \
                   r"\begin{document}"

        font_setter = r"\fontsize{%i pt}{%i pt}\selectfont" % (self.font.font_size, self.font.font_size * 1.2)
        color_setter = r"{\color{kkolor}"
        end_color_setter = '}'
        end = r'\end{document}'
        text = preamble + font_setter + color_setter + self.text + end_color_setter + end

        # generates the LaTeX png
        self._surface = self.latex_to_img(text)

        # load it
        rect = self._surface.get_rect()

        self.size = rect.size

        try:
            os.remove(name)
        except FileNotFoundError:
            pass


__all__ = ['SimpleText', 'LaText']


if __name__ == '__main__':
    screen = pygame.display.set_mode((400, 200))

    normal_text = SimpleText("42, c'est moi !", (270, 20), GREEN, anchor=MIDTOP)
    math_text = LaText(r'$$\sqrt{2}^{7x+3}\times\sum_{k=0}^{\infty} 3A_kf(ke^{i\pi})= 0$$', (200, 100))
    matrix = LaText(r"""
\[
M=
  \begin{bmatrix}
    1 & 2 & 3 & 4 & 5 \\
    3 & 4 & 5 & 6 & 7
  \end{bmatrix}
\]
""", (300, 150), color=RED, font=Font(10))
    pi = LaText('$$\pi$$', (84, 42), LIGHT_GREY, font=Font(24))  # Too big fonts doesn't works, max is 24

    pi_size = 24
    run = True
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    pi_size = max(pi_size - 1, 1)
                if e.button == 5:
                    pi_size += 1
                pi.font.font_size = pi_size
                pi.text = pi_size

        screen.fill((250, 250, 250))
        math_text.render(screen)
        matrix.render(screen)
        pi.render(screen)
        normal_text.render(screen)
        pygame.display.flip()
