from util import *
from emulator import Emulator
from test import *
import shutil
import requests
import re
import zipfile


class Masquerade(Emulator):
    def __init__(self):
        super().__init__("Masquerade", "https://github.com/Kotambail-Hegde/Masquerade-Emulator",
                         startup_time=5.0, features=(PCM,))

    def setup(self):
        downloadGithubRelease("Kotambail-Hegde/Masquerade-Emulator", "downloads/masquerade.zip")

        if extract("downloads/masquerade.zip", "emu/masquerade_temp"):
            # Flatten the extracted folder
            import shutil
            nested_folder = os.path.join("emu/masquerade_temp", os.listdir("emu/masquerade_temp")[0])
            if os.path.exists("emu/masquerade"):
                shutil.rmtree("emu/masquerade")
            shutil.move(nested_folder, "emu/masquerade")
            shutil.rmtree("emu/masquerade_temp")

            # Modify CONFIG.ini
            config_path = "emu/masquerade/assets/CONFIG.ini"
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    content = f.read()

                # Modify [mods] section
                content = re.sub(
                    r'(\[mods\].*?)_VIDEO_EFFECTS=[^\n]+',
                    r'\1_VIDEO_EFFECTS=NO_FILTER',
                    content,
                    flags=re.DOTALL
                )
                content = re.sub(
                    r'(\[mods\].*?)_MUTE_AUDIO=[^\n]+',
                    r'\1_MUTE_AUDIO=true',
                    content,
                    flags=re.DOTALL
                )

                # Modify [gb-gbc] section
                content = re.sub(
                    r'(\[gb-gbc\].*?)_volume=[^\n]+',
                    r'\1_volume=0.0',
                    content,
                    flags=re.DOTALL
                )
                content = re.sub(
                    r'(\[gb-gbc\].*?)_force_gb_palette=[^\n]+',
                    r'\1_force_gb_palette=Black/White',
                    content,
                    flags=re.DOTALL
                )
                content = re.sub(
                    r'(\[gb-gbc\].*?)_enable_cgb_color_correction=[^\n]+',
                    r'\1_enable_cgb_color_correction=true',
                    content,
                    flags=re.DOTALL
                )

                content = re.sub(
                    r'(\[gb-gbc\].*?)_XFPS=[^\n]+',
                    r'\1_XFPS=500',
                    content,
                    flags=re.DOTALL
                )

                content = re.sub(
                    r'(\[gb-gbc\].*?)_XSCALE=[^\n]+',
                    r'\1_XSCALE=4',
                    content,
                    flags=re.DOTALL
                )

                with open(config_path, 'w') as f:
                    f.write(content)

            download("https://github.com/libsdl-org/SDL/releases/download/release-3.2.0/SDL3-3.2.0-win32-x64.zip",
                     "downloads/sdl3.zip")
            if extract("downloads/sdl3.zip", "downloads/sdl3_temp"):
                import shutil
                shutil.copy("downloads/sdl3_temp/SDL3.dll", "emu/masquerade/SDL3.dll")
                shutil.rmtree("downloads/sdl3_temp")

            download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin",
                     "emu/masquerade/assets/gbc/bios/cgb_boot.bin")
            download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin",
                     "emu/masquerade/assets/gb/bios/dmg_boot.bin")
        setDPIScaling("emu/masquerade/masquerade.exe")

    def startProcess(self, rom, *, model, required_features):
        if model == DMG:
            self.startup_time = 5.0
        elif model == CGB:
            self.startup_time = 5.0
        else:
            return None
        return subprocess.Popen(["emu/masquerade/masquerade.exe", os.path.abspath(rom)], cwd="emu/masquerade")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None

        w, h = screenshot.size

        # Crop borders (your values)
        left = 0
        top = 45  # for _XSCALE=4
        right = w
        bottom = h - 25  # for _XSCALE=4

        if right <= left or bottom <= top:
            print("Invalid crop: window too small")
            return None

        cropped = screenshot.crop((left, top, right, bottom))

        # Now resize to Game Boy resolution
        gb = cropped.resize((160, 144), PIL.Image.Resampling.NEAREST)

        return gb
