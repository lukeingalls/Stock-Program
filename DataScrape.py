# This program will scrape data on any non-dividen paying company.

import sys
import time
import requests
import urllib.request
import csv
import random
from bs4 import BeautifulSoup
from selenium import webdriver

# Default values for the company being scraped and also the number of days to obtain.
code = 'TSLA'
day_range = 3000

# Use command line arguments if those are applicable.
if len(sys.argv) != 1:
	code = sys.argv[1]
	if len(sys.argv) > 2:
		day_range = int(sys.argv[2])

# Identifies who it is sending the requests
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'luin3949@colorado.edu'
    }
)

# These are used to calculate numerical values that will occur in the URL
epoch_time = int(time.time())
local_offset = 86400/4
today = epoch_time - ((epoch_time - local_offset) % 86400)
begin_date = today - 86400*day_range

# The URL that will be scraped
url = 'https://finance.yahoo.com/quote/'+ code +'/history?period1='+ str(int(begin_date)) +'&period2='+ str(int(today)) +'&interval=1d&filter=history&frequency=1d'

# Time buffer to decrease requests
SCROLL_PAUSE_TIME = 2

browser = webdriver.Chrome('/Users/iMac/Desktop/Projects/Stock/chromedriver')
browser.get(url)

# This gets the original height of the browser
last_height = browser.execute_script("return document.documentElement.scrollHeight")


# Keep scrolling until all the values have been loaded.
while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

page = browser.page_source

browser.quit()

# Start to actually parse the data
soup = BeautifulSoup(page, 'html.parser')

# Select the body of the page
table = soup.find('tbody')
rows = soup.findAll('tr')

data = []
for r in range(0,len(rows)):
    stats = rows[r].findAll('td')
    for s in range(0, len(stats)):
        stats[s] = stats[s].get_text()
    if (len(stats) > 4):
    	data.append(stats)

# Format the dates in an appropriate manner
for d in data[1:-7]:
    final = ''
    split_date = d[0].split(' ')
    split_date[1] = split_date[1][:-1]
    if (split_date[0] == 'Jan'):
        final = final + '1-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Feb'):
        final = final + '2-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Mar'):
        final = final + '3-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Apr'):
        final = final + '4-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'May'):
        final = final + '5-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Jun'):
        final = final + '6-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Jul'):
        final = final + '7-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Aug'):
        final = final + '8-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Sep'):
        final = final + '9-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Oct'):
        final = final + '10-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Nov'):
        final = final + '11-' + split_date[1] + '-' + split_date[2]
    elif (split_date[0] == 'Dec'):
        final = final + '12-' + split_date[1] + '-' + split_date[2]

    d[0] = final

    d[-1] = d[-1].replace(',','')


# Write the data to a file.
with open("/Data/" + code + ".csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(data[1:len(data) - 7])