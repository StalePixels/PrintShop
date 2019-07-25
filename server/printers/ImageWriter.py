#!/usr/bin/env python
#
# ImageWriter.py
#
from __future__ import print_function
from formats.ZXGraphics import ZXScreen, ZXImage
from PIL import Image
from datetime import datetime

from datetime import datetime

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
            processor = ZXScreen()

        elif opts.mode == PRINT_MODE_NXI:
            processor = ZXImage()

        processor.store(input_buffer)

        processor.dither = opts.dither

        img = processor.process()

        if opts.rotate:
            img = img.rotate(-90, 0, 1)

        # Resize image, but maintain aspect ratio...

        if opts.rotate:
            wpercent = (MAX_PRINTER_DOTS_PER_LINE / float(processor.HEIGHT))
            hsize = int((float(processor.WIDTH) * float(wpercent)))
        else:
            wpercent = (MAX_PRINTER_DOTS_PER_LINE / float(processor.WIDTH))
            hsize = int((float(processor.HEIGHT) * float(wpercent)))

        img = img.resize((MAX_PRINTER_DOTS_PER_LINE, hsize), Image.NEAREST)

        # Dither after resizing, so we get smaller stipling...
        if opts.dither:
            img = img.convert("1")

        self._save(img, opts)

    def _text(self, text, opts):
        print("text: "+text)

    def _save(self, img, opts):
        """Write the PILlow Image (img) to disk."""
        img.save("PrintShop-"+datetime.now().strftime("%Y%m%d%H%M%S")+".png")

# Trap running this by itself
if __name__ == '__main__':
    print("Nope")

