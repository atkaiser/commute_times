import argparse
from datetime import datetime
import signal
import sys

from timeout_utils import TimeoutException
from timeout_utils import handler
import requests


DEBUG = False


def write_time_to_file(data_file, response):
    # Write to data file
    with open(data_file, "a+") as data:
        now_time = datetime.now().strftime("%Y-%m-%d,%H:%M")
        weekday = datetime.today().weekday()
        data_list = [now_time,
                     weekday,
                     "deprecated",
                     response["time"],
                     response["summary_route"],
                     response["detailed_route"]]
        data_list = map(str, data_list)
        data.write(",".join(data_list) + "\n")


if __name__ == '__main__':
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(60)
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("origin", help="Origin location")
        parser.add_argument("dest", help="Destination location")
        parser.add_argument("-s", "--switch", action="store_true")
        parser.add_argument(
            "-f", "--data_file", help="Append result to data file")
        args = parser.parse_args()
        if not args.data_file:
            print("This is not supported with this script")
            sys.exit()
        if args.switch:
            origin = args.dest
            dest = args.origin
        else:
            origin = args.origin
            dest = args.dest
        r = requests.get(
            'http://sc2ls.mooo.com:10000/all_info?origin=' + origin + '&destination=' + dest)
        write_time_to_file(args.data_file, r.json())
    except TimeoutException as exc:
        print("Timed out while trying to run route: " + str(datetime.now()))
