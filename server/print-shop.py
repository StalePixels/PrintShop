#!/usr/bin/env python
#
# print-shop.py
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

'''PrintShop is provided as-is, and is for demonstration
purposes only. Stale Pixels, or Xalior takes no responsibility
for any system implementations based on this code.

Copyright (c) 2019 Stale Pixels.         Some rights reserved.

'''
import argparse
import logging
import platform
import sys
import time
from PIL import Image

import socket

from libs.Options import *

Printer = None

#Our printers
from printers.ImageWriter import ImageWriter as ImageWriter
from printers.ESCpos import ESCpos as ESCpos
from printers.Pipsta import Pipsta as Pipsta

#Our formats

from formats.ZXGraphics import ZXScreen, ZXImage
from array import array
from bitarray import bitarray

LOGGER = logging.getLogger('PrintShop')

def setup_logging(opts):
    '''Sets up logging for the application.'''

    LOGGER.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    LOGGER.addHandler(stream_handler)

    if opts.logfile:
        file_handler = logging.FileHandler(opts.logfile)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s',
                                                    datefmt='%d/%m/%Y %H:%M:%S'))
        LOGGER.addHandler(file_handler)


def convert_image(image):
    """Takes the bitmap and converts it to PIPSTA 24-bit image format"""
    imagebits = bitarray(image.getdata(), endian='big')
    imagebits.invert()
    return imagebits.tobytes()

def parse_arguments():
    """Parse the arguments passed to the script, logging, fonts, printer type, etc..."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--font', '-f', type=str, dest='font',
                        help='Optional 1bit-mapped font (not yet used)',
                        nargs='?')
    parser.add_argument('--printer', '-p', type=str, default='ImageWriter', dest='printer',
                        help='Type of printer, default is the ImageWriter',
                        choices=['ImageWriter', 'ESCpos', 'Pipsta'],
                        nargs='?')
    parser.add_argument('--printer-width', '-p-w', type=int, default=None, dest='printer_width',
                        help='Change default output width of printer (not supported by all printers)',
                        nargs='?')
    parser.add_argument('--printer-height', '-p-h', type=int, default=None, dest='printer_height',
                        help='Change default output height of printer (not supported by all printers)',
                        nargs='?')
    parser.add_argument('--log', '-l', type=str, default='ERROR', dest='loglevel',
                        help='LogLevel (Default is ERROR)',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        nargs='?')
    parser.add_argument('--logfile', '-lf', type=str, default=None, dest='logfile',
                        help='Optional file name to write logs to',
                        nargs='?')
    args = parser.parse_args()

    return args

def main():
    """The main loop of the application.  Wrapping the code in a function
    may be useful if we ever want to librarise, and import the file elsewhere later."""

    # We support Python2, because that's most likely to be on the pi...
    if sys.version_info[0] != 2:
        sys.exit('This application requires python 2.')

    if platform.system() != 'Linux':
        sys.exit('This script has only been written for Linux')

    opts = Options(parse_arguments())
    setup_logging(opts)

    if opts.printer == 'ImageWriter':
        Printer = ImageWriter(LOGGER)
        pass
    elif opts.printer == 'Pipsta':
        Printer = Pipsta(LOGGER)
        pass
    elif opts.printer == 'ESCpos':
        Printer = ESCpos(LOGGER)
        pass

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))

    try:
        while True:
            s.listen(0)
            print('Listening with timeout: '+ s.gettimeout().__str__())
            conn, addr = s.accept()
            print('Connected by', addr)

            job_options = PrintJobOptions(opts)

            # Wipe the input buffer fresh...
            input_buffer = array('B')
            while True:
                data = conn.recv(65536)
                if not data:
                    break

                for byte in data:
                    done = False
                    if mode is PRINT_MODE_CMD:                  # We're currently processing commands
                        if byte == chr(13):                              # Finish processing command
                            print("RECV: EoCOMMAND ("+job_options.cmd+")")

                            if job_options.cmd == '.SCR':
                                job_options.mode = PRINT_MODE_SCR                   # Engage SCR Printer
                                print(' CMD! Enable SCR Mode')
                                job_options.done = True
                            elif job_options.cmd == '.NXI':
                                job_options.mode = PRINT_MODE_NXI                   # Engage SCR Printer
                                print(' CMD! Enable NXI Mode')
                                job_options.done = True
                            elif job_options.cmd.startswith("SET"):
                                if "dither" in cmd:
                                    print(' CMD! Enable DITHERing')
                                    job_options.dither = 1
                                    job_options.mode = PRINT_MODE_NEW
                                elif "rotate" in cmd:
                                    print(' CMD! Enable ROTATE')
                                    job_options.job_options.rotate = 1
                                    job_options.mode = PRINT_MODE_NEW
                            else:
                                job_options.mode = PRINT_MODE_NEW                   # Wait for Next Instruction

                            job_options.cmd = ""
                        else:
                            job_options.cmd = job_options.cmd + byte

                    elif not mode:                              # First Packet -- decide how to proceed
                        if byte == chr(0):
                            print(' CMD! Enable Command Mode')
                            job_options.mode = PRINT_MODE_CMD               # Command Mode
                        else:
                            print('RECV: Detected Plain Text File')
                            job_options.mode = PRINT_MODE_TXT               # Classic Printer Mode

                    if not job_options.done:
                        if job_options.mode == PRINT_MODE_TXT:                          # Classic Textmode Printer
                            # Print a char at a time and check the printers buffer isn't full
                            usb_out.write(byte)    # write all the data to the USB OUT endpoint
                            #
                            res = device.ctrl_transfer(0xC0, 0x0E, 0x020E, 0, 2)
                            while res[0] == USB_BUSY:
                               time.sleep(0.01)
                               res = device.ctrl_transfer(0xC0, 0x0E, 0x020E, 0, 2)
                        elif mode == PRINT_MODE_SCR \
                            or mode == PRINT_MODE_NXI:                      # .FILE appendnd to buffer
                            input_buffer.append(ord(byte))
                    job_options.size = job_options.size + 1

            print("DIAG: Total Size "+size.__str__()+"bytes, input_buffer "+input_buffer.__len__().__str__())

            if mode == PRINT_MODE_SCR:
                screen = ZXScreen()
                screen.parse(input_buffer)
                if dither == 0:
                    img = screen.mono()
                else:
                    img = screen.dither()
                print(rotate)
                if rotate == 1:
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

                Epson = Escpos(0x0416, 0x5011)
                Epson.image("demo.png", True, True, u'bitImageColumn')

            elif mode == PRINT_MODE_NXI:
                screen = ZXImage()
                screen.parse(input_buffer)
                if dither == 0:
                    img = screen.mono()
                else:
                    img = screen.dither()
                print(rotate)
                if rotate == 1:
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

                Epson = Escpos(0x0416, 0x5011)
                Epson.image("demo.png", True, True, u'bitImageColumn')

    finally:
        #device.reset()
        pass

# Ensure that BasicPrint is ran in a stand-alone fashion (as intended) and not
# imported as a module. Prevents accidental execution of code.
if __name__ == '__main__':
    main()

