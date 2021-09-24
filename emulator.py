import time
import os
import PIL.Image
from collections import namedtuple

from util import *


TestResult = namedtuple('TestResult', ['result', 'screenshot', 'startuptime', 'runtime'])

class Emulator:
    def __init__(self, name, url, *, startup_time=1.0, features=None):
        self.name = name
        self.url = url
        self.startup_time = startup_time
        self.title_check = lambda title: title.startswith(self.name)
        self.speed = 1.0
        self.features = features or set()
    
    def setup(self):
        raise NotImplementedError()

    def startProcess(self, rom, *, model, required_features):
        raise NotImplementedError()

    def postWindowCreation(self):
        pass

    def getScreenshot(self):
        return getScreenshot(self.title_check)

    def run(self, test):
        print("Running %s on %s" % (test, self))
        
        sav_file = os.path.splitext(test.rom)[0] + ".sav"
        if os.path.exists(sav_file):
            os.unlink(sav_file)
        
        p = self.startProcess(test.rom, model=test.model, required_features=test.required_features)
        if p is None:
            print("%s cannot run %s (incompattible model or feature requests)" % (self, test))
            return None
        process_create_time = time.monotonic()
        while findWindow(self.title_check) is None:
            time.sleep(0.01)
            assert p.poll() is None, "Process crashed?"
            assert time.monotonic() - process_create_time < 30.0, "Creating the window took longer then 30 seconds?"
        process_create_time = time.monotonic() - process_create_time
        self.postWindowCreation()
        start_time = time.monotonic()
        result = None
        while time.monotonic() - start_time < (test.runtime / self.speed) + self.startup_time + 5.0:
            time.sleep(0.1)
            screenshot = self.getScreenshot()
            if screenshot is not None:
                result = test.checkResult(screenshot)
                if result is not None:
                    print("Early exit: %s: %g" % (result, time.monotonic() - start_time))
                    break
            assert p.poll() is None, "Process crashed? (exit: %d)" % (p.returncode)
        p.terminate()
        if result is None:
            result = test.getDefaultResult()
        return TestResult(result=result, screenshot=screenshot, startuptime=process_create_time, runtime=time.monotonic()-start_time)

    def getRunTimeFor(self, test):
        p = self.startProcess(test.rom, model=test.model, required_features=test.required_features)
        if p is None:
            return None
        while findWindow(self.title_check) is None:
            time.sleep(0.01)
            assert p.poll() is None, "Process crashed?"
        time.sleep(self.startup_time)
        start = time.monotonic()
        last_change = time.monotonic()
        prev = None
        while True:
            time.sleep(0.1)
            screenshot = self.getScreenshot()
            if prev is not None and not compareImage(screenshot, prev):
                last_change = time.monotonic()
            prev = screenshot
            if time.monotonic() - last_change > 10.0:
                break
            assert p.poll() is None, "Process crashed?"
        if not os.path.exists(test.pass_result_filename):
            screenshot.save(test.pass_result_filename)
        p.terminate()
        return last_change - start

    def measureStartupTime(self, *, model):
        p = self.startProcess("startup_time_test.gb", model=model, required_features=set())
        if p is None:
            return None, None
        reference = PIL.Image.open("startup_time_test.png")
        start_pre_window_time = time.monotonic()
        while findWindow(self.title_check) is None:
            time.sleep(0.01)
            if p.poll() is not None or time.monotonic() - start_pre_window_time > 60.0:
                print("Process gone or timeout")
                if p.poll() is None:
                    p.terminate()
                return None, fullscreenScreenshot()
        post_window_time = time.monotonic()
        print("Window found")
        while True:
            if p.poll() is not None or time.monotonic() - post_window_time > 60.0:
                print("Process gone or timeout: %s" % (p.poll()))
                if p.poll() is None:
                    p.terminate()
                return None, fullscreenScreenshot()
            screenshot = self.getScreenshot()
            if screenshot is None:
                continue
            if screenshot.size[0] != 160 or screenshot.size[1] != 144:
                continue
            colors = screenshot.getcolors()
            if colors is None or len(colors) != 2:
                continue
            if not compareImage(screenshot, reference):
                continue
            break
        startup_time = time.monotonic() - post_window_time
        screenshot = fullscreenScreenshot()
        p.terminate()
        return startup_time, screenshot

    def getJsonFilename(self):
        return "%s.json" % (self.name.replace(" ", "_").lower())

    def __repr__(self):
        return self.name
