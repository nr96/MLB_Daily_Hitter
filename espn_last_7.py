import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Program mines the first 320 hitters from ESPN's 'MLB Player Batting Stats - Last 7 Days - 2019'
# database and stores them in a pandas datagrame.

urls = ['http://www.espn.com/mlb/stats/batting/_/split/61/sort/atBats/count/',
        'http://www.espn.com/mlb/stats/batting/_/split/61/sort/atBats/count/41',
        'http://www.espn.com/mlb/stats/batting/_/split/61/sort/atBats/count/81',
        'http://www.espn.com/mlb/stats/batting/_/split/61/sort/atBats/count/121',
        'http://www.espn.com/mlb/stats/batting/_/split/61/sort/atBats/count/161',
        'http://www.espn.com/mlb/stats/batting/_/split/61/sort/atBats/count/201',
        'http://www.espn.com/mlb/stats/batting/_/split/61/sort/atBats/count/241',
        'http://www.espn.com/mlb/stats/batting/_/split/61/sort/atBats/count/281'
        ] # list of urls to mine

player_db = [] # list for players
db_columns = [] # list for coulumn headers

for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table') # get table html

    headers = soup.find('tr', attrs={'class':'colhead'}) # get headers html
    columns = [col.text for col in headers.find_all('td')] # get individual headers
    db_columns = columns[1:] # discard rank

    player_rows = table.find_all("tr", attrs={'class': re.compile("row player-10-")}) # get individual players html

    for player in player_rows:
        stats = [stat.text for stat in player.find_all('td')] # get stats for player
        stats = stats[1:] # discard rank
        player_db.append(stats) # add to player_db


df = pd.DataFrame(player_db, columns=db_columns) # create dataframe from player_db using db_columns

#df
