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
import argparse

import tests.blarg
import tests.mooneye
import tests.acid
from emulators.bgb import BGB
from emulators.vba import VBA, VBAM
from emulators.mgba import MGBA
from emulators.sameboy import SameBoy
from emulators.nocash import NoCash
from emulators.gambatte import GambatteSpeedrun
from emulators.emulicious import Emulicious
from util import *


emulators = [
    # MGBA(), MGBA is currently not working, so skip that.
    SameBoy(),
    BGB(),
    VBA(),
    VBAM(),
    NoCash(),
    GambatteSpeedrun(),
    Emulicious(),
]
tests = tests.acid.all + tests.blarg.all + tests.mooneye.all

def checkFilter(input, filter_data):
    if filter_data is None:
        return True
    input = str(input)
    for f in filter_data:
        if f not in input:
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='append', help="Filter for tests with keywords")
    parser.add_argument('--emulator', action='append', help="Filter to test only emulators with keywords")
    parser.add_argument('--get-runtime', action='store_true')
    parser.add_argument('--get-startuptime', action='store_true')
    args = parser.parse_args()
    
    tests = [test for test in tests if checkFilter(test, args.test)]
    emulators = [emulator for emulator in emulators if checkFilter(emulator, args.emulator)]
    
    print("%d emulators" % (len(emulators)))
    print("%d tests" % (len(tests)))
    
    if args.get_runtime:
        for emulator in emulators:
            emulator.setup()
            for test in tests:
                if not checkFilter(test, args.test):
                    continue
                print("%s: %s: %g seconds" % (emulator, test, emulator.getRunTimeFor(test)))
        sys.exit()

    if args.get_startuptime:
        f = open("startuptime.html", "wt")
        f.write("<html><body>\n")
        for emulator in emulators:
            emulator.setup()
            dmg_start_time, dmg_screenshot = emulator.measureStartupTime(gbc=False)
            gbc_start_time, gbc_screenshot = emulator.measureStartupTime(gbc=True)
            if dmg_start_time is not None and gbc_start_time is not None:
                print("Startup time: %s = %g (dmg) %g (gbc)" % (emulator, dmg_start_time, gbc_start_time))
            f.write("%s (dmg)<br>\n<img src='data:image/png;base64,%s'>\n" % (emulator, imageToBase64(dmg_screenshot)))
            f.write("%s (gbc)<br>\n<img src='data:image/png;base64,%s'>\n" % (emulator, imageToBase64(gbc_screenshot)))
        f.write("</body></html>")
        sys.exit()

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
        f.write("<tr><td>%s (%d/%d)</td>\n" % (emulator, passed, len(results[emulator])))
        for test in tests:
            result_string = {True: "PASS", False: "FAILED", None: "UNKNOWN"}[results[emulator][test][0]]
            f.write("  <td>%s<br><img src='data:image/png;base64,%s'></td>\n" % (result_string, imageToBase64(results[emulator][test][1])))
        f.write("</tr>\n")
    f.write("</table></body></html>")
