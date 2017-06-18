import pygame

from GUI import SimpleText, LaText, Font
from GUI.locals import *


def gui():
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


if __name__ == '__main__':
    gui()
