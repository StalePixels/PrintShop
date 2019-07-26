#!/usr/bin/env python
#
# ImageWriter.py
#
from __future__ import print_function
from datetime import datetime

from includes.Options import *
from includes.DummyPrinter import DummyPrinter

'''
ImageWriter driver is provided as-is, and is for demonstration
purposes only, a fake printer that writes input to disk. 

Stale Pixels, or Xalior takes no responsibility for any critical
system implementations based on this code.

Copyright (c) 2019 Stale Pixels.         Some rights reserved.
'''

class ImageWriter(DummyPrinter):
    MAX_PRINTER_DOTS_PER_LINE = 1024
    TYPE = "ImageWriter"

    def print(self, input_buffer, opts):
        img = DummyPrinter.print(self, input_buffer, opts)
        self._print_image(img, opts)

    def _text(self, text, opts):
        print("text: "+text)

    def _print_image(self, img, opts):
        """Write the PILlow Image (img) to disk."""
        img.save("PrintShop-"+datetime.now().strftime("%Y%m%d%H%M%S")+".png")

# Trap running this by itself
if __name__ == '__main__':
    raise SystemExit

