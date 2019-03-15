'''
Created on Mar 6, 2016

@author: akaiser
'''

import argparse
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument(
    "-f", "--file", help="The data file to parse", default="data/morn_route.csv")
args = parser.parse_args()

plt.rc('figure', figsize=(20, 11))

clean_file = "/tmp/clean.tmp"

with open(args.file, 'r') as data_file:
    with open(clean_file, 'w') as rewrite:
        for line in data_file:
            columns = line.split(",")
            columns = columns[0:5]
            new_line = ",".join(columns)
            rewrite.write(new_line + "\n")

df = pd.read_csv(clean_file, names=[
                 "date", "time", "weekday", "long time", "length"])

# Filter out the errors
df = df[df.length > 20]
df = df[df.length < 100]
df = df[(df.time.str[-1] == "0") | (df.time.str[-1] == "5")]

grouped = df.groupby(['weekday', 'time']).mean()
#
for weekday in grouped.index.levels[0]:
    labels = list(grouped.loc[weekday].index.values)
    labels = list(map(lambda time: datetime.strptime(time, "%H:%M"), labels))
    plt.plot(labels, grouped.loc[weekday], label=str(weekday))

plt.legend(loc='best')
plt.ylabel("Time in Minutes")
plt.show()
