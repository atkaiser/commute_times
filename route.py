from selenium import webdriver
import time
from pyvirtualdisplay import Display
import traceback
import sys


def get_time_and_route(origin, destination):
    url = "http://maps.google.com/maps?f=q&source=s_q&hl=en&q=to+" + \
          destination + "+from+" + origin
    display = Display(visible=0, size=(1024, 768))
    display.start()
    driver = webdriver.Chrome()
    try:
        driver.set_window_size(1024, 768)
        driver.get(url)
        elems = driver.find_elements_by_xpath('//button[text()=" Details "]')
        while not elems:
            time.sleep(1)
            elems = driver.find_elements_by_xpath('//button[text()=" Details "]')
        elem = elems[0]
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
    driver.quit()
    display.stop()
    return [time_str, summary_route, detailed_route]

if __name__ == "__main__":
    time_str, summary_route, detailed_route = get_time_and_route("777+Mariners+Island+Blvd,+San+Mateo,+CA+94404", "5024+Ray+Ave,+Castro+Valley,+CA+94546")
    print("Time: " + time_str)
    print("Summary route: " + summary_route)
    print("Detailed route:")
    for line in detailed_route:
        print(line)
    