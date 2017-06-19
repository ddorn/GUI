# coding=utf-8

import os
import pygame
from pygame.locals import *

from GUI import Separator as Sep, InLinePassBox, InLineTextBox, Button, FocusSelector, line
from GUI.geo import Rectangle
from GUI.locals import *

pygame.init()
# noinspection PyArgumentList
pygame.key.set_repeat(300, 40)

SCREEN_SIZE = 616, 30
FPS = 60


def new_widow():
    return pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF | NOFRAME)


def gui():
    """ Main function """

    global SCREEN_SIZE

    # #######
    # setup all objects
    # #######
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    screen = new_widow()
    pygame.display.set_caption('Client swag')
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])
    clock = pygame.time.Clock()
    # fps = FPSIndicator(clock)

    bound = Rectangle((0, 0), SCREEN_SIZE, BLUE, Rectangle.BORDER)
    login = InLineTextBox((5, 1), 200, MIDNIGHT_BLUE, anchor=TOPLEFT, default_text='Login: ')
    passw = InLinePassBox(login.topright + Sep(5, 0), 200, MIDNIGHT_BLUE, anchor=TOPLEFT, default_text='Password: ')

    def sup():
        print('Signed up !')
        print('login:', login.text)
        print('pass:', passw.text)

    def sin():
        print('Signed in !')
        print('login:', login.text)
        print('pass:', passw.text)

    sign_up = Button(sup, passw.topright + Sep(5, 0), (100, passw.height), 'Sign Up', YELLOW, anchor=TOPLEFT)
    sign_in = Button(sin, sign_up.topright, (100, passw.height), 'Sign In', GREEN, anchor=TOPLEFT)

    focus = FocusSelector(login, passw, sign_up, sign_in)
    focus.select(0)

    while True:

        # #######
        # Input loop
        # #######

        mouse = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == QUIT:
                return 0  # quit

            elif e.type == KEYDOWN:
                # intercept special inputs
                if e.key == K_ESCAPE:
                    return 0  # quit

                elif e.key == K_F4 and e.mod & KMOD_ALT:
                    return 0  # quit

                elif e.key == K_TAB:
                    if e.mod & KMOD_SHIFT:
                        focus.prev()
                    else:
                        focus.next()

                elif e.key == K_RETURN:
                    if focus.selected() in (sign_up, sign_in):
                        focus.selected().click(40)
                    else:
                        focus.next()

                else:
                    # or give them to the selected box
                    focus.selected().update(e)

            elif e.type == VIDEORESIZE:
                SCREEN_SIZE = e.size
                screen = new_widow()

            elif e.type == MOUSEBUTTONDOWN:
                if mouse in login:
                    focus.select(login)

                elif mouse in passw:
                    focus.select(passw)

                elif mouse in sign_up:
                    sign_up.click()

                elif mouse in sign_in:
                    sign_in.click()

            elif e.type == MOUSEBUTTONUP:
                sign_in.release()
                sign_up.release()

        # #######
        # Draw all
        # #######

        screen.fill(WHITE)
        # fps.render(screen)
        bound.render(screen)
        login.render(screen)
        passw.render(screen)
        line(screen, login.topright + Sep(2, 0), login.bottomright + Sep(2, 0), BLUE)
        sign_up.render(screen)
        sign_in.render(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    gui()
