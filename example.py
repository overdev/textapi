# -*- coding: utf-8 -*-

__author__ = 'Jorge A. Gomes'

__all__ = [
    'Textbox',
    'BmpFont'
]

import os
import pygame
from . import *
import pygame.locals as c


class BmpFont(object):

    @staticmethod
    def normalize_color(color):
        """Gets a 3-tuple RGB and return a 0..1 float value"""
        return ((color[2] << 16 | color[1] << 8 | color[0]) & 0xFFFFFF) / 16777215.0

    @staticmethod
    def blend_color(a, b, r):
        """blends color a and b in r ratio."""
        return (
            int(a[0] + (b[0] - a[0]) * r),
            int(a[1] + (b[1] - a[1]) * r),
            int(a[2] + (b[2] - a[2]) * r)
        )

    image = pygame.image.load(os.path.join(os.getcwd(), "res/CBFG_Consolas_24x16_cp1252.png"))
    glyph_size = (24, 16)
    glyphs = u" !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~_¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"
    def_palette = image.get_palette()
    nrm_palette = [0 for i in range(256)]
    advance = 10

    @classmethod
    def initialize(cls):
        cls.image = pygame.image.load(os.path.join(os.getcwd(), "res/CBFG_Consolas_24x16_cp1252.png"))
        cls.glyph_size = (16, 24)
        cls.glyphs = u" !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~_¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"
        cls.def_palette = cls.image.get_palette()
        cls.nrm_palette = [cls.normalize_color(color) for color in cls.def_palette]

    @classmethod
    def set_colors(cls, forecolor, backcolor):
        for index in range(256):
            ratio = cls.nrm_palette[index]
            cls.image.set_palette_at(index, cls.blend_color(backcolor, forecolor, ratio))

    @classmethod
    def get_texglyph(cls, glyph):
        if glyph not in cls.glyphs:
            return (0, 0) + (cls.advance, cls.glyph_size[1])

        gy, gx = divmod(cls.glyphs.find(glyph), cls.glyph_size[0])

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

    def render(self, surface):
        firstline = self.caret.page_pos[1]
        lastline = min(len(self), firstline + self.caret.page_size[1])
        for index, line in enumerate(self[firstline: lastline + 1]):
            firstcolumn = self.caret.page_pos[0]
            lastcolumn = min(len(line), firstcolumn + self.caret.page_size[0])

            text = line[firstcolumn, lastcolumn]