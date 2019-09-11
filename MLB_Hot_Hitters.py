import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

url = 'https://www.baseballmusings.com/cgi-bin/CurStreak.py'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

#attrs = {'attribute1_name': 'attribute1_value', 'attribute2_name': 'attribute2_value'}
#hot_batters = soup.find_all('div', attrs = {'class': 'hcPlayerMugshot'})
table = soup.find('table', attrs={'class': 'dbd'}) # get table html
#hot_batters = soup.find_all('td', attrs = {'class': 'letter'}) #get names html
players_rows = table.find_all('tr') # get player rows from table


#headers = players_rows[0]
headers = []

for col in players_rows[0]:
    try: # replace with type check
        headers.append(col.text)
    except : # fix bare except
        pass

headers = (headers[:12]) # discard date header

#print(headers)

players = []

for line in players_rows[1:21]:
    name = line.find('td', attrs={'class': 'letter'}) # get name html
    name = name.get_text() # strip html
    name = name[:len(name) - 1] # discard /n
    stats = line.find_all('td', attrs={'class': 'number'}) # get stats from html
    row_stats = [] # list of stats in row
    for stat in stats[:11]: # ignore date
        row_stats.append(stat.text) # get get and add to row
    tmp_tuble = (name,row_stats)
    players.append(tmp_tuble) # add tuble to players list

#print(players)
