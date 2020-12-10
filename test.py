import PIL.Image
import os

from util import *


class Test:
    def __init__(self, name, *, runtime, rom=None, result=None, gbc=False):
        rom = rom or name
        self.name = name
        self.rom = os.path.join("tests", rom)
        assert os.path.exists(self.rom)
        self.runtime = runtime
        if result is None:
            result = os.path.splitext(rom)[0] + ".png"
        self.result = os.path.join("tests", result)
        self.gbc = gbc

    def checkResult(self, screenshot):
        if not os.path.exists(self.result):
            return None
        reference = PIL.Image.open(self.result)
        return compareImage(screenshot, reference)

    def __repr__(self):
        return self.name
