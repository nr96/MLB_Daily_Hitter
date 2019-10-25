import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Program mines the Starting Pitcher's from ESPN's 'MLB Player Pitching Stats - As Starter - 2019'
# database and stores them in a pandas dataframe.


def get_espn_pitchers():
    urls = ['http://www.espn.com/mlb/stats/pitching/_/seasontype/2/split/127/sort/thirdInnings',
            'http://www.espn.com/mlb/stats/pitching/_/seasontype/2/split/127/sort/thirdInnings/count/41/',
            'http://www.espn.com/mlb/stats/pitching/_/seasontype/2/split/127/sort/thirdInnings/count/81/',
            'http://www.espn.com/mlb/stats/pitching/_/seasontype/2/split/127/sort/thirdInnings/count/121/',
            'http://www.espn.com/mlb/stats/pitching/_/seasontype/2/split/127/sort/thirdInnings/count/161/',
            'http://www.espn.com/mlb/stats/pitching/_/seasontype/2/split/127/sort/thirdInnings/count/201/',
            'http://www.espn.com/mlb/stats/pitching/_/seasontype/2/split/127/sort/thirdInnings/count/241/',
            ] # list of urls to mine

    pitcher_db = [] # list for players
    db_columns = [] # list for coulumn headers

    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table') # get table html
        player_rows = table.find_all("tr", attrs={'class': re.compile("row player-10-")}) # get individual players html

        db_columns = get_headers(soup)
        get_players(pitcher_db, player_rows)

    df = pd.DataFrame(pitcher_db, columns=db_columns) # create dataframe from pitcher_db using db_columns
    return df


def get_headers(soup):
    headers = soup.find('tr', attrs={'class': 'colhead'}) # get headers html
    columns = [col.text for col in headers.find_all('td')] # get individual headers
    columns[0] = "LINK" # change rank header to link
    columns = columns[1:] + columns[:1] # move 0th (link) column to last position
    return columns


def get_players(pitcher_db, player_rows):
    for player in player_rows:
        player_link = [a['href'] for a in player.find_all('a', href=True)] # get link to player's ESPN page
        stats = [stat.text for stat in player.find_all('td')] # get stats for player
        stats[0] = player_link[0] # discard rank and add player link
        stats = stats[1:] + stats[:1] # move 0th (link) column to last position
        pitcher_db.append(stats) # add to pitcher_db and discard rank

if __name__ == "__main__":
    df = get_espn_pitchers()
    df.set_index('PLAYER',inplace=True)
    # print(df)
    name = df.iloc[0,:]
    print(name)
    print()
    print(df.loc["Gerrit Cole"][-1])
