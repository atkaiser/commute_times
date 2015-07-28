'''
Created on Feb 11, 2015

@author: akaiser

A script to get the transit time between two locations.  Meant to be run many times to collect
aggregate data at different times of the week.  Later it can be analyzed to determine what the best
time to leave is. Run like:

    python commute_times.py <data_file>

or if you want to switch the origin and destination:

    python commute_times.py <data_file> -switch

I have mine running through cron in the following command:

*/5 5-10 * * 1-5 <path to python> <path to data file>
'''

import urllib2
import re
import sys
from datetime import datetime

DEBUG = True

# Configs: Change these to what you want to record
origin = "37+May+Ct,+Hayward,+CA+94544"
destination = "777+Mariners+Island+Blvd,+San+Mateo,+CA+94404"

def get_time(switch):
    if switch:
        url = "https://www.google.com/maps/dir/" + destination + "/" + origin + "/"
    else:
        url = "https://www.google.com/maps/dir/" + origin + "/" + destination + "/"
    response = urllib2.urlopen(url)
    html = response.read()
    # Find transit times from google
    times = re.findall("In current traffic: (\d+) min", html)
    if DEBUG:
        print url
        print html
        print times
    # Print error if there were no times
    if len(times) == 0:
        print "ERROR: No times from google"
        return
    shortest_time = int(times[0])
    for time in times:
        time_int = int(time)
        if time_int < min:
            shortest_time = time_int
    return shortest_time

def write_time_to_file(data_file, shortest_time):
    # Write to data file
    with open(data_file, "a+") as data:
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        weekday = datetime.today().weekday()
        data_list = [time, weekday, shortest_time]
        data_list = map(str, data_list)
        data.write(",".join(data_list) + "\n")
    
if __name__ == '__main__':
    data_file = sys.argv[1]
    switch = len(sys.argv) >= 3 and sys.argv[2] == "-switch"
    time = get_time(switch)
    write_time_to_file(data_file, shortest_time)
