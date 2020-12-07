from util import *
from emulator import Emulator
import shutil
import winreg


class GambatteSpeedrun(Emulator):
    def __init__(self):
        super().__init__("GambatteSpeedrun", startup_time=4.5)

        self.title_check = lambda title: "Gambatte-Speedrun" in title

    def setup(self):
        downloadGithubRelease("pokemon-speedrunning/gambatte-speedrun", "downloads/gambatte-speedrun.zip", filter=lambda n: "theothers" in n and n.endswith(".zip"))
        extract("downloads/gambatte-speedrun.zip", "emu/gambatte-speedrun")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_bios.bin", "emu/gambatte-speedrun/cgb_bios.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/gambatte-speedrun/dmg_boot.bin")
        setDPIScaling("emu/gambatte-speedrun/gambatte_speedrun.exe")

        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\gambatte\gambatte_qt")
        winreg.SetValueEx(key, "biosFilename", 0, 1, os.path.abspath("emu/gambatte-speedrun/cgb_bios.bin"))
        winreg.SetValueEx(key, "biosFilenameDMG", 0, 1, os.path.abspath("emu/gambatte-speedrun/dmg_boot.bin"))
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\gambatte\gambatte_qt\video")
        winreg.SetValueEx(key, "windowSize", 0, 1, "@Size(160 144)")
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\gambatte\gambatte_qt\sound")
        winreg.SetValueEx(key, "engineIndex", 0, 1, "Null")

    def startProcess(self, rom, *, gbc=False):
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\gambatte\gambatte_qt")
        winreg.SetValueEx(key, "platform", 0, winreg.REG_DWORD, 1 if gbc else 0)
        self.startup_time = 4.0 if gbc else 6.0
        return subprocess.Popen(["emu/gambatte-speedrun/gambatte_speedrun.exe", os.path.abspath(rom)], cwd="emu/gambatte-speedrun")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        return screenshot.crop((0, screenshot.size[1] - 144, 160, screenshot.size[1]))
