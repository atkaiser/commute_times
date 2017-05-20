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
MAX_REUSES = 20

DEBUG = True


class BrowserPool:

    _browsers = queue.Queue()
    _current_browsers = []

    def __init__(self):
        pass

    def get_browser(self):
        try:
            browser = BrowserPool._browsers.get_nowait()
            if DEBUG:
                print("Got allready created browser")
            return browser
        except queue.Empty:
            if len(BrowserPool._current_browsers) < MAX_CONCURRENT_BROWSERS:
                print("Created a new browser")
                new_browser = Browser()
                BrowserPool._current_browsers.append(new_browser)
                return new_browser
            else:
                if DEBUG:
                    print("Wait for a browser to be returned")
                browser = BrowserPool._browsers.get()
                if DEBUG:
                    print("Done waiting for a browser")
                return browser

    def return_browser(self, browser):
        if DEBUG:
            print("Browser returned")
        if (self._reuse_browser(browser)):
            BrowserPool._browsers.put(browser)
        else:
            BrowserPool._current_browsers.remove(browser)
            browser.close()

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
