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
import platform
import sys
import time
import usb.core
import usb.util

from escpos.printer import Usb as Escpos

from formats.ZXGraphics import ZXScreen, ZXImage
from includes.DummyPrinter import DummyPrinter

class ESCpos(DummyPrinter):
    MAX_PRINTER_DOTS_PER_LINE = 256

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

        tmp = int(round(time.time() * 1000)).__str__()

        img.save(tmp+".png")

        Epson = Escpos(0x0416, 0x5011)
        Epson.image(tmp+".png", True, True, u'bitImageColumn')


    def _setup_usb(self):
        """Connects to the 1st pritner matching the device ID the USB bus"""
        # Find the given Vendor ID and Product ID (also known as vid
        # and pid)
        self._dev = usb.core.find(custom_match=printer_finder())
        if self._dev is None:  # if no such device is connected...
            raise IOError('Printer not found')  # ...report error

        try:
            self._dev.reset()

            # Initialisation. Passing no arguments sets the configuration to the
            # currently active configuration.
            self._dev.set_configuration()
        except usb.core.USBError as err:
            raise IOError('Failed to configure the printer', err)

        # Get a handle to the active interface
        cfg = self._dev.get_active_configuration()

        interface_number = cfg[(0, 0)].bInterfaceNumber
        usb.util.claim_interface(self._dev, interface_number)
        alternate_setting = usb.control.get_interface(self._dev, interface_number)

        intf = usb.util.find_descriptor(
            cfg, bInterfaceNumber=interface_number,
            bAlternateSetting=alternate_setting)

        ep_out = usb.util.find_descriptor(
            intf,
            custom_match=lambda e:
            usb.util.endpoint_direction(e.bEndpointAddress) ==
            usb.util.ENDPOINT_OUT
        )

        # get an endpoint instance
        cfg = self._dev.get_active_configuration()
        intf = cfg[(0, 0)]

        ep = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match= \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT)


        if ep_out is None:  # check we have a real endpoint handle
            raise IOError('Could not find an endpoint to print to')

        return ep_out, dev

# Ensure that BasicPrint is ran in a stand-alone fashion (as intended) and not
# imported as a module. Prevents accidental execution of code.
if __name__ == '__main__':
    main()

