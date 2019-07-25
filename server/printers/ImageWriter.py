#!/usr/bin/env python
#
# ImageWriter.py
#
from __future__ import print_function
from formats.ZXGraphics import ZXScreen, ZXImage
from PIL import Image

from libs.Options import *


'''ImageWriter driver is provided as-is, and is for demonstration
purposes only. 

Stale Pixels, or Xalior takes no responsibility for any critical
system implementations based on this code.

Copyright (c) 2019 Stale Pixels.         Some rights reserved.

'''

MAX_PRINTER_DOTS_PER_LINE = 1024

class ImageWriter:
    TYPE = "ImageWriter"

    def __init__(self, logger):
        self.LOGGER = logger

    def print(self, input_buffer, opts):
        if opts.mode == PRINT_MODE_SCR:
            screen = ZXScreen()
            screen.parse(input_buffer)
            if opts.dither == 0:
                img = screen.mono()
            else:
                img = screen.dither()
            print(opts.rotate)
            if opts.rotate == 1:
                print("ROTATED IT")
                img = img.rotate(90, 0, 1)

            # From http://stackoverflow.com/questions/273946/
            # /how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
            wpercent = (MAX_PRINTER_DOTS_PER_LINE / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((MAX_PRINTER_DOTS_PER_LINE, hsize), Image.NONE)
            #
            # print_data = convert_image(img)
            # usb_out.write(SET_LED_MODE + b'\x00')
            # print_image(device, usb_out, print_data)
            # usb_out.write(FEED_PAST_CUTTER)
            # # Ensure the LED is not in test mode
            # usb_out.write(SET_LED_MODE + b'\x00')

            img.save("demo.png")

            # Epson = Escpos(0x0416, 0x5011)
            # Epson.image("demo.png", True, True, u'bitImageColumn')

        elif opts.mode == PRINT_MODE_NXI:
            screen = ZXImage()
            screen.parse(input_buffer)
            if opts.dither == 0:
                img = screen.mono()
            else:
                img = screen.dither()
            print(opts.rotate)
            if opts.rotate == 1:
                print("ROTATED IT")
                img = img.rotate(90, 0, 1)

            # From http://stackoverflow.com/questions/273946/
            # /how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
            wpercent = (MAX_PRINTER_DOTS_PER_LINE / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((MAX_PRINTER_DOTS_PER_LINE, hsize), Image.NONE)
            #
            # print_data = convert_image(img)
            # usb_out.write(SET_LED_MODE + b'\x00')
            # print_image(device, usb_out, print_data)
            # usb_out.write(FEED_PAST_CUTTER)
            # # Ensure the LED is not in test mode
            # usb_out.write(SET_LED_MODE + b'\x00')

            img.save("demo.png")

            # Epson = Escpos(0x0416, 0x5011)
            # Epson.image("demo.png", True, True, u'bitImageColumn')

    def _text(self, text, opts):
        print("text: "+text)

    def _image(self, img, opts):
        """Write the PILlow Image (img) to disk."""
        img.save("demo.png")

# Trap running this by itself
if __name__ == '__main__':
    print("Nope")

