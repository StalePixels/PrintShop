#!/usr/bin/env python
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

Copyright (c) 2014 Able Systems Limited. All rights reserved.
Copyright (c) 2019 Stale Pixels.         Some rights reserved.

'''
import argparse
import logging
import platform
import struct
import sys
import time
from PIL import Image

import usb.core
import usb.util

import socket

from formats.ZXGraphics import ZXScreen, ZXImage
from includes.DummyPrinter import DummyPrinter

from array import array
from bitarray import bitarray

'''
Pipsta driver is provided as-is, and is for demonstration
purposes only. Stale Pixels, or Xalior takes no responsibility
for any system implementations based on this code.

Copyright (c) 2019 Stale Pixels.         Some rights reserved.
'''
# USB specific constant definitions
USB_VENDOR_ID = 0x0483
PIPSTA_USB_PRODUCT_ID = 0xA19D
AP1400_USB_PRODUCT_ID = 0xA053
AP1400V_USB_PRODUCT_ID = 0xA19C

USB_PRODUCT_IDS = {PIPSTA_USB_PRODUCT_ID, AP1400_USB_PRODUCT_ID, AP1400V_USB_PRODUCT_ID}

# Pipsta specific printer commands, defined here for ease of use
PIPSTA_SET_FONT_MODE_3 = b'\x1b!\x03'
PIPSTA_SET_LED_MODE = b'\x1bX\x2d'
PIPSTA_FEED_PAST_CUTTER = b'\n' * 5
PIPSTA_SELECT_SDL_GRAPHICS = b'\x1b*\x08'
PIPSTA_USB_BUSY = 66

class printer_finder(object):
    def __call__(self, device):
        if device.idVendor != USB_VENDOR_ID:
            return False

        return True if device.idProduct in USB_PRODUCT_IDS else False

class Pipsta(DummyPrinter):
    MAX_PRINTER_DOTS_PER_LINE = 384

    TYPE = "Pipsta"

    def __init__(self, logger):
        DummyPrinter.__init__(self,logger)

        # Find the Pipsta's specific Vendor ID and Product ID (also known as vid
        # and pid)
        dev = usb.core.find(custom_match=printer_finder())
        if dev is None:  # if no such device is connected...
            raise IOError('Printer not found')  # ...report error

        try:
            dev.reset()
            dev.set_configuration()
        except usb.core.USBError as err:
            raise IOError('Failed to configure the printer', err)

        # Get a handle to the active interface
        cfg = dev.get_active_configuration()

        interface_number = cfg[(0, 0)].bInterfaceNumber
        usb.util.claim_interface(dev, interface_number)
        alternate_setting = usb.control.get_interface(dev, interface_number)
        intf = usb.util.find_descriptor(
            cfg, bInterfaceNumber=interface_number,
            bAlternateSetting=alternate_setting)

        self._ep_out = usb.util.find_descriptor(
            intf,
            custom_match=lambda e:
            usb.util.endpoint_direction(e.bEndpointAddress) ==
            usb.util.ENDPOINT_OUT
        )

        if self._ep_out is None:  # check we have a real endpoint handle
            raise IOError('Could not find an endpoint to print to')

    def print(self, input_buffer, opts):
        img = DummyPrinter.print(self, input_buffer, opts)
        self._print_image(img, opts)

    def _print_image(self, img, opts):
        """
        Reads the img and sends it a dot line at once to the printer
        """
        data = bitarray(img.getdata(), endian='big')
        data.invert()
        data.tobytes()

        self._ep_out.write(PIPSTA_SET_FONT_MODE_3)
        cmd = struct.pack('3s2B', PIPSTA_SELECT_SDL_GRAPHICS,
                          (self.MAX_PRINTER_DOTS_PER_LINE / 8) & 0xFF,
                          (self.MAX_PRINTER_DOTS_PER_LINE / 8) / 256)
        lines = len(data) // (self.MAX_PRINTER_DOTS_PER_LINE / 8)
        for line in range(0, lines):
            start = line * (self.MAX_PRINTER_DOTS_PER_LINE / 8)
            # intentionally +1 for slice operation below
            end = start + (self.MAX_PRINTER_DOTS_PER_LINE / 8)
            # ...to end (end not included)
            self._ep_out.write(b''.join([cmd, data[start:end]]))


# Ensure that Pipsta is never ran in a stand-alone fashion (as intended)
# and always imported as a module. Prevents accidental execution of code.
if __name__ == '__main__':
    raise SystemExit

