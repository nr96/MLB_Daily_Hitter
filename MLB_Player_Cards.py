import pandas as pd
import requests
from bs4 import BeautifulSoup

test_url = 'http://mlb.mlb.com/team/player.jsp?player_id=543685'

def get_player_card(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    splits = soup.find('div', attrs={'class': 'player-splits__container'}) #
    splits_tables = splits.find('table') # get table html
    table_info = splits_tables.find_all('span')
    table_text = [header.text for header in table_info]

    headers = table_text[:12]
    headers[0] = "Splits"

    last_7 = table_text[12:24]
    last_15 = table_text[24:36]
    last_30 = table_text[36:]

    player_splits = [last_7,last_15,last_30]

    df = pd.DataFrame(player_splits, columns=headers) # create dataframe from player_db using db_columns
    return(df)

if __name__ == "__main__":
    df = get_player_card(test_url)
    print(df)
