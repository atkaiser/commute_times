'''
Created on May 20, 2017

This is supposed to contain a pool of browser objects.  And will restart
them when necessary.

YOU MUST CHECK IN A BROWSER AFTER USING IT.

@author: akaiser
'''

from browser import Browser
import queue


MAX_CONCURRENT_BROWSERS = 2
MAX_REUSES = 200000

DEBUG = True


class BrowserPool:

    # Contains all the browsers that are sitting idle ready to be used
    _browsers = queue.Queue()
    # Contains all the browsers created that haven't been destroyed
    _current_browsers = []

    def __init__(self):
        if (len(BrowserPool._current_browsers) < MAX_CONCURRENT_BROWSERS):
            for _ in range(MAX_CONCURRENT_BROWSERS):
                print("Creating initial browsers")
                new_browser = Browser()
                BrowserPool._current_browsers.append(new_browser)

    def get_browser(self):
        try:
            if DEBUG:
                print("Looking for browser")
            browser = BrowserPool._browsers.get_nowait()
            if DEBUG:
                print("Got already created browser")
            return browser
        except queue.Empty:
            # if len(BrowserPool._current_browsers) < MAX_CONCURRENT_BROWSERS:
            #     print("Created a new browser")
            #     new_browser = Browser()
            #     BrowserPool._current_browsers.append(new_browser)
            #     return new_browser
            # else:
            if DEBUG:
                print("Wait for a browser to be returned")
            browser = BrowserPool._browsers.get()
            if DEBUG:
                print("Done waiting for a browser")
            return browser

    def return_browser(self, browser):
        if DEBUG:
            print("Browser returned")
        # if (self._reuse_browser(browser)):
        BrowserPool._browsers.put(browser)
        # else:
        #     BrowserPool._current_browsers.remove(browser)
        #     browser.close()

    def _reuse_browser(self, browser):
        if (browser.uses_count >= MAX_REUSES):
            if DEBUG:
                print("Not reusing browser")
                print(
                    "Current browser length: {}".format(len(BrowserPool._current_browsers)))
            return False
        return True

    def status(self):
        status_lines = ["Number of browsers: {}".format(
            len(self._current_browsers))]
        for i, browser in enumerate(self._current_browsers):
            status_lines.append("Browser {}".format(i))
            status_lines.append(
                "\t number of uses: {}".format(browser.uses_count))
            status_lines.append(
                "\t display pid: {}".format(browser._display_pid))
            status_lines.append(
                "\t driver pid: {}".format(browser._driver_pid))
        return "\n".join(status_lines)

    def close_all(self):
        for browser in self._current_browsers:
            browser.close()
