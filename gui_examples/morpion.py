# coding=utf-8
import os
import pygame
from pygame import gfxdraw
from pygame.locals import *
from random import randint, choice

from GUI.draw import *
from GUI.draw import ring
from GUI.locals import *

SCREEN_SIZE = 500, 500
FPS = 60

DARK = [44, 62, 80]
RED = (231, 76, 60)


class Morpion(object):
    TIC = 42
    TOC = 69

    def __init__(self):
        self.grid = [[0, 0, 0] for _ in range(3)]
        self._hint = None
        self.turn = 42 + 27*randint(0, 1)
        self.won = None

    def tic(self, x, y):
        if not self.grid[x][y]:
            self.grid[x][y] = self.TIC
            self.turn = self.TOC

        else:
            raise IndexError

    def toc(self, x, y):
        if not self.grid[x][y]:
            self.grid[x][y] = self.TOC
            self.turn = self.TIC

        else:
            raise IndexError

    def play(self, x, y):
        if self.is_won():
            return

        if self.turn == self.TIC:
            self.tic(x, y)
        else:
            self.toc(x, y)

        self._hint = None

    def is_won(self):
        if self.won is not None:
            return self.won

        a = b = d1 = d2 = True
        for i in range(3):
            a = b = True
            for j in range(3):
                if a and a is True or a == self.grid[i][j]:
                    a = self.grid[i][j]
                else:
                    a = False

                if b and b is True or b == self.grid[j][i]:
                    b = self.grid[j][i]
                else:
                    b = False

            if a or b:
                break

            if d1 and d1 is True or d1 == self.grid[i][i]:
                d1 = self.grid[i][i]
            else:
                d1 = False

            if d2 and d2 is True or d2 == self.grid[i][2 - i]:
                d2 = self.grid[i][2 - i]
            else:
                d2 = False

        for cond in (a, b, d1, d2):
            if cond:
                self.won = cond
                return cond

        return False

    def render(self, screen):
        for i in range(2, 4):
            line(screen, (100 * i, 100), (100 * i, 400), DARK, 8, ROUNDED)
            line(screen, (100, 100 * i), (400, 100 * i), DARK, 8, ROUNDED)

        for x in range(3):
            for y in range(3):
                if self.grid[x][y] == self.TIC:
                    self.render_tic(screen, x, y)

                elif self.grid[x][y] == self.TOC:
                    self.render_toc(screen, x, y)

        if self._hint and not self.won:
            if self.turn == self.TOC:
                self.render_toc(screen, *self._hint, True)
            else:
                self.render_tic(screen, *self._hint, True)

        won = self.is_won()
        if won == self.TIC:
            pos = 250, 250
            ring(screen, pos, 125, 30, GREEN)
        if won == self.TOC:
            line(screen, (150, 150), (350, 350), RED, 30, ROUNDED)
            line(screen, (350, 150), (150, 350), RED, 30, ROUNDED)

    def render_tic(self, screen, x, y, hint=False):
        pos = (150 + 100 * x, 150 + 100 * y)

        color = GREEN
        if hint or self.won:
            color = (149, 165, 166)

        circle(screen, pos, 40, color)
        circle(screen, pos, 28, WHITE)

    def render_toc(self, screen, x, y, hint=False):
        xx = 100 * x
        yy = 100 * y
        pos1 = 120 + xx, 120 + yy
        pos2 = pos1[0] + 60, pos1[1]
        pos3 = pos1[0], pos1[1] + 60
        pos4 = pos2[0], pos3[1]

        color = RED
        if hint or self.won:
            color = (149, 165, 166)

        line(screen, pos1, pos4, color, 12, ROUNDED)
        line(screen, pos2, pos3, color, 12, ROUNDED)

    def free_cases(self):
        for x in range(3):
            for y in range(3):
                if not self.grid[x][y]:
                    yield x, y

    def hint(self, x=None, y=None):

        cases = [c for c in self.free_cases()]

        if None in (x, y):
            if cases:
                self._hint = choice(cases)

        else:
            if (x, y) in cases:
                self._hint = x, y

    def is_full(self):
        for l in self.grid:
            for c in l:
                if not c:
                    return False

        return True


def pos_from_mouse(mouse):
    x, y = mouse
    if 100 <= x < 400 and 100 <= y < 400:
        x = (x - 100) // 100
        y = (y - 100) // 100

        return x, y

    return None


def gui():
    """ Main function """

    # #######
    # setup all objects
    # #######
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF | NOFRAME)
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])

    game = Morpion()
    turn = randint(1, 2)

    run = True
    while run:

        # #######
        # Input loop
        # #######

        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == QUIT:
                run = False

            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    run = False

                if e.key == K_F4 and e.mod & KMOD_ALT:
                    return 0

            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if pos_from_mouse(mouse):

                        if game.is_full() or game.is_won():
                            game = Morpion()
                            continue

                        x, y = pos_from_mouse(mouse)

                        try:
                            game.play(x, y)
                        except IndexError:
                            pass

        if pos_from_mouse(mouse):
            x, y = pos_from_mouse(mouse)
            game.hint(x, y)

        # #######
        # Draw all
        # #######

        screen.fill(WHITE)
        game.render(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    gui()
