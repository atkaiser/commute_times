'''
Created on May 20, 2017

This is supposed to hold a browser.  Additionally it knows how to close all process related to this
specific browser.

@author: akaiser
'''

import os
import signal

from pyvirtualdisplay import Display
from selenium import webdriver


class Browser:

    def __init__(self):
        """
        Start up the browser and selenium driver and keep track of the
        process that they are using so that we can kill them later on.
        """
        self._display = Display(visible=0, size=(1024, 768))
        self._display.start()
        self._driver = webdriver.Chrome()
        self._driver.set_window_size(1024, 768)
        # Somehow I need to know what process these are running
        # so that I can shut them down later
        self._display_pid = self._display.pid
        self._driver_pid = self._driver.service.process.pid

        self.uses_count = 0

    def close(self):
        """
        This should kill any processes that this object created.
        """
        self._driver.quit()
        self._display.stop()
        try:
            os.kill(self._driver_pid, signal.SIGTERM)
        except OSError:
            pass
        try:
            os.kill(self._display_pid, signal.SIGTERM)
        except OSError:
            pass

    def get_driver(self):
        self.uses_count += 1
        return self._driver
