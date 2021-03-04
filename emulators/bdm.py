from util import *
from emulator import Emulator
import shutil


class BDM(Emulator):
    def __init__(self):
        super().__init__("Beaten Dying Moon", "https://mattcurrie.com/bdm-demo/", startup_time=5.0)
        self.title_check = lambda title: "Beaten Dying Moon" in title

    def setup(self):
        download("https://mattcurrie.com/bdm/downloads/bdms-win.zip", "downloads/bdm.zip")
        extract("downloads/bdm.zip", "emu/bdm")
        setDPIScaling("emu/bdm/bdms.exe")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin", "emu/bdm/cgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/bdm/dmg_boot.bin")
    
    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/bdm/bdms.exe", "-scale", "1", "-turbo", "-cgb" if gbc else "-dmg", os.path.abspath(rom)], cwd="emu/bdm")
