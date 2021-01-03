from util import *
from emulator import Emulator
import shutil
import os
import PIL.Image
import PIL.ImageOps


class Higan(Emulator):
    def __init__(self):
        super().__init__("Higan", "https://byuu.org/higan/", startup_time=5.0)
        self.title_check = lambda title: "byuu-rom" in title
        self.gbc = False

    def setup(self):
        downloadGithubRelease("higan-emu/higan", "downloads/higan.zip", filter=lambda n: "byuu" in n and "windows" in n and n.endswith(".zip"), allow_prerelease=True)
        extract("downloads/higan.zip", "emu/higan")
        setDPIScaling("emu/higan/byuu-nightly/byuu.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "higan-settings.bml"), "emu/higan/byuu-nightly/settings.bml")
    
    def startProcess(self, rom, *, gbc=False):
        target = "emu/higan/byuu-nightly/byuu-rom.gb"
        self.gbc = gbc
        if gbc:
            target += "c"
        shutil.copy(rom, target)
        return subprocess.Popen(["emu/higan/byuu-nightly/byuu.exe", os.path.abspath(target)], cwd="emu/higan/byuu-nightly")

    def getScreenshot(self):
        screenshot = super().getScreenshot()
        if screenshot is None:
            return None
        screenshot = screenshot.reduce(3)
        if not self.gbc:
            screenshot = screenshot.convert(mode="L", dither=PIL.Image.NONE)
            screenshot = PIL.ImageOps.autocontrast(screenshot)
            screenshot.save("tmp.png")
        return screenshot
