A collection of scripts to use headless chrome to query google maps for the time
between two addresses, store the results long term and analyze those results.

Installation:
Requires python 3.7+ and node 12.16.2+ then just run:
`npm install`
`pip install -r requirements.txt`

The useful scripts are run like:

`node get_time_cli.js <start address> <destination addresss>`
For example: `node get_time_cli.js 1+Dr+Carlton+B+Goodlett+Pl,+San+Francisco,+CA+94102 24+Willie+Mays+Plaza,+San+Francisco,+CA+94107`

There is a web server that can be run to get the time between arbitrary addresses:
`node app.js`