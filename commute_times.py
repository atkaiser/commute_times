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
import re
from datetime import datetime
import json
from route import RouteFinder
import os
import subprocess
import signal
import sys

DEBUG = False

class TimeoutException(Exception):
    pass

def get_time(origin, destination):
    finder = RouteFinder(2)
    time_str, _, _ = finder.get_time_and_route(origin, destination)
    return time_from_string(time_str)


def all_info(origin, destination):
    finder = RouteFinder(2)
    time_str, summary_route, detailed_route = finder.get_time_and_route(origin, destination)
    data = {}
    data["time"] = str(time_from_string(time_str))
    data["summary_route"] = summary_route
    better_detailed_route = map(lambda x: x.split("\n")[0], detailed_route)
    data["detailed_route"] = "||".join(better_detailed_route)
    return json.dumps(data)
    

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


def write_time_to_file(data_file, shortest_time):
    # Write to data file
    with open(data_file, "a+") as data:
        now_time = datetime.now().strftime("%Y-%m-%d,%H:%M")
        weekday = datetime.today().weekday()
        data_list = [now_time, weekday, shortest_time]
        data_list = map(str, data_list)
        data.write(",".join(data_list) + "\n")


def write_route_to_file(file_name, shortest_time, summary_route, detailed_route):
    with open(file_name, "a+") as data:
        now_time = datetime.now().strftime("%Y-%m-%d,%H:%M")
        weekday = datetime.today().weekday()
        better_detailed_route = map(lambda x: x.split("\n")[0], detailed_route)
        data_list = [now_time, weekday, time_str, time_from_string(time_str), summary_route, "||".join(better_detailed_route)]
        data_list = map(str, data_list)
        data.write(",".join(data_list) + "\n")

def cleanup():
    """Make sure there isn't any lingering Xvfb or chrome processes around"""
    # Find current proccess id
    main_pid = os.getpid()
    
    # Get group process id
    tree = subprocess.check_output("pstree -p " + str(main_pid), shell=True).decode(sys.stdout.encoding)
    for line in tree.split("\n"):
        matches = re.finditer(r'(\d+)', line)
        for match in matches:
            if int(match.group(1)) != main_pid:
                try:
                    os.kill(int(match.group(1)), signal.SIGTERM)
                except Exception:
                    pass

def handler(signum, frame):
    raise TimeoutException("")


if __name__ == '__main__':
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)
    try:
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
        finder = RouteFinder(2)
        time_str, summary_route, detailed_route = finder.get_time_and_route(origin, dest)
        finder.close()
        if not args.data_file and not args.route:
            print("Time: " + time_str)
            print("Summary route: " + summary_route)
            better_detailed_route = map(lambda x: x.split("\n")[0], detailed_route)
            print("Detailed route: " + "||".join(better_detailed_route))
        if args.data_file:
            write_time_to_file(args.data_file, time_from_string(time_str))
        if args.route:
            write_route_to_file(args.route, time_str, summary_route, detailed_route)
    except TimeoutException as exc:
        print("Timed out while trying to run route: " + str(datetime.now()))
    cleanup()
