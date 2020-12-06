import time
import os
import PIL.Image

from util import *


class Emulator:
    def __init__(self, name, *, startup_time=1.0):
        self.name = name
        self.startup_time = startup_time
        self.title_check = lambda title: title.startswith(self.name)
        self.speed = 1.0
    
    def setup(self):
        raise NotImplementedError()

    def startProcess(self, rom, *, gbc=False):
        raise NotImplementedError()

    def postStartup(self):
        pass
    
    def getScreenshot(self):
        return getScreenshot(self.title_check)

    def run(self, test):
        print("Running %s on %s" % (test, self))
        
        sav_file = os.path.splitext(test.rom)[0] + ".sav"
        if os.path.exists(sav_file):
            os.unlink(sav_file)
        
        p = self.startProcess(test.rom, gbc=test.gbc)
        process_create_time = time.time()
        while findWindow(self.title_check) is None:
            time.sleep(0.01)
            assert p.poll() is None, "Process crashed?"
            assert time.time() - process_create_time < 30.0, "Creating the window took longer then 30 seconds?"
        time.sleep(self.startup_time + 1.0)
        self.postStartup()
        start_time = time.time()
        while time.time() - start_time < test.runtime / self.speed:
            time.sleep(0.1)
            screenshot = self.getScreenshot()
            if test.checkResult(screenshot) == True:
                print("Early exit: %g" % (time.time() - start_time))
                break
        p.terminate()
        return test.checkResult(screenshot), screenshot
    
    def getRunTimeFor(self, test):
        p = self.startProcess(test.rom, gbc=test.gbc)
        while findWindow(self.title_check) is None:
            time.sleep(0.01)
            assert p.poll() is None
        time.sleep(self.startup_time)
        start = time.time()
        last_change = time.time()
        prev = None
        while True:
            time.sleep(0.1)
            screenshot = self.getScreenshot()
            if prev is not None and not compareImage(screenshot, prev):
                last_change = time.time()
            prev = screenshot
            if time.time() - last_change > 10.0:
                break
        if not os.path.exists(test.result):
            screenshot.save(test.result)
        p.terminate()
        return last_change - start

    def measureStartupTime(self, gbc=False):
        p = self.startProcess("startup_time_test.gb", gbc=gbc)
        reference = PIL.Image.open("startup_time_test.png")
        start_pre_window_time = time.time()
        while findWindow(self.title_check) is None:
            time.sleep(0.01)
            assert p.poll() is None
        post_window_time = time.time()
        print("Window found")
        while True:
            screenshot = self.getScreenshot()
            if screenshot.size[0] != 160 or screenshot.size[1] != 144:
                continue
            colors = screenshot.getcolors()
            if colors is None or len(colors) != 2:
                continue
            if not compareImage(screenshot, reference):
                continue
            break
        startup_time = time.time() - post_window_time
        p.terminate()
        return startup_time

    def __repr__(self):
        return self.name
