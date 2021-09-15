from util import *
from emulator import Emulator
from PIL import Image
import os
import shutil


class Binjgb(Emulator):
    def __init__(self):
        super().__init__("binjgb", "https://github.com/binji/binjgb/releases", startup_time=1.0)
    
    def setup(self):
        downloadGithubRelease("binji/binjgb", "downloads/binjgb.tar.gz")
        extract("downloads/binjgb.tar.gz", "emu/binjgb")
        setDPIScaling("emu/binjgb/binjgb-v0.1.10/bin/binjgb.exe")

    def startProcess(self, rom, *, gbc=False):
        if not gbc:
            return subprocess.Popen(["emu/binjgb/binjgb-v0.1.10/bin/binjgb.exe", "--force-dmg", os.path.abspath(rom)], cwd="emu/binjgb")
        return subprocess.Popen(["emu/binjgb/binjgb-v0.1.10/bin/binjgb.exe", os.path.abspath(rom)], cwd="emu/binjgb")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        print(screenshot)
        if screenshot is None:
            return None
        return screenshot.resize((160, 144), Image.NEAREST)
