import pygame


class BaseWidget(pygame.Rect):
    def __init__(self, rect):
        super().__init__(rect)
        
        self._focus = False

    def __contains__(self, item):
        """Test if a point is in the button"""
        return self.collidepoint(*item)

    def focus(self):
        print('Focus on %s' %self)
        self._focus = True
        
    def unfocus(self):
        print('Unfocus on %s' %self)

        self._focus = False
