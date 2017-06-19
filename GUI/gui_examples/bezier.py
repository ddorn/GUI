import pygame
from pygame.locals import *
from random import choice

from GUI import COLORS, WHITE, ORANGE, FPSIndicator, V2
from GUI.geo import Bezier, Point

SCREEN_SIZE = 800, 500
ALL = (0, 0), SCREEN_SIZE
FPS = 40


def gui():
    """ Main function """

    # #######
    # setup all objects
    # #######

    zones = [ALL]
    last_zones = []

    COLORS.remove(WHITE)

    screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)
    pygame.display.set_caption('Bezier simulator')
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])
    points = [
        (40, 40),
        (100, 400),
        (200, 100),
        (650, 420)
    ]
    bezier = Bezier((0, 0), SCREEN_SIZE, points, ORANGE, 8)
    points = [Point(p, 24, choice(COLORS)) for p in points]

    clock = pygame.time.Clock()
    fps = FPSIndicator(clock)
    dragging = None
    render = True

    while True:

        # #######
        # Input loop
        # #######

        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == QUIT:
                return 0

            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    return 0

                if e.key == K_F4 and e.mod & KMOD_ALT:
                    return 0

            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    dragging = not dragging

                if e.button == 3:
                    points.append(Point(mouse, 24, choice(COLORS)))
                    bezier.points.append(V2(mouse))
                    render = True

        if dragging:
            mdist = 10000
            the_p = None
            for i, p in enumerate(points):
                if p.dist_to(mouse) < mdist:
                    mdist = p.dist_to(mouse)
                    the_p = i

            render = points[the_p].pos != mouse
            points[the_p].pos = mouse
            bezier.points[the_p] = V2(mouse)

        # #######
        # Draw all
        # #######

        if render:
            render = False
            screen.fill(WHITE)
            bezier.render(screen)
            for p in points:
                p.render(screen)

            zones.append(ALL)

        _ = fps.render(screen)
        zones.append(_)

        pygame.display.update(zones + last_zones)
        last_zones = zones[:]
        zones.clear()

        clock.tick(FPS)


if __name__ == '__main__':
    gui()
