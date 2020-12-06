from util import *
from emulator import Emulator


class MGBA(Emulator):
    def __init__(self):
        super().__init__("mGBA", startup_time=2.5)
        self.speed = 1.0

    def setup(self):
        download("https://github.com/mgba-emu/mgba/releases/download/0.8.4/mGBA-0.8.4-win32.7z", "downloads/mgba.7z")
        extract("downloads/mgba.7z", "emu/mgba")
        setDPIScaling("emu/mgba/mGBA-0.8.4-win32/mgba-sdl.exe")
    
    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/mgba/mGBA-0.8.4-win32/mgba-sdl.exe", "-1", os.path.abspath(rom)], cwd="emu/mgba/mGBA-0.8.4-win32/")
