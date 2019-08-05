#!/usr/bin/env python
#
# ESCpos.py
#
from __future__ import print_function

import time
import os

from escpos.printer import Usb as ESCposUSBInterface

from includes.Options import *
from includes.DummyPrinter import DummyPrinter
'''
ESCpos driver is provided as-is, and is for demonstration
purposes only. Stale Pixels, or Xalior takes no responsibility
for any system implementations based on this code.

Copyright (c) 2019 Stale Pixels.         Some rights reserved.
'''
class ESCpos(DummyPrinter):
    MAX_PRINTER_DOTS_PER_LINE = 384

    TYPE = "ESCpos"
    _dev = None

    # USB specific constant definitions
    USB_VENDOR_ID = 0x0416
    USB_DEVICE_ID = 0x5011  # Zjiang POS Thermal Printer Mini 58mm USB - https://www.aliexpress.com/item/1000006163834.html


    def __init__(self, logger):
        DummyPrinter.__init__(self,logger)
        self.ESCposPrinter = ESCposUSBInterface(self.USB_VENDOR_ID, self.USB_DEVICE_ID)

    def print(self, input_buffer, opts):
        printjob = DummyPrinter.print(self, input_buffer, opts)

        if opts.mode == PRINT_MODE_TXT:
            self._print_text(printjob, opts)
        else:
            self._print_image(printjob, opts)

    def _print_image(self, img, opts):
        """Take the PILlow image, and convert to ESC format, and print"""

        # I am a mono printer, I INSIST this is a mono image...
        img = img.convert("1")

        tmpfile = opts.args.temppath + os.path.sep + int(round(time.time() * 1000)).__str__() + ".png"
        img.save(tmpfile)

        self.ESCposPrinter.image(tmpfile, True, True, u'bitImageColumn')

        os.remove(tmpfile)



# Ensure that ESCpos is never ran in a stand-alone fashion (as intended)
# and always imported as a module. Prevents accidental execution of code.
if __name__ == '__main__':
    raise SystemExit

