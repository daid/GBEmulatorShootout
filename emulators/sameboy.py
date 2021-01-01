from util import *
from emulator import Emulator
import os
import shutil


class SameBoy(Emulator):
    def __init__(self):
        super().__init__("SameBoy", "https://sameboy.github.io/", startup_time=4.5)
    
    def setup(self):
        downloadGithubRelease("LIJI32/SameBoy", "downloads/sameboy.zip")
        if extract("downloads/sameboy.zip", "emu/sameboy"):
            os.unlink("emu/sameboy/cgb_boot.bin")
            os.unlink("emu/sameboy/dmg_boot.bin")
            download("https://gbdev.gg8.se/files/roms/bootroms/cgb_bios.bin", "emu/sameboy/cgb_boot.bin")
            download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/sameboy/dmg_boot.bin")
        setDPIScaling("emu/sameboy/sameboy.exe")
        os.makedirs(os.path.join(os.environ["APPDATA"], "SameBoy"), exist_ok=True)

    def startProcess(self, rom, *, gbc=False):
        if gbc:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "sameboy.prefs.gbc.bin"), os.path.join(os.environ["APPDATA"], "SameBoy", "prefs.bin"))
            self.startup_time = 3.5
        else:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "sameboy.prefs.dmg.bin"), os.path.join(os.environ["APPDATA"], "SameBoy", "prefs.bin"))
            self.startup_time = 6.5
        return subprocess.Popen(["emu/sameboy/sameboy.exe", os.path.abspath(rom)], cwd="emu/sameboy")
