from util import *
from emulator import Emulator
from test import *
import shutil
import requests
import re
import zipfile
import os
import subprocess
import PIL.Image


# ===========================================================
#  CONFIG MANAGER
# ===========================================================
class ConfigManager:

    @staticmethod
    def rewrite_masquerade_paths(content: str, masquerade_abs_path: str) -> str:
        """
        Rewrites ANY absolute path that contains 'assets/' or 'assets\\',
        and forces it into: <masquerade_abs_path>/assets/<relative>

        Old path may have:
            .../masquerade/assets/...
            .../assets/...
            C:\anything\assets\...
            /mnt/c/whatever/assets/...
        """

        # match: absolute path *ANYTHING* followed by assets/<stuff>
        pattern = re.compile(
            r'([A-Za-z]:[\\/][^\n]*?assets[\\/][^\n]*)'
            r'|'
            r'(/[^ \n]*?assets/[^\n]*)'
        )

        def replace(match):
            original = match.group(1) or match.group(2)

            # Detect slash style from original
            slash = "\\" if "\\" in original else "/"

            # Normalize masquerade_abs_path
            base = masquerade_abs_path.replace("/", slash).replace("\\", slash)

            # Find "assets/"
            lower = original.lower()
            idx = lower.rfind("assets")
            if idx == -1:
                return original  # should never happen

            # Extract RELATIVE PART after assets/
            # e.g. "assets/ui/config" → "ui/config"
            rel = original[idx + len("assets") + 1:]
            rel = rel.replace("\\", slash).replace("/", slash)

            # Build final: <masquerade>/assets/<relative>
            return base + slash + "assets" + slash + rel

        return pattern.sub(replace, content)

    # -------------------------------------------------------
    #  PREP CONFIG
    # -------------------------------------------------------
    @staticmethod
    def prepConfig():
        config_path = "emu/masquerade/assets/CONFIG.ini"
        if not os.path.exists(config_path):
            return

        with open(config_path, 'r') as f:
            content = f.read()

        # --- [mods] ---
        content = re.sub(
            r'(\[mods\].*?)_VIDEO_EFFECTS=[^\n]+',
            r'\1_VIDEO_EFFECTS=NO_FILTER',
            content, flags=re.DOTALL
        )
        content = re.sub(
            r'(\[mods\].*?)_MUTE_AUDIO=[^\n]+',
            r'\1_MUTE_AUDIO=true',
            content, flags=re.DOTALL
        )

        # --- [gb-gbc] ---
        content = re.sub(
            r'(\[gb-gbc\].*?)_volume=[^\n]+',
            r'\1_volume=0.0',
            content, flags=re.DOTALL
        )
        content = re.sub(
            r'(\[gb-gbc\].*?)_force_gb_palette=[^\n]+',
            r'\1_force_gb_palette=Black/White',
            content, flags=re.DOTALL
        )
        content = re.sub(
            r'(\[gb-gbc\].*?)_enable_cgb_color_correction=[^\n]+',
            r'\1_enable_cgb_color_correction=true',
            content, flags=re.DOTALL
        )
        content = re.sub(
            r'(\[gb-gbc\].*?)_XFPS=[^\n]+',
            r'\1_XFPS=500',
            content, flags=re.DOTALL
        )
        content = re.sub(
            r'(\[gb-gbc\].*?)_XSCALE=[^\n]+',
            r'\1_XSCALE=4',
            content, flags=re.DOTALL
        )

        # Fix hardcoded absolute paths
        masquerade_abs_path = os.path.abspath("emu/masquerade")
        content = ConfigManager.rewrite_masquerade_paths(content, masquerade_abs_path)

        with open(config_path, 'w') as f:
            f.write(content)

    # -------------------------------------------------------
    #  toCGB
    # -------------------------------------------------------
    @staticmethod
    def toCGB():
        config_path = "emu/masquerade/assets/CONFIG.ini"
        if not os.path.exists(config_path):
            return

        with open(config_path, 'r') as f:
            content = f.read()

        content = re.sub(
            r'(\[gb-gbc\].*?)_force_gbc_for_gb=[^\n]+',
            r'\1_force_gbc_for_gb=true',
            content, flags=re.DOTALL
        )

        with open(config_path, 'w') as f:
            f.write(content)

    # -------------------------------------------------------
    #  toDMG
    # -------------------------------------------------------
    @staticmethod
    def toDMG():
        config_path = "emu/masquerade/assets/CONFIG.ini"
        if not os.path.exists(config_path):
            return

        with open(config_path, 'r') as f:
            content = f.read()

        content = re.sub(
            r'(\[gb-gbc\].*?)_force_gbc_for_gb=[^\n]+',
            r'\1_force_gbc_for_gb=false',
            content, flags=re.DOTALL
        )

        with open(config_path, 'w') as f:
            f.write(content)


# ===========================================================
#  MAIN EMULATOR CLASS
# ===========================================================
class Masquerade(Emulator):
    def __init__(self):
        super().__init__("Masquerade", "https://github.com/Kotambail-Hegde/Masquerade-Emulator",
                         startup_time=5.0, features=(PCM,))

    def setup(self):
        downloadGithubRelease("Kotambail-Hegde/Masquerade-Emulator", "downloads/masquerade.zip")

        if extract("downloads/masquerade.zip", "emu/masquerade_temp"):
            nested_folder = os.path.join("emu/masquerade_temp", os.listdir("emu/masquerade_temp")[0])

            if os.path.exists("emu/masquerade"):
                shutil.rmtree("emu/masquerade")

            shutil.move(nested_folder, "emu/masquerade")
            shutil.rmtree("emu/masquerade_temp")

            ConfigManager.prepConfig()

            download("https://github.com/libsdl-org/SDL/releases/download/release-3.2.0/SDL3-3.2.0-win32-x64.zip",
                     "downloads/sdl3.zip")

            if extract("downloads/sdl3.zip", "downloads/sdl3_temp"):
                shutil.copy("downloads/sdl3_temp/SDL3.dll", "emu/masquerade/SDL3.dll")
                shutil.rmtree("downloads/sdl3_temp")

            download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin",
                     "emu/masquerade/assets/gbc/bios/cgb_boot.bin")
            download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin",
                     "emu/masquerade/assets/gb/bios/dmg_rom.bin")

        setDPIScaling("emu/masquerade/masquerade.exe")

    def startProcess(self, rom, *, model, required_features):
        if model == DMG:
            self.startup_time = 5.0
            ConfigManager.toDMG()
        elif model == CGB:
            self.startup_time = 5.0
            ConfigManager.toCGB()
        else:
            return None

        return subprocess.Popen(
            ["emu/masquerade/masquerade.exe", os.path.abspath(rom)],
            cwd="emu/masquerade"
        )

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None

        w, h = screenshot.size
        left = 0
        top = 45
        right = w
        bottom = h - 25

        if right <= left or bottom <= top:
            print("Invalid crop: window too small")
            return None

        cropped = screenshot.crop((left, top, right, bottom))
        gb = cropped.resize((160, 144), PIL.Image.Resampling.NEAREST)

        return gb
