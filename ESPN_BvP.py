import pandas as pd
import requests
from bs4 import BeautifulSoup

test_url = 'http://www.espn.com/mlb/player/batvspitch/_/id/32081/teamId/20'

def get_pitcher_splits(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', attrs={'class': 'tablehead'}) # get table html
    headers_row = table.find('tr', attrs={'class': 'colhead'})
    split_rows = table.find_all("tr")
    headers = []

    player_splits = []

    for col in headers_row: # get individual headers
        headers.append(col.text) # store in list

    for line in split_rows[2:-1]: # get Batter info
        player_line = []

        name = line.find('a') # find player name
        player_line.append(name.get_text())

        splits = line.find_all('td', attrs={'class': 'textright'})
        for stat in splits: # get individual stats
             player_line.append(stat.get_text())
        player_splits.append(player_line)

    df = pd.DataFrame(player_splits, columns=headers) # create dataframe from player_db using db_columns
    return(df)

def get_team_id(abr):
    team_ids = {'BAL': 1,
                'BOS': 2,
                'LAA' : 3,
                'CWS' : 4,
                'CLE' : 5,
                'DET': 6,
                'KC': 7,
                'MIL': 8,
                'MIN': 9,
                'NYY': 10,
                'OAK': 11,
                'SEA': 12,
                'TEX': 13,
                'TOR': 14,
                'ATL': 15,
                'CHC': 16,
                'CIN': 17,
                'HOU': 18,
                'LAD': 19,
                'WSH': 20,
                'NYM': 21,
                'PHI': 22,
                'PIT': 23,
                'STL': 24,
                'SD': 25,
                'SF': 26,
                'COL': 27,
                'MIA': 28,
                'ARI': 29,
                'TB': 30,
    }
    return team_ids[abr]

if __name__ == "__main__":
    df = get_pitcher_splits(test_url)
    print(df)
