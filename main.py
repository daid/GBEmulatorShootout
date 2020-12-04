import pyautogui
import requests
import os
import zipfile
import subprocess
import time
import win32gui
import PIL.Image
import PIL.ImageChops
import sys
import base64
import io

import tests.blarg
from emulators.bgb import BGB
from emulators.vba import VBA
from emulators.sameboy import SameBoy


emulators = [
    BGB(),
    VBA(),
    SameBoy(),
]
tests = tests.blarg.all


if __name__ == "__main__":
    for emulator in emulators:
        emulator.setup()
        print("Startup time: %s = %g" % (emulator, emulator.measureStartupTime()))

if False:
    for test in tests:
        emulators[0].getRunTimeFor(test)

if __name__ == "__main__":
    results = {}
    for emulator in emulators:
        emulator.setup()
        results[emulator] = {}
        for test in tests:
            results[emulator][test] = emulator.run(test)

    f = open("results.html", "wt")
    f.write("<html><head><style>table { border-collapse: collapse } td { border: solid 1px }</style></head><body><table>\n")
    f.write("<tr><th>-</th>\n")
    for test in tests:
        f.write("  <th>%s</th>\n" % (test))
    f.write("</tr>\n");
    for emulator in emulators:
        passed = len([result[0] for result in results[emulator].values() if result[0]])
        f.write("<tr><td>%s (%d/%d)</td>\n" % (emulator, passed, len(tests)))
        for test in tests:
            tmp = io.BytesIO()
            results[emulator][test][1].save(tmp, "png")
            result_string = {True: "PASS", False: "FAILED", None: "UNKNOWN"}[results[emulator][test][0]]
            f.write("  <td>%s<br><img src='data:image/png;base64,%s'></td>\n" % (result_string, base64.b64encode(tmp.getvalue()).decode('ascii')))
        f.write("</tr>\n")
    f.write("</table></body></html>")
