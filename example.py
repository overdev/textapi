# -*- coding: utf-8 -*-

__author__ = 'Jorge A. Gomes'

__all__ = [
    'Textbox',
    'BmpFont'
]

import os
import pygame
from __init__ import *
import pygame.locals as c


def normalize_color(color):
    """Gets a 3-tuple of RGB ints and return a 3-tuple of unity floats"""
    return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)

def blend_color(a, b, r):
    """blends color a and b in r ratio."""
    return (
        int(a[0] + (b[0] - a[0]) * r[0]),
        int(a[1] + (b[1] - a[1]) * r[1]),
        int(a[2] + (b[2] - a[2]) * r[2])
    )


class BmpFont(object):

    image = pygame.image.load(os.path.join(os.getcwd(), "res/CBFG_Consolas_24x16_cp1252.png"))
    glyph_size = (16, 24)
    glyphs = u" !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~_¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"
    def_palette = image.get_palette()
    nrm_palette = [normalize_color(color) for color in def_palette]
    advance = 10

    @classmethod
    def set_colors(cls, forecolor, backcolor):
        for index in range(256):
            ratio = cls.nrm_palette[index]
            cls.image.set_palette_at(index, blend_color(backcolor, forecolor, ratio))

    @classmethod
    def get_texglyph(cls, glyph):
        if glyph not in cls.glyphs:
            return (0, 0) + (cls.advance, cls.glyph_size[1])

        gy, gx = divmod(cls.glyphs.index(glyph), 32)

        return (gx * cls.glyph_size[0], gy * cls.glyph_size[1], cls.advance, cls.glyph_size[1])

    @classmethod
    def render(cls, surface, text, position):
        x, y = position
        for ch in text:
            rct = cls.get_texglyph(ch)
            surface.blit(cls.image, (x, y), rct)
            x += cls.advance


class TextBox(StrList):

    """Represents a visual controls for text editing."""

    def __init__(self, position, page_size=(80, 20)):
        super(TextBox, self).__init__(
            Caret()
        )
        self._position = position
        self.caret.page_size = page_size

    @property
    def position(self):
        return self._position[:]

    @position.setter
    def position(self, value):
        self.position = value[0], value[1]

    def render(self, surface, backcolor=(0, 0, 0)):

        left = self.position[0] -1
        top = self.position[1] - 1
        width = (self.caret.page_size[0] * BmpFont.advance) + 2
        height = (self.caret.page_size[1] * BmpFont.glyph_size[1]) + 2

        pts = [(left, top), (left + width, top), (left + width, top + height), (left, top + height)]
        pygame.draw.polygon(surface, backcolor, pts)

        firstline = self.caret.page_pos[1]
        lastline = min(len(self), firstline + self.caret.page_size[1])
        firstcolumn = self.caret.page_pos[0]

        x, y = self.position
        caretline = y + ((self.caret.line - firstline) * BmpFont.glyph_size[1])
        caretcolumn = x + ((self.caret.column - firstcolumn) * BmpFont.advance)

        for index, line in enumerate(self[firstline: lastline + 1]):
            lastcolumn = min(len(line), firstcolumn + self.caret.page_size[0])
            BmpFont.render(surface, line[firstcolumn: lastcolumn], (x, y))
            y += BmpFont.glyph_size[1]

        pygame.draw.line(
            surface,
            (255, 0, 0),
            (caretcolumn, caretline),
            (caretcolumn, caretline + BmpFont.glyph_size[1]),
            2
        )
        pygame.draw.polygon(surface, (255, 255, 255), pts, 1)


def program():

    pygame.init()

    surface = pygame.display.set_mode([800, 400])
    forecolor = (0, 0, 0)
    backcolor = (255, 255, 255)

    BmpFont.set_colors(forecolor, backcolor)


    pygame.key.set_repeat(250, 50)

    clock = pygame.time.Clock()
    textbox = TextBox((50, 50), (40, 10))
    textbox.lines = [
        u"THIS EXAMPLE DEMONSTRATES THE USE OF THE StrList CLASS.",
        u"",
        u"In this example, basic text navigation is supported.",
        u"Also, is uses the 'page_size' attribute of the Caret",
        u"class to acomodate the text properly.",
        u"In this example, the following commands are supported:",
        u"[UP], [DOWN], [LEFT], [RIGHT] keys to move the caret",
        u"a single character or line.",
        u"[HOME], [END] keys to move the caret to the beginning or",
        u"or the end of the current line."
    ]

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == c.QUIT:
                done = True

            elif event.type == c.KEYDOWN:
                if event.key == c.K_UP:
                    textbox.mov_operation(Caret.MOVPREVLINE)
                elif event.key == c.K_DOWN:
                    textbox.mov_operation(Caret.MOVNEXTLINE)
                elif event.key == c.K_RIGHT:
                    textbox.mov_operation(Caret.MOVNEXTCHAR)
                elif event.key == c.K_LEFT:
                    textbox.mov_operation(Caret.MOVPREVCHAR)
                elif event.key == c.K_HOME:
                    textbox.mov_operation(Caret.MOVLINEHOME)
                elif event.key == c.K_END:
                    textbox.mov_operation(Caret.MOVLINEEND)

        clock.tick(30)
        surface.fill((192, 192, 192))

        BmpFont.set_colors((0, 0, 0), (192, 192, 192))
        BmpFont.render(surface, u"Use the arrow keys to navigate in the text.", (5, 5))

        BmpFont.set_colors(forecolor, backcolor)
        textbox.render(surface, backcolor)

        pygame.display.flip()

if __name__ == '__main__':
    program()