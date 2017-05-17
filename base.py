""" The very bases of the GUI module """

import pygame


class BaseWidget(pygame.Rect):
    """ The base class for any widget """
    
    def __init__(self, rect):
        """
        Creates a 
        :param rect: A pygame Rect-like object (can be a tuple of 4 values.
        """
        super().__init__(rect)
        
        self._focus = False

    def __contains__(self, item):
        """ Test if a point is in the widget """
        return self.collidepoint(*item)

    def focus(self):
        """ Gives the focus to the widget """
        self._focus = True
        
    def unfocus(self):
        """ Takes back the focus from the widget """
        self._focus = False


__all__ = ['BaseWidget']
