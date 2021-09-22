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
import json

import tests.blarg
import tests.mooneye
import tests.acid
import tests.samesuite
import tests.ax6
import tests.daid
import tests.hacktix
import tests.cpp
from emulators.kigb import KiGB
from emulators.bgb import BGB
from emulators.vba import VBA, VBAM
from emulators.mgba import MGBA
from emulators.sameboy import SameBoy
from emulators.nocash import NoCash
from emulators.gambatte import GambatteSpeedrun
from emulators.emulicious import Emulicious
from emulators.bdm import BDM
from emulators.higan import Higan
from emulators.goomba import Goomba
from emulators.binjgb import Binjgb
from emulators.pyboy import PyBoy
from util import *


emulators = [
    BDM(),
    MGBA(), # Black screen on github actions
    KiGB(), # Crashes on github actions
    SameBoy(),
    BGB(),
    VBA(),
    VBAM(),
    NoCash(),
    GambatteSpeedrun(),
    Emulicious(),
    # Higan(), # Crashes all over the place.
    Goomba(),
    Binjgb(),
    PyBoy(),
]
tests = tests.acid.all + tests.blarg.all + tests.daid.all + tests.ax6.all + tests.mooneye.all + tests.samesuite.all + tests.hacktix.all + tests.cpp.all

def checkFilter(input, filter_data):
    if filter_data is None:
        return True
    input = str(input)
    for f in filter_data:
        if f.startswith("!"):
            if f[1:] in input:
                return False
        else:
            if f not in input:
                return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='append', help="Filter for tests with keywords")
    parser.add_argument('--emulator', action='append', help="Filter to test only emulators with keywords")
    parser.add_argument('--get-runtime', action='store_true')
    parser.add_argument('--get-startuptime', action='store_true')
    parser.add_argument('--dump-emulators-json', action='store_true')
    parser.add_argument('--dump-tests-json', action='store_true')
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
    if args.dump_emulators_json:
        json.dump({
            str(emulator): {
                "file": emulator.getJsonFilename(),
                "url": emulator.url,
            } for emulator in emulators
        }, open("emulators.json", "wt"), indent="  ")
    if args.dump_tests_json:
        json.dump([
            {
                'name': str(test),
                'description': test.description,
                'url': test.url,
            } for test in tests
        ], open("tests.json", "wt"), indent="  ")
    if args.dump_tests_json or args.dump_emulators_json:
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
    emulators.sort(key=lambda emulator: len([result[0] for result in results[emulator].values() if result.result != "FAIL"]), reverse=True)
    
    for emulator in emulators:
        data = {
            'emulator': str(emulator),
            'date': time.time(),
            'tests': {str(test): {'result': result.result, 'startuptime': result.startuptime, 'runtime': result.runtime, 'screenshot': imageToBase64(result.screenshot)} for test, result in results[emulator].items()},
        }
        json.dump(data, open(emulator.getJsonFilename(), "wt"), indent="  ")
