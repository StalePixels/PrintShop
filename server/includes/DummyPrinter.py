#!/usr/bin/env python
#
# ImageWriter.py
#
from __future__ import print_function
from formats.ZXGraphics import ZXScreen, ZXImage
from PIL import Image
from datetime import datetime

from datetime import datetime

from includes.Options import *


'''DummpyPriinter is the base class all other printers can 
 inherit from, and should confirm to.

Stale Pixels, or Xalior takes no responsibility for any critical
system implementations based on this code.

Copyright (c) 2019 Stale Pixels.         Some rights reserved.

'''

class DummyPrinter:
    TYPE = "DummyPrinter"
    processor = None

    def __init__(self, logger):
        self.LOGGER = logger

    def print(self, input_buffer, opts):
        if opts.mode == PRINT_MODE_SCR:
            processor = ZXScreen()

        elif opts.mode == PRINT_MODE_NXI:
            processor = ZXImage()

        # Load the image data into the processor
        processor.store(input_buffer)

        # Activate, get a PIL image instance back
        img = processor.process()

        # Rotate
        if opts.rotate:
            img = img.rotate(-90, 0, 1)

        # Resize image, but maintain aspect ratio...

        # Rotate, keep aspect ratio
        if opts.rotate:
            wpercent = (self.MAX_PRINTER_DOTS_PER_LINE / float(processor.HEIGHT))
            hsize = int((float(processor.WIDTH) * float(wpercent)))
        else:
            wpercent = (self.MAX_PRINTER_DOTS_PER_LINE / float(processor.WIDTH))
            hsize = int((float(processor.HEIGHT) * float(wpercent)))

        # Resize after rotate, maximise resolution
        img = img.resize((self.MAX_PRINTER_DOTS_PER_LINE, hsize), Image.NEAREST)

        # Dither after resizing, so we get smaller stipling...
        if opts.dither:
            img = img.convert("1")

        # Pass image back to real printer instance
        return img

    def _print_text(self, text, opts):
        print("text: "+text)

    def _print_image(self, img, opts):
        """This does nothing in a dummy instance..."""
        raise Exception

# Trap running this by itself
if __name__ == '__main__':
    raise SystemExit

