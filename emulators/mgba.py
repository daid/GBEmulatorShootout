from util import *
from emulator import Emulator
import shutil


class MGBA(Emulator):
    def __init__(self):
        super().__init__("mGBA", startup_time=2.5)
        self.speed = 1.0

    def setup(self):
        downloadGithubRelease("mgba-emu/mgba", "downloads/mgba.7z", filter=lambda n: "win32" in n and n.endswith(".7z"))
        extract("downloads/mgba.7z", "emu/mgba")
        # TODO: Fix path containing version number
        setDPIScaling("emu/mgba/mGBA-0.8.4-win32/mGBA.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "mgba.qt.ini"), "emu/mgba/mGBA-0.8.4-win32/qt.ini")
    
    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/mgba/mGBA-0.8.4-win32/mGBA.exe", "-1", os.path.abspath(rom)], cwd="emu/mgba/mGBA-0.8.4-win32/")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        return screenshot.crop((0, screenshot.size[1] - 144, 160, screenshot.size[1]))
