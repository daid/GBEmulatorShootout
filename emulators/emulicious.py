from util import *
from emulator import Emulator
import shutil


class Emulicious(Emulator):
    def __init__(self):
        super().__init__("Emulicious", startup_time=1.0)
    
    def setup(self):
        download("https://emulicious.net/Emulicious.zip", "downloads/Emulicious.zip")
        extract("downloads/Emulicious.zip", "emu/emulicious")
        setDPIScaling("emu/emulicious/Emulicious.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "emulicious.ini"), "emu/emulicious/Emulicious.ini")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_bios.bin", "emu/emulicious/cgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/emulicious/dmg_boot.bin")

    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["java", "-jar", "Emulicious.jar", "-throttle", "10000", os.path.abspath(rom)], cwd="emu/emulicious")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        return screenshot.crop((0, screenshot.size[1] - 144, 160, screenshot.size[1]))
