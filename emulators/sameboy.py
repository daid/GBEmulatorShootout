from util import *
from emulator import Emulator
import os
import shutil


class SameBoy(Emulator):
    def __init__(self):
        super().__init__("SameBoy", startup_time=6.0)
    
    def setup(self):
        download("https://github.com/LIJI32/SameBoy/releases/download/v0.13.6/sameboy_winsdl_v0.13.6b.zip", "downloads/sameboy.zip")
        extract("downloads/sameboy.zip", "emu/sameboy")
        setDPIScaling("emu/sameboy/sameboy.exe")
        os.makedirs(os.path.join(os.environ["APPDATA"], "SameBoy"), exist_ok=True)
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "sameboy.prefs.bin"), os.path.join(os.environ["APPDATA"], "SameBoy", "prefs.bin"))

    def startProcess(self, rom):
        return subprocess.Popen(["emu/sameboy/sameboy.exe", os.path.abspath(rom)], cwd="emu/sameboy")
