import pandas as pd
import requests
from bs4 import BeautifulSoup

test_url = 'http://www.espn.com/mlb/player/_/id/32422'

def get_player_splits(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # table = soup.find('table', attrs={'class': 'player-profile-container'}) # get table html
    table = soup.find('table', attrs={'class': 'tablehead'}) # get table html
    headers_row = table.find('tr', attrs={'class': 'colhead'})
    split_rows = table.find_all("tr")

    headers = []

    player_splits = []

    for col in headers_row: # get individual headers
        headers.append(col.text) # store in list

    for line in split_rows[1:]:
        split_line = []
        for stat in line:
            split_line.append(stat.text)
        player_splits.append(split_line)

    df = pd.DataFrame(player_splits, columns=headers) # create dataframe from player_db using db_columns

    return(df)

if __name__ == "__main__":
    get_player_splits(test_url)
