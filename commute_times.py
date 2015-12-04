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

import urllib2
import sys
import json
import config
from datetime import datetime

DEBUG = False

def get_time(switch):
    if switch:
        url = "http://www.mapquestapi.com/directions/v2/route?doReverseGeocode=false&key=" + \
              config.mapquest_key + "&from=" + config.destination + "&to=" + config.origin
    else:
        url = "http://www.mapquestapi.com/directions/v2/route?doReverseGeocode=false&key=" + \
              config.mapquest_key + "&from=" + config.origin + "&to=" + config.destination
              
    response = urllib2.urlopen(url)
    json_response = response.read()
    json_data = json.loads(json_response)
    time = json_data["route"]["realTime"];
    if DEBUG:
        print "URL: " + url
        print "Response: " + json_response
        print "Time: " + str(time)
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
