from util import *
from emulator import Emulator
import shutil
import requests
import re


class Emulicious(Emulator):
    def __init__(self):
        super().__init__("Emulicious", "https://emulicious.net/", startup_time=1.0)
    
    def setup(self):
        res = requests.get("https://emulicious.net/downloads/")
        url = re.search("data-downloadurl=\"([^\"]+)\"", res.text).group(1)
        download(url, "downloads/Emulicious.zip")
        extract("downloads/Emulicious.zip", "emu/emulicious")
        setDPIScaling("emu/emulicious/Emulicious.exe")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin", "emu/emulicious/cgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/emulicious/dmg_boot.bin")

    def startProcess(self, rom, *, gbc=False):
        if gbc:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "emulicious.gbc.ini"), "emu/emulicious/Emulicious.ini")
        else:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "emulicious.dmg.ini"), "emu/emulicious/Emulicious.ini")
        return subprocess.Popen(["java", "-jar", "Emulicious.jar", "-throttle", "10000", os.path.abspath(rom)], cwd="emu/emulicious")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        return screenshot.crop((0, screenshot.size[1] - 144, 160, screenshot.size[1]))
