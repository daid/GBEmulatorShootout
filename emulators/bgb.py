from util import *
from emulator import Emulator
import shutil


class BGB(Emulator):
    def __init__(self):
        super().__init__("bgb", "https://bgb.bircd.org/", startup_time=0.6)
        self.speed = 10.0

    def setup(self):
        download("https://bgb.bircd.org/bgb.zip", "downloads/bgb.zip")
        extract("downloads/bgb.zip", "emu/bgb")
        setDPIScaling("emu/bgb/bgb.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "bgb.ini"), "emu/bgb/bgb.ini")
    
    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/bgb/bgb.exe", "-set", "SystemMode=%d" % (1 if gbc else 0), "-set", "Speed=%g" % (self.speed), "-set", "LoadRomWarnings=0", "-set", "Width=160", "-set", "Height=144", "-set", "SoundOut=null", os.path.abspath(rom)], cwd="emu/bgb")


class BGBRC(Emulator):
    def __init__(self):
        super().__init__("bgb-r159", "https://bgb.bircd.org/", startup_time=0.6)
        self.title_check = lambda title: "bgb" in title
        self.speed = 10.0

    def setup(self):
        download("https://bgb.bircd.org/bgb.zip", "downloads/bgb.zip")
        extract("downloads/bgb.zip", "emu/bgb")
        download("https://bgb.bircd.org/bgb-159-rc64.exe", "emu/bgb/bgb-159-rc64.exe")
        setDPIScaling("emu/bgb/bgb-159-rc64.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "bgb.ini"), "emu/bgb/bgb.ini")
    
    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/bgb/bgb-159-rc64.exe", "-set", "SystemMode=%d" % (1 if gbc else 0), "-set", "Speed=%g" % (self.speed), "-set", "LoadRomWarnings=0", "-set", "Width=160", "-set", "Height=144", "-set", "SoundOut=null", os.path.abspath(rom)], cwd="emu/bgb")
