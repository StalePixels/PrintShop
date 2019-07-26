#!/usr/bin/env python
#
# ESCpos.py
#
from __future__ import print_function

HOST = ''
PORT = 65432

'''ESCpos driver is provided as-is, and is for demonstration
purposes only. Stale Pixels, or Xalior takes no responsibility
for any system implementations based on this code.

Copyright (c) 2019 Stale Pixels.         Some rights reserved.

'''
import time
import sys

from escpos.printer import Usb as Escpos

from includes.DummyPrinter import DummyPrinter

class ESCpos(DummyPrinter):
    MAX_PRINTER_DOTS_PER_LINE = 384

    TYPE = "ESCpos"
    _dev = None

    # USB specific constant definitions
    USB_VENDOR_ID = 0x0416
    USB_DEVICE_ID = 0x5011  # Zjiang POS Thermal Printer Mini 58mm USB - https://www.aliexpress.com/item/1000006163834.html

    def __init__(self, logger):
        DummyPrinter.__init__(self,logger)

    def print(self, input_buffer, opts):
        img = DummyPrinter.print(self, input_buffer, opts)
        self._print_image(img, opts)

    def _print_image(self, img, opts):
        """Take the PILlow image, and convert to ESC format, and print"""

        # I am a mono printer, I INSIST this is a mono image...
        img = img.convert("1")

        tmp = int(round(time.time() * 1000)).__str__()
        img.save(tmp+".png")

        Epson = Escpos(self.USB_VENDOR_ID, self.USB_DEVICE_ID)
        Epson.image(tmp+".png", True, True, u'bitImageColumn')



# Ensure that ESCpos is never ran in a stand-alone fashion (as intended)
# and always imported as a module. Prevents accidental execution of code.
if __name__ == '__main__':
    raise SystemExit

