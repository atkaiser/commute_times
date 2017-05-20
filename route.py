import sys
import time
import traceback

from browser_pool import BrowserPool


MAX_SLEEP_TIME = 60


class RouteFinder:

    def __init__(self):
        self._browser_pool = BrowserPool()

    def get_time_and_route(self, origin, destination):
        url = "http://maps.google.com/maps?f=q&source=s_q&hl=en&q=to+" + \
              destination + "+from+" + origin
        browser = self._browser_pool.get_browser()
        try:
            driver = browser.get_driver()
            driver.get(url)
            elems = driver.find_elements_by_xpath(
                '//button[text()=" Details "]')
            sleep_time = 0
            while not elems:
                time.sleep(1)
                elems = driver.find_elements_by_xpath(
                    '//button[text()=" Details "]')
                sleep_time += 1
                if sleep_time > MAX_SLEEP_TIME:
                    raise Exception("Couldn't find Details button")
            elem = elems[0]
            time.sleep(1)
            elem.click()
            elems = driver.find_elements_by_xpath(
                "//h1[@class='section-trip-summary-title']")
            sleep_time = 0
            while not elems:
                time.sleep(1)
                elems = driver.find_elements_by_xpath(
                    "//h1[@class='section-trip-summary-title']")
                sleep_time += 1
                if sleep_time > MAX_SLEEP_TIME:
                    raise Exception(
                        "Couldn't find 'section-trip-summary-title'")
            elem = elems[0]
            time_str = elem.text
            elem = driver.find_element_by_xpath(
                "//h1[@class='section-directions-trip-title']")
            summary_route = elem.text
            detailed_route = []
            # elems = driver.find_elements_by_xpath("//div[@class='directions-mode-group-title']")
            elems = driver.find_elements_by_xpath(
                "//div[@data-groupindex!='']")
            for elem in elems:
                if elem.text:
                    detailed_route.append(elem.text)
        except Exception as e:
            print(e)
            traceback.print_exc(limit=100, file=sys.stdout)
        finally:
            self._browser_pool.return_browser(browser)
        if not time_str:
            time_str = -1
        if not summary_route:
            summary_route = ""
        if not detailed_route:
            detailed_route = ""
        return [time_str, summary_route, detailed_route]

if __name__ == "__main__":
    router = RouteFinder()
    time_str, summary_route, detailed_route = router.get_time_and_route(
        "777+Mariners+Island+Blvd,+San+Mateo,+CA+94404", "5024+Ray+Ave,+Castro+Valley,+CA+94546")
    print("Time: " + time_str)
    print("Summary route: " + summary_route)
    print("Detailed route:")
    for line in detailed_route:
        print(line)
