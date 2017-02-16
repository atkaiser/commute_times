from selenium import webdriver
import time
from pyvirtualdisplay import Display
import traceback
import sys
import queue


class RouteFinder:
    
    drivers = queue.Queue()
    pool_size = 2
    initiated = False

    def __init__(self):
        while not RouteFinder.initiated and RouteFinder.drivers.qsize() < RouteFinder.pool_size:
            display = Display(visible=0, size=(1024, 768))
            display.start()
            driver = webdriver.Chrome()
            driver.set_window_size(1024, 768)
            RouteFinder.drivers.put(driver)
        RouteFinder.initiated = True
            

    def get_time_and_route(self, origin, destination):
        url = "http://maps.google.com/maps?f=q&source=s_q&hl=en&q=to+" + \
              destination + "+from+" + origin
        driver = RouteFinder.drivers.get()
        try:
            driver.get(url)
            elems = driver.find_elements_by_xpath('//button[text()=" Details "]')
            while not elems:
                time.sleep(1)
                elems = driver.find_elements_by_xpath('//button[text()=" Details "]')
            elem = elems[0]
            time.sleep(1)
            elem.click()
            elems = driver.find_elements_by_xpath("//h1[@class='section-trip-summary-title']")
            while not elems:
                time.sleep(1)
                elems = driver.find_elements_by_xpath("//h1[@class='section-trip-summary-title']")
            elem = elems[0]
            time_str = elem.text
            elem = driver.find_element_by_xpath("//h1[@class='section-directions-trip-title']")
            summary_route = elem.text
            detailed_route = []
            # elems = driver.find_elements_by_xpath("//div[@class='directions-mode-group-title']")
            elems = driver.find_elements_by_xpath("//div[@data-groupindex!='']")
            for elem in elems:
                if elem.text:
                    detailed_route.append(elem.text)
        except Exception as e:
            print(e)
            traceback.print_exc(limit=100, file=sys.stdout)
        RouteFinder.drivers.put(driver)
        return [time_str, summary_route, detailed_route]

if __name__ == "__main__":
    router = RouteFinder()
    time_str, summary_route, detailed_route = router.get_time_and_route("777+Mariners+Island+Blvd,+San+Mateo,+CA+94404", "5024+Ray+Ave,+Castro+Valley,+CA+94546")
    print("Time: " + time_str)
    print("Summary route: " + summary_route)
    print("Detailed route:")
    for line in detailed_route:
        print(line)
    