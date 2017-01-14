A script to get the transit time between two locations.  Meant to be run many times to collect
aggregate data at different times of the week.  Later it can be analyzed to determine what the best
time to leave is. Run like:

    commute_times.py [-s] [-f DATA_FILE] origin dest

The -s flag will switch the origin and destination.

I have mine running through cron in the following command:

*/5 5-10 * * 1-5 \<path to python\> \<path to commute_times.py\> \<origin\> \<dest\> \<path to data file\>


How to setup:

sudo apt-get install xvfb
<install chrome browser>

pip install -r requirements.txt


How to run the web service:

nohup python web.py &> weblog.log &