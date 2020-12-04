from util import *
from emulator import Emulator


class VBA(Emulator):
    def __init__(self):
        super().__init__("VisualBoyAdvance", startup_time=4.0)
    
    def setup(self):
        download("https://sourceforge.net/projects/vba/files/latest/download", "downloads/vba.zip")
        extract("downloads/vba.zip", "emu/vba")
        setDPIScaling("emu/vba/VisualBoyAdvance.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "vba.ini"), "emu/vba/vba.ini")

    def startProcess(self, rom):
        return subprocess.Popen(["emu/vba/VisualBoyAdvance.exe", os.path.abspath(rom)], cwd="emu/vba")
