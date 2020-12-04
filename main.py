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
import argparse

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

def checkFilter(input, filter_data):
    if filter_data is None:
        return True
    input = str(input)
    for f in filter_data:
        if f in input:
            return True
    return False


if False:
    for emulator in emulators:
        emulator.setup()
        print("Startup time: %s = %g" % (emulator, emulator.measureStartupTime()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='append', help="Filter for tests with keywords")
    parser.add_argument('--emulator', action='append', help="Filter to test only emulators with keywords")
    parser.add_argument('--get-runtime', action='store_true')
    args = parser.parse_args()
    
    if args.get_runtime:
        for emulator in emulators:
            if not checkFilter(emulator, args.emulator):
                continue
            emulator.setup()
            for test in tests:
                if not checkFilter(test, args.test):
                    continue
                print("%s: %s: %g seconds" % (emulator, test, emulator.getRunTimeFor(test)))
        sys.exit()

    results = {}
    for emulator in emulators:
        if not checkFilter(emulator, args.emulator):
            continue
        emulator.setup()
        results[emulator] = {}
        for test in tests:
            if not checkFilter(test, args.test):
                continue
            results[emulator][test] = emulator.run(test)

    f = open("results.html", "wt")
    f.write("<html><head><style>table { border-collapse: collapse } td { border: solid 1px }</style></head><body><table>\n")
    f.write("<tr><th>-</th>\n")
    for test in tests:
        f.write("  <th>%s</th>\n" % (test))
    f.write("</tr>\n");
    for emulator in emulators:
        if not checkFilter(emulator, args.emulator):
            continue

        passed = len([result[0] for result in results[emulator].values() if result[0]])
        f.write("<tr><td>%s (%d/%d)</td>\n" % (emulator, passed, len(results[emulator])))
        for test in tests:
            if not checkFilter(test, args.test):
                continue

            tmp = io.BytesIO()
            results[emulator][test][1].save(tmp, "png")
            result_string = {True: "PASS", False: "FAILED", None: "UNKNOWN"}[results[emulator][test][0]]
            f.write("  <td>%s<br><img src='data:image/png;base64,%s'></td>\n" % (result_string, base64.b64encode(tmp.getvalue()).decode('ascii')))
        f.write("</tr>\n")
    f.write("</table></body></html>")
