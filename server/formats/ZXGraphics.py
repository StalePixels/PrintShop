#!/usr/bin/env python

from PIL import Image
from array import array

class ZXScreen:
    WIDTH = 256
    HEIGHT = 192

    def __init__(self):
        self.bitmap = array('B')
        self.attributes = array('B')

    # This could be useful on the PI accelerator?
    def load(self, filename):
        with open(filename, 'rb') as f:
            self.bitmap.fromfile(f, 6144)
            self.attributes.fromfile(f, 768)

    def store(self, s):
        self.bitmap.fromstring(s[:6144])
        self.attributes.fromstring(s[6144:])

    def process(self, mono=False):
        if mono:
            return self._mono()
        else:
            return self._colour()

    def _get_pixel_address(self, x, y):
        y76 = y & 0b11000000 # third of screen
        y53 = y & 0b00111000
        y20 = y & 0b00000111
        address = (y76 << 5) + (y20 << 8) + (y53 << 2) + (x >> 3)
        return address

    def _get_attribute_address(self, x, y):
        y73 = y & 0b11111000
        address = (y73 << 2) + (x >> 3)
        return address

    def _get_byte(self, x, y):
        return self.bitmap[ self._get_pixel_address(x,y) ]

    #'Private' method
    def __get_attribute(self, x, y):
        return self.attributes[ self._get_attribute_address(x,y) ]


    def _colour(self):
        img = Image.new('RGB', (ZXScreen.WIDTH, ZXScreen.HEIGHT), 'white')
        pixels = img.load()
        for y in xrange(ZXScreen.HEIGHT):
            for col in xrange(ZXScreen.WIDTH >> 3):
                x = col << 3
                byte = self._get_byte(x, y)
                attr = self.__get_attribute(x, y)
                ink = attr & 0b0111
                paper = (attr >> 3) & 0b0111
                bright = (attr >> 6) & 1
                val = 0xcd if not bright else 0xff
                for bit in xrange(8):
                    bit_is_set = (byte >> (7 - bit)) & 1
                    color = ink if bit_is_set else paper
                    rgb = tuple(val * (color >> i & 1) for i in (1,2,0))
                    pixels[x + bit, y] = rgb
        return img

    def _mono(self):
        img = Image.new('RGB', (ZXScreen.WIDTH, ZXScreen.HEIGHT), 'white')
        pixels = img.load()
        for y in xrange(ZXScreen.HEIGHT):
            for col in xrange(ZXScreen.WIDTH >> 3):
                x = col << 3
                byte = self.get_byte(x, y)
                for bit in xrange(8):
                    bit_is_set = (byte >> (7 - bit)) & 1
                    pixels[x + bit, y] = tuple([255,255,255]) if bit_is_set else 0
        return img.convert("1")

class ZXImage:
    WIDTH = 256
    HEIGHT = 192

    def __init__(self):
        self.hasPalette = False
        self.palette = array('B')
        self.bitmap = array('B')

    # This could be useful on the PI accelerator?
    def load(self, filename):
        print("TODO")
        # with open(filename, 'rb') as f:
        #     self.bitmap.fromfile(f, 6144)
        #     self.attributes.fromfile(f, 768)

    def store(self, s):
        if s.__len__()==49152:
            self.bitmap.fromstring(s)
        else:
            self.hasPalette = True
            self.palette.fromstring(s[:512])
            self.bitmap.fromstring(s[49152:])

    def process(self, mono=False):
        if mono:
            return self._mono()
        else:
            return self._colour()

    def _get_pixel_address(self, x, y):
        address = (y * 256) + x
        return address

    def _get_byte(self, x, y):
        return self.bitmap[ self._get_pixel_address(x,y) ]

    def _mono(self):
        print("TODO - impliment dither options")
        # img = Image.new('RGB', (ZXScreen.WIDTH, ZXScreen.HEIGHT), 'white')
        # pixels = img.load()
        # for y in xrange(ZXScreen.HEIGHT):
        #     for col in xrange(ZXScreen.WIDTH >> 3):
        #         x = col << 3
        #         byte = self.get_byte(x, y)
        #         attr = self.get_attribute(x, y)
        #         ink = attr & 0b0111
        #         paper = (attr >> 3) & 0b0111
        #         bright = (attr >> 6) & 1
        #         val = 0xcd if not bright else 0xff
        #         color = ink if bit_is_set else paper
        #         rgb = tuple(val * (color >> i & 1) for i in (1,2,0))
        #         pixels[x, y] = rgb
        return self._colour().convert("1")

    def _colour(self):
        img = Image.new('RGB', (ZXScreen.WIDTH, ZXScreen.HEIGHT), 'white')
        pixels = img.load()
        for y in xrange(ZXScreen.HEIGHT):
            for x in xrange(ZXScreen.WIDTH):
                byte = self._get_byte(x, y)
                r = (byte & 224)
                g = (byte & 28) << 3
                b = (byte & 3) << 6
                if r>0:
                    r = r + 31
                if g>0:
                    g = g + 31
                if b>0:
                    b = b + 63
                col = tuple([r, g, b])
                pixels[x, y] = col
        return img

if __name__ == '__main__':
    pass