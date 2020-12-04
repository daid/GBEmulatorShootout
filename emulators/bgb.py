from util import *
from emulator import Emulator


class BGB(Emulator):
    def __init__(self):
        super().__init__("bgb", startup_time=2.0)
        self.speed = 10

    def setup(self):
        download("https://bgb.bircd.org/bgb.zip", "downloads/bgb.zip")
        extract("downloads/bgb.zip", "emu/bgb")
        setDPIScaling("emu/bgb/bgb.exe")
    
    def startProcess(self, rom):
        return subprocess.Popen(["emu/bgb/bgb.exe", "-set", "Speed=10", "-set", "LoadRomWarnings=0", "-set", "Width=160", "-set", "Height=144", os.path.abspath(rom)], cwd="emu/bgb")
