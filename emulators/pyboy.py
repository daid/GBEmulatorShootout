from util import *
from emulator import Emulator
import shutil
import sys


class PyBoy(Emulator):
    def __init__(self):
        super().__init__("PyBoy", "https://github.com/Baekalfen/PyBoy", startup_time=5.0)
        self.title_check = lambda title: "CPU/frame" in title

    def setup(self):
        downloadGithubRelease("Baekalfen/PyBoy", "downloads/pyboy.zip")
        extract("downloads/pyboy.zip", "emu/pyboy")
        self.__path = [f for f in os.listdir("emu/pyboy")][0]
        setDPIScaling(sys.executable)
        
        subprocess.Popen([sys.executable, "-m", "pip", "install", "pysdl2-dll"], cwd="emu/pyboy/%s" % (self.__path)).wait()
        subprocess.Popen([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd="emu/pyboy/%s" % (self.__path)).wait()
    
    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen([sys.executable, "-m", "pyboy", "-s", "1", os.path.abspath(rom)], cwd="emu/pyboy/%s" % (self.__path))
