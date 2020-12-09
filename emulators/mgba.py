from util import *
from emulator import Emulator
import shutil
import os


class MGBA(Emulator):
    def __init__(self):
        super().__init__("mGBA", startup_time=2.5)
        self.speed = 1.0

    def setup(self):
        # downloadGithubRelease("mgba-emu/mgba", "downloads/mgba.7z", filter=lambda n: "win32" in n and n.endswith(".7z"))
        download("https://s3.amazonaws.com/mgba/mGBA-build-latest-win64.7z", "downloads/mgba.7z")
        extract("downloads/mgba.7z", "emu/mgba")
        self.path = os.path.join("emu", "mgba", os.listdir("emu/mgba")[0])
        setDPIScaling("%s/mGBA.exe" % (self.path))
        setDPIScaling("%s/mgba-sdl.exe" % (self.path))
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "mgba.qt.ini"), "%s/qt.ini" % (self.path))
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "mgba.config.ini"), "%s/config.ini" % (self.path))
    
    def startProcess(self, rom, *, gbc=False):
        #return subprocess.Popen(["%s/mGBA.exe" % (self.path), os.path.abspath(rom)], cwd=self.path)
        return subprocess.Popen(["%s/mgba-sdl.exe" % (self.path), os.path.abspath(rom)], cwd=self.path)

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        return screenshot.crop((0, screenshot.size[1] - 144, 160, screenshot.size[1]))
