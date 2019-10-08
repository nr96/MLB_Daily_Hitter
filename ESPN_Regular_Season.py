import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Program mines the first 320 hitters from ESPN's 'MLB Player Batting Stats - Last 7 Days - 2019'
# database and stores them in a pandas dataframe.


def get_last7db():
    urls = ['http://www.espn.com/mlb/stats/batting/_/seasontype/2',
            'http://www.espn.com/mlb/stats/batting/_/seasontype/2/split/61/count/41',
            'http://www.espn.com/mlb/stats/batting/_/seasontype/2/split/61/count/81',
            'http://www.espn.com/mlb/stats/batting/_/seasontype/2/split/61/count/121',
            'http://www.espn.com/mlb/stats/batting/_/seasontype/2/split/61/count/161',
            'http://www.espn.com/mlb/stats/batting/_/seasontype/2/split/61/count/201',
            'http://www.espn.com/mlb/stats/batting/_/seasontype/2/split/61/count/241',
            'http://www.espn.com/mlb/stats/batting/_/seasontype/2/split/61/count/281',
            'http://www.espn.com/mlb/stats/batting/_/seasontype/2/split/61/count/321',
            'http://www.espn.com/mlb/stats/batting/_/seasontype/2/split/61/count/361'
            ] # list of urls to mine

    player_db = [] # list for players
    db_columns = [] # list for coulumn headers

    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table') # get table html
        player_rows = table.find_all("tr", attrs={'class': re.compile("row player-10-")}) # get individual players html

        db_columns = get_headers(soup)
        get_players(player_db, player_rows)

    df = pd.DataFrame(player_db, columns=db_columns) # create dataframe from player_db using db_columns

    #print(df.iloc[0,:])
    return df


def get_headers(soup):
    headers = soup.find('tr', attrs={'class': 'colhead'}) # get headers html
    columns = [col.text for col in headers.find_all('td')] # get individual headers
    columns[0] = "LINK" # change rank header to link
    columns = columns[1:] + columns[:1] # move 0th (link) column to last position
    return columns


def get_players(player_db, player_rows):
    for player in player_rows:
        player_link = [a['href'] for a in player.find_all('a', href=True)] # get link to player's ESPN page
        stats = [stat.text for stat in player.find_all('td')] # get stats for player
        stats[0] = player_link # discard rank and add player link
        stats = stats[1:] + stats[:1] # move 0th (link) column to last position
        player_db.append(stats) # add to player_db and discard rank

#get_last7db()
