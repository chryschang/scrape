#!/usr/bin/python
import sys                          #parse system inputs
import requests                     #parse HTTP requests
import time                         #timer for script efficiency
import os                           #to get current working directory
from bs4 import BeautifulSoup       #beautifulsoup to parse html pages
import urllib.request               #interacting with urls
import re                           #regex

start_time = time.clock() #timer

# syntax reminder
if len(sys.argv) > 3 or len(sys.argv) < 2:
    print("Please specify link and optional output location (defaults to current working drive).")
    print("Syntax: python scrape.py <link> /path/to/output")
    sys.exit()

# user specified input
url = sys.argv[1]

# define file saving location
if len(sys.argv) == 3:
    output = sys.argv[2] #define an output location
else:
    output = os.getcwd() #else pdf files will be stored in current working directory

# open specified link
resp = urllib.request.urlopen(url)
soup = BeautifulSoup(resp, "lxml", from_encoding=resp.info().get_param('charset'))

# hunt for a href links that contain pdf
for link in soup.find_all('a', href=True):
    if '.pdf' in link['href']:
        full_link = link['href']
        name = re.search('/documents/(.+?).pdf', full_link).group(1) # edit this regex to match the structure on your url of interest
        #indicate to user what was found
        print(link['href'])
        response = requests.get(link['href'])
        outputfile = output + "\\" + name + '.pdf'
        #save file to specified location or cwd
        with open(outputfile, 'wb') as f:
            f.write(response.content)

print("---%s seconds---" % (time.clock() - start_time))
