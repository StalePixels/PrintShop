#!/usr/bin/env python

from PIL import Image
from array import array

class ZXScreen:
    # Original parser from https://gist.github.com/alexanderk23/f459c76847d9412548f7
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

    def parse(self, s):
        self.bitmap.fromstring(s[:6144])
        self.attributes.fromstring(s[6144:])

    def get_pixel_address(self, x, y):
        y76 = y & 0b11000000 # third of screen
        y53 = y & 0b00111000
        y20 = y & 0b00000111
        address = (y76 << 5) + (y20 << 8) + (y53 << 2) + (x >> 3)
        return address

    def get_attribute_address(self, x, y):
        y73 = y & 0b11111000
        address = (y73 << 2) + (x >> 3)
        return address

    def get_byte(self, x, y):
        return self.bitmap[ self.get_pixel_address(x,y) ]

    #'Private' method
    def __get_attribute(self, x, y):
        return self.attributes[ self.get_attribute_address(x,y) ]

    def dither(self):
        img = Image.new('RGB', (ZXScreen.WIDTH, ZXScreen.HEIGHT), 'white')
        pixels = img.load()
        for y in xrange(ZXScreen.HEIGHT):
            for col in xrange(ZXScreen.WIDTH >> 3):
                x = col << 3
                byte = self.get_byte(x, y)
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
        return img.convert("1")

    def mono(self):
        img = Image.new('RGB', (ZXScreen.WIDTH, ZXScreen.HEIGHT), 'white')
        pixels = img.load()
        for y in xrange(ZXScreen.HEIGHT):
            for col in xrange(ZXScreen.WIDTH >> 3):
                x = col << 3
                byte = self.get_byte(x, y)
                attr = self.__get_attribute(x, y)
                for bit in xrange(8):
                    bit_is_set = (byte >> (7 - bit)) & 1
                    pixels[x + bit, y] = tuple([255,255,255]) if bit_is_set else 0
        return img.convert("1")

class ZXImage:
    WIDTH = 256
    HEIGHT = 192

    def __init__(self):
        self.palette = array('B')
        self.bitmap = array('B')

    # This could be useful on the PI accelerator?
    def load(self, filename):
        print("TODO")
        # with open(filename, 'rb') as f:
        #     self.bitmap.fromfile(f, 6144)
        #     self.attributes.fromfile(f, 768)

    def parse(self, s):
        if s.__len__()==49152:
            self.bitmap.fromstring(s)
        else:
            self.palette.fromstring(s[:512])
            self.bitmap.fromstring(s[49152:])

    def get_pixel_address(self, x, y):
        address = (y * 256) + x
        return address

    def get_byte(self, x, y):
        return self.bitmap[ self.get_pixel_address(x,y) ]

    def dither(self):
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
        return img.convert("1")

    def mono(self):
        img = Image.new('RGB', (ZXScreen.WIDTH, ZXScreen.HEIGHT), 'white')
        pixels = img.load()
        for y in xrange(ZXScreen.HEIGHT):
            for x in xrange(ZXScreen.WIDTH):
                byte = self.get_byte(x, y)
                pixels[x, y] = tuple([(byte >> 5) << 5, ((byte>>3) & 7) << 5, (byte & 3) << 5])
        img.save("mono.png")
        return img.convert("1")

if __name__ == '__main__':
    pass