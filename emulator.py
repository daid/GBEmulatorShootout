import time
import os

from util import *


class Emulator:
    def __init__(self, name, *, startup_time=1.0):
        self.name = name
        self.startup_time = startup_time
        self.title_check = lambda title: title.startswith(self.name)
        self.speed = 1.0
    
    def setup(self):
        raise NotImplementedError()

    def startProcess(self, rom):
        raise NotImplementedError()

    def run(self, test):
        print("Running %s on %s" % (test, self))
        p = self.startProcess(test.rom)
        time.sleep(self.startup_time + test.runtime / self.speed)
        screenshot = getScreenshot(self.title_check)
        p.terminate()
        if not test.checkResult(screenshot):
            return False, screenshot
        return True, screenshot
    
    def getRunTimeFor(self, test):
        p = self.startProcess(test.rom)
        time.sleep(self.startup_time)
        start = time.time()
        last_change = time.time()
        prev = None
        while True:
            time.sleep(0.1)
            screenshot = getScreenshot(self.title_check)
            if prev is not None and not compareImage(screenshot, prev):
                last_change = time.time()
            prev = screenshot
            if time.time() - last_change > 3.0:
                break
        if not os.path.exists(test.result):
            screenshot.save(test.result)
        if last_change - start > (test.runtime / self.speed) - 1.0:
            print("Time for test: %s = %g" % (test, (last_change - start) * self.speed))
        p.terminate()

    def __repr__(self):
        return self.name
