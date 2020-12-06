from util import *
from emulator import Emulator
import shutil
import winreg


class GambatteSpeedrun(Emulator):
    def __init__(self):
        super().__init__("GambatteSpeedrun", startup_time=4.5)

        self.title_check = lambda title: "Gambatte-Speedrun" in title

    def setup(self):
        download("https://github.com/pokemon-speedrunning/gambatte-speedrun/releases/download/r717/gambatte-speedrun-r717-psr.zip", "downloads/gambatte-speedrun.zip")
        extract("downloads/gambatte-speedrun.zip", "emu/gambatte-speedrun")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_bios.bin", "emu/gambatte-speedrun/cgb_bios.bin")
        setDPIScaling("emu/gambatte-speedrun/gambatte_speedrun.exe")

        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\gambatte\gambatte_qt")
        winreg.SetValueEx(key, "biosFilename", 0, 1, os.path.abspath("emu/gambatte-speedrun/cgb_bios.bin"))
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\gambatte\gambatte_qt\video")
        winreg.SetValueEx(key, "windowSize", 0, 1, "@Size(160 144)")

    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/gambatte-speedrun/gambatte_speedrun.exe", os.path.abspath(rom)], cwd="emu/gambatte-speedrun")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        return screenshot.crop((0, screenshot.size[1] - 144, 160, screenshot.size[1]))
