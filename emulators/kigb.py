from util import *
from emulator import Emulator
import os
import shutil


class KiGB(Emulator):
    def __init__(self):
        super().__init__("KiGB", "http://kigb.emuunlim.com/", startup_time=1.6)
        self.gbc = False

    def setup(self):
        download("http://kigb.emuunlim.com/kigb_win.zip", "downloads/kigb.zip")
        extract("downloads/kigb.zip", "emu/kigb")
        setDPIScaling("emu/kigb/kigb.exe")
    
    def startProcess(self, rom, *, gbc=False):
        open("emu/kigb/kigb.cfg", "wt").write("""
SIZE_FACTOR = 1
EMU_TYPE = %d
PALETTE = 1
GB_DEVICE = 1
GBC_REAL_COLOR = 1
SGB_BORDER = 0
EMU_SPEED = 2
""" % (2 if gbc else 1))
        self.gbc = gbc
        return subprocess.Popen(["emu/kigb/kigb.exe", os.path.abspath(rom)], cwd="emu/kigb")
