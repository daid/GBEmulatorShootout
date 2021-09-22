from util import *
from emulator import Emulator
import shutil
import os
import sys


class PyBoy(Emulator):
    def __init__(self):
        super().__init__("PyBoy", "https://github.com/Baekalfen/PyBoy", startup_time=5.0)
        self.title_check = lambda title: "CPU/frame" in title

    def setup(self):
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin", "emu/pyboy/cgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/pyboy/dmg_boot.bin")
        setDPIScaling(sys.executable)
        
        subprocess.Popen([sys.executable, "-m", "pip", "install", "pysdl2-dll"], cwd="emu/pyboy").wait()
        subprocess.Popen([sys.executable, "-m", "pip", "install", "pyboy"], cwd="emu/pyboy").wait()
    
    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen([sys.executable, "-m", "pyboy", "-b", "dmg_boot.bin", "-s", "1", os.path.abspath(rom)], cwd="emu/pyboy")
