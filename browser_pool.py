'''
Created on May 20, 2017

This is supposed to contain a pool of browser objects.  And will restart
them when necessary.

YOU MUST CHECK IN A BROWSER AFTER USING IT.

@author: akaiser
'''

import queue
from browser import Browser

MAX_CONCURRENT_BROWSERS = 3
MAX_REUSES = 2

DEBUG = True


class BrowserPool:

    _browsers = queue.Queue()
    _current_browsers = []

    def __init__(self):
        pass

    def get_browser(self):
        try:
            return BrowserPool._browsers.get_nowait()
        except queue.Empty:
            if len(BrowserPool._current_browsers) < MAX_CONCURRENT_BROWSERS:
                new_browser = Browser()
                BrowserPool._current_browsers.append(new_browser)
                return new_browser
            else:
                return BrowserPool._browsers.get()

    def return_browser(self, browser):
        if DEBUG:
            print("Browser returned")
        if (self._reuse_browser(browser)):
            BrowserPool._browsers.put(browser)
        else:
            BrowserPool._current_browsers.remove(browser)

    def _reuse_browser(self, browser):
        if (browser.uses_count >= MAX_REUSES):
            if DEBUG:
                print("Not reusing browser")
                print(
                    "Current browser length: {}".format(len(BrowserPool._current_browsers)))
            return False
        return True

    def close_all(self):
        for browser in self._current_browsers:
            browser.close()
