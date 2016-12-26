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

import argparse
import requests
import re
from datetime import datetime

DEBUG = False

def get_time(origin, destination):
    response = get_gdirections_response(origin, destination)
    matches = re.findall('"((\d+ h)|(\d+ min)|(\d+ h \d+ min))"', response)
    if matches:
        match = matches[1][0]
        time = time_from_string(match)
    else:
        time = -1
    if DEBUG:
        print "Match: " + match
        print "Time: " + str(time)
    return time

def time_from_string(match):
    hours = 0
    hour_match = re.search('(\d+) h', match)
    if hour_match:
        hours = int(hour_match.group(1)) * 60
    min_match = re.search('(\d+) min', match)
    if min_match:
        minutes = int(min_match.group(1))
    else:
        minutes = 0
    time = minutes + hours
    return time

# [[[["CA-92 W",[36369,"22.6 miles",1],[1660,"28 min"],0,null,null,[[1732,"29 min"],
def get_route_name(origin, destination):
    response = get_gdirections_response(origin, destination)
    matches = re.search(r'\[\[\[\["(.*?)",\[\d+,"\d+.?\d* miles",\d+\],\[\d+,"((\d+ h)|(\d+ min)|(\d+ h \d+ min))"\],\d+,null,null,\[\[\d+,"((\d+ h)|(\d+ min)|(\d+ h \d+ min))"\]', response)
    if matches:
        route_name = matches.group(1)
    else:
        route_name = "Err"
    if DEBUG:
#         print "Response: " + "\n".join(response.splitlines()[0:50])
#        print "Match: " + matches.group()
        print "Route Name: " + route_name
    return route_name
        

def get_gdirections_response(origin, destination):
    url = "http://maps.google.com/maps?f=q&source=s_q&hl=en&q=to+" + \
          destination + "+from+" + origin
    response = requests.get(url)
    if DEBUG:
        print "URL: " + url
#         print "Response: " + response.text
    return response.text

def write_time_to_file(data_file, shortest_time):
    # Write to data file
    with open(data_file, "a+") as data:
        now_time = datetime.now().strftime("%Y-%m-%d,%H:%M")
        weekday = datetime.today().weekday()
        data_list = [now_time, weekday, shortest_time]
        data_list = map(str, data_list)
        data.write(",".join(data_list) + "\n")


def write_route_to_file(file_name, shortest_time, route_name):
    with open(file_name, "a+") as data:
        now_time = datetime.now().strftime("%Y-%m-%d,%H:%M")
        weekday = datetime.today().weekday()
        data_list = [now_time, weekday, shortest_time, route_name]
        data_list = map(str, data_list)
        data.write(",".join(data_list) + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("origin", help="Origin location")
    parser.add_argument("dest", help="Destination location")
    parser.add_argument("-s", "--switch", action="store_true")
    parser.add_argument("-f", "--data_file", help="Append result to data file")
    parser.add_argument("-r", "--route", help="Print the best route")
    args = parser.parse_args()
    if (args.switch):
        origin = args.dest
        dest = args.origin
    else:
        origin = args.origin
        dest = args.dest
    shortest_time = get_time(origin, dest)
    route_name = get_route_name(args.dest, args.origin)
    if args.data_file:
        write_time_to_file(args.data_file, shortest_time)
    if args.route:
        write_route_to_file(args.route, shortest_time, route_name)
