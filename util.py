import pyautogui
import requests
import os
import zipfile
import subprocess
import win32gui
import PIL.Image
import PIL.ImageChops


def download(url, filename):
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        print("Downloading %s" % (url))
        r = requests.get(url, allow_redirects=True)
        open(filename, "wb").write(r.content)

def extract(filename, path):
    if not os.path.exists(path):
        zipfile.ZipFile(filename).extractall(path)

def getScreenshot(title_check):
    def f(hwnd, results):
        title = win32gui.GetWindowText(hwnd)
        if title_check(title):
            results.append(hwnd)
    results = []
    win32gui.EnumWindows(f, results)
    hwnd = results[0]
    rect = win32gui.GetClientRect(hwnd)
    position = win32gui.ClientToScreen(hwnd, (rect[0], rect[1]))
    return pyautogui.screenshot(region=(position[0], position[1], rect[2], rect[3]))

def setDPIScaling(executable):
    subprocess.run(["REG", "ADD", "HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", "/V", os.path.abspath(executable), "/T", "REG_SZ", "/D", "~ HIGHDPIAWARE", "/F"])

def compareImage(a, b):
    a = a.convert(mode="L", dither=PIL.Image.NONE)
    b = b.convert(mode="L", dither=PIL.Image.NONE)
    result = PIL.ImageChops.difference(a, b)
    for count, color in result.getcolors():
        if color > 40:
            return False
    return True
