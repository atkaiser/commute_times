'''
Created on Feb 11, 2015

@author: akaiser

A script to get the transit time between two locations.  Before being run copy the config.py.tmp
file to config.py and set the desired values. Meant to be run many times to collect
aggregate data at different times of the week.  Later it can be analyzed to determine what the best
time to leave is. Run like:

    python commute_times.py <data_file>

or if you want to switch the origin and destination:

    python commute_times.py <data_file> -switch

I have mine running through cron in the following command:

*/5 5-10 * * 1-5 <path to python> <path to data file>
'''

import sys
import requests
import re
from datetime import datetime

import config

DEBUG = True

def get_time(switch):
    if switch:
        url = "http://maps.google.com/maps?f=q&source=s_q&hl=en&q=to+" + \
              config.origin + "+from+" + config.destination
    else:
        url = "http://maps.google.com/maps?f=q&source=s_q&hl=en&q=to+" + \
              config.destination + "+from+" + config.origin
              
    response = requests.get(url)
    matches = re.findall('"[0-9 hr]+? min"', response.text)
    print matches
    match = matches[1]
    time = time_from_string(match)
    if DEBUG:
        print "URL: " + url
        print "Match: " + match
#         print "Response: " + json_response
        print "Time: " + str(time)
    return time

def time_from_string(match):
    hours = 0
    hour_match = re.search('(\d+) hr', match)
    if hour_match:
        hours = int(hour_match.group(1)) * 60
    min_match = re.search('(\d+) min', match)
    minutes = int(min_match.group(1))
    time = minutes + hours
    return time

def write_time_to_file(data_file, shortest_time):
    # Write to data file
    with open(data_file, "a+") as data:
        now_time = datetime.now().strftime("%Y-%m-%d,%H:%M")
        weekday = datetime.today().weekday()
        data_list = [now_time, weekday, shortest_time]
        data_list = map(str, data_list)
        data.write(",".join(data_list) + "\n")
    
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        data_file = sys.argv[1]
    switch = len(sys.argv) >= 3 and sys.argv[2] == "-switch"
    shortest_time = get_time(switch)
    if len(sys.argv) >= 2:
        write_time_to_file(data_file, shortest_time)
