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

    def __init__(self, logger):
        DummyPrinter.__init__(self,logger)
        # If you had some network, or physical connection to set up this would be the place to do it and
        # bail if the printer can't be found, etc...
        #
        # We have none of that, making this proc pointless, since the super does all our work, but I've left
        # it in so there's somewhere to put this comment ;-)
        #                                                                       -Xalior

    def print(self, input_buffer, opts):
        printjob = DummyPrinter.print(self, input_buffer, opts)
        # If we want to do any further manipulation of the "printjob" now is the time
        # You can inspect opts.mode if you want to see what kind of payload this is...
        if opts.mode == PRINT_MODE_TXT:
            self._print_text(printjob, opts)
        else:
            self._print_image(printjob, opts)

    def _text(self, text, opts):
        """
        Write the text, in text, to an img to disk?

        Naaaa, son. Not on this day...
        """
        print("text: "+text)
        raise Exception

    def _print_image(self, img, opts):
        """
        Write the PILlow Image (img) to disk - filename is based on time based on "PrintShop-YYYYMMDDhhmmss.png"
        in the working dir (the dir you were in when you launched print-shop.py) by default
        """
        img.save("PrintShop-"+datetime.now().strftime("%Y%m%d%H%M%S")+".png")

# Trap running this by itself
if __name__ == '__main__':
    raise SystemExit

