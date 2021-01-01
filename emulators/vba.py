from util import *
from emulator import Emulator
import shutil


class VBA(Emulator):
    def __init__(self):
        super().__init__("VisualBoyAdvance", "https://sourceforge.net/projects/", startup_time=0.6)
    
    def setup(self):
        download("https://sourceforge.net/projects/vba/files/latest/download", "downloads/vba.zip")
        extract("downloads/vba.zip", "emu/vba")
        setDPIScaling("emu/vba/VisualBoyAdvance.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "vba.ini"), "emu/vba/vba.ini")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_bios.bin", "emu/vba/cgb_bios.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/vba/dmg_boot.bin")

    def startProcess(self, rom, *, gbc=False):
        return subprocess.Popen(["emu/vba/VisualBoyAdvance.exe", os.path.abspath(rom)], cwd="emu/vba")


class VBAM(Emulator):
    def __init__(self):
        super().__init__("VisualBoyAdvance-M", "https://vba-m.com/", startup_time=1.0)
        self.title_check = lambda title: "VisualBoyAdvance-M" in title
    
    def setup(self):
        downloadGithubRelease("visualboyadvance-m/visualboyadvance-m", "downloads/vba-m.zip", filter=lambda n: "Win" in n and "64bit" in n and n.endswith(".zip"))
        extract("downloads/vba-m.zip", "emu/vba-m")
        setDPIScaling("emu/vba-m/visualboyadvance-m.exe")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_bios.bin", "emu/vba-m/cgb_bios.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/vba-m/dmg_boot.bin")

    def startProcess(self, rom, *, gbc=False):
        if gbc:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "vbam.gbc.ini"), "emu/vba-m/vbam.ini")
        else:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "vbam.dmg.ini"), "emu/vba-m/vbam.ini")
        return subprocess.Popen(["emu/vba-m/visualboyadvance-m.exe", os.path.abspath(rom)], cwd="emu/vba-m")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        x = (screenshot.size[0] - 160) // 2
        y = (screenshot.size[1] - 144) // 2
        return screenshot.crop((x, y, x + 160, y + 144))
