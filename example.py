# -*- coding: utf-8 -*-

__author__ = 'Jorge'

__all__ = [
    'Textbox'
]

import pygame
from . import *
import pygame.locals as c


class TextBox(StrList):

    """Represents a visual controls for text editing."""

    def __init__(self, position, page_size=(80, 20)):
        super(TextBox, self).__init__(
            Caret()
        )
        self.position = position
        self.caret.page_size = page_size

