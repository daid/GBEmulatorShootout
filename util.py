import pyautogui
import requests
import os
import zipfile
import subprocess
import win32gui
import PIL.Image
import PIL.ImageChops
import io
import base64


def download(url, filename):
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        print("Downloading %s" % (url))
        r = requests.get(url, allow_redirects=True)
        open(filename, "wb").write(r.content)

def downloadGithubRelease(repo, filename, *, filter=lambda n: "win" in n):
    if not os.path.exists(filename):
        r = requests.get("https://api.github.com/repos/%s/releases/latest" % (repo))
        url = None
        for asset in r.json()["assets"]:
            if filter(asset["name"]):
                url = asset["browser_download_url"]
                break
        download(url, filename)

def extract(filename, path):
    if os.path.exists(path):
        return False
    if filename.endswith(".zip"):
        zipfile.ZipFile(filename).extractall(path)
    elif filename.endswith(".7z"):
        os.makedirs(path, exist_ok=True)
        if os.path.exists("c:/Program Files/7-Zip/7z.exe"):
            subprocess.run(["c:/Program Files/7-Zip/7z.exe", "x", os.path.abspath(filename)], cwd=path)
        else:
            subprocess.run(["7z", "x", os.path.abspath(filename)], cwd=path)        
    return True

def findWindow(title_check):
    def f(hwnd, results):
        title = win32gui.GetWindowText(hwnd)
        if title_check(title):
            results.append(hwnd)
    results = []
    win32gui.EnumWindows(f, results)
    if results:
        return results[0]
    return None

def getScreenshot(title_check):
    hwnd = findWindow(title_check)
    if not hwnd:
        print("Window not found....")
        def f(hwnd, _):
            title = win32gui.GetWindowText(hwnd)
            if title:
                print(hwnd, title)
        win32gui.EnumWindows(f, None)
        return None
    rect = win32gui.GetClientRect(hwnd)
    position = win32gui.ClientToScreen(hwnd, (rect[0], rect[1]))
    return pyautogui.screenshot(region=(position[0], position[1], rect[2], rect[3]))

def fullscreenScreenshot():
    return pyautogui.screenshot()

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

def imageToBase64(img):
    tmp = io.BytesIO()
    img.save(tmp, "png")
    return base64.b64encode(tmp.getvalue()).decode('ascii')
