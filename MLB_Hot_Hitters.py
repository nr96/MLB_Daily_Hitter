import pandas as pd
import requests
from bs4 import BeautifulSoup

# Program mines the first 20 hitters with longest active hitting streaks from baseballmusings's
# 'Current Hit Streaks' database and stores them in a pandas dataframe.


def get_hitting_streaks():
    url = 'https://www.baseballmusings.com/cgi-bin/CurStreak.py' # link to MLB current hit streak leaders
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('table', attrs={'class': 'dbd'}) # get table html
    players_rows = table.find_all('tr') # get player rows from table

    headers = [] # list for headers of table
    headers = get_headers(headers, players_rows[0]) # get column headers from first row of table

    players = [] # list of hitter stats
    players = get_players(players, players_rows[1:21]) # get first 20 hitters

    df = pd.DataFrame(players, columns=headers) # create dataframe from player_db using db_columns
    return(df)


def get_headers(headers, header_row):
    for col in header_row:
        try:
            headers.append(col.text) # add individual column headers to list
        except AttributeError:
            pass

    headers = (headers[:12]) # discard date header
    return headers


def get_players(players, player_rows):
    for player in player_rows:
        stats = [stat.text for stat in player.find_all('td')] # get stats for player
        stats[0] = (stats[0][:len(stats[0]) - 1]) # discard \n from name
        players.append(stats[:12]) # add to players list

    return players
