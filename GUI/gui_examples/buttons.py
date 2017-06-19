import pygame

from GUI import SlideBar, RED, Button, BOTTOMRIGHT, WHITE


def gui():
    display = pygame.display.set_mode((300, 200))

    sb = SlideBar(print, (150, 100), (200, 30), 0, 160, 1, interval=4)

    def func_b():
        sb.color = RED

    red = Button(func_b, (300, 200), (60, 40), 'RED', anchor=BOTTOMRIGHT)

    def func_sb(value):
        red.topright = 300, value

    sb.func = func_sb
    sb.set(0)

    run = True
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse in sb:
                    sb.focus()

                if mouse in red:
                    red.click()

            if event.type == pygame.MOUSEBUTTONUP:
                red.release()
                sb.unfocus()

        display.fill(WHITE)
        sb.render(display)
        red.render(display)
        pygame.display.flip()


if __name__ == '__main__':
    gui()
