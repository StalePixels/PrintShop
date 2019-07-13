#!/usr/bin/env python
#
# ImageWriter.py
#
from __future__ import print_function

HOST = ''
PORT = 65432

'''ImageWriter driver is provided as-is, and is for demonstration
purposes only. 

Stale Pixels, or Xalior takes no responsibility for any critical
system implementations based on this code.

Copyright (c) 2019 Stale Pixels.         Some rights reserved.

'''
class ImageWriter:
    TYPE = "ImageWriter"

    def __init__(self, logger):
        self.LOGGER = logger

    def text(self, text):
        print(text)

    def image(self, img):
        """Write the PILlow Image (img) to disk."""
        img.save("demo.png")

# Trap running this by itself
if __name__ == '__main__':
    print("Nope")

