#
# PrintShopPrint.py
#
# Original Name - BasicPrint.py
# Copyright (c) 2014 Able Systems Limited. All rights reserved.
#
# Modified by Garry Lancaster 2019 to perform as a simple wifi print server
# on port 65432 for the ZX Spectrum Next.
#
# Modified by D. 'Xalior' Rimron-Soutter 2019 to perform as a slightly more
# complex wifi print server, also on port 65432, compatible with Garry's
# version, still for the ZX Spectrum Next.
from __future__ import print_function

HOST = ''
PORT = 65432

'''PrintShopPipsta is provided as-is, and is for demonstration
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



# Ensure that BasicPrint is ran in a stand-alone fashion (as intended) and not
# imported as a module. Prevents accidental execution of code.
if __name__ == '__main__':
    main()

