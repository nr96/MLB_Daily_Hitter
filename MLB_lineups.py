import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

#url = 'http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2018/start/1'
#url = 'http://www.rotowire.com/baseball/stats.php'
url = 'https://www.rotowire.com/baseball/daily-lineups.php'

page = requests.get(url) # get webpage from url
soup = BeautifulSoup(page.text, 'html.parser') # parse webpage into HTML

#attrs = {'attribute1_name': 'attribute1_value', 'attribute2_name': 'attribute2_value'}
lineup__abbr = soup.find_all('div', attrs={'class': 'lineup__abbr'}) # get team abbrevations
lineup_pitchers = soup.find_all('div', attrs={'class': 'lineup__player-highlight-name'}) # get team starting pitchers
lineups_boxs = soup.find_all('div', attrs={'class': 'lineup__box'}) # get game lineups

# get team abbrevations
teams = []
for team in lineup__abbr:
    teams.append(team.get_text())

# get team starting pitchers
pitchers = []
for pitcher in lineup_pitchers:
    pitchers.append(pitcher.a.text)

all_players = []
all_positions = []

# get team lineups
for lineup in lineups_boxs[:len(lineups_boxs) - 1]:
    players = lineup.find_all('li', attrs={'class': 'lineup__player'})
    home_players = []
    away_players = []
    #player_positions = []
    for player in players[:9]:
        #player_positions.append(player.div.text)
        home_players.append(player.a.text)
    for player in players[9:]:
        #player_positions.append(player.div.text)
        away_players.append(player.a.text)
    all_players.append(home_players)
    all_players.append(away_players)


#create list of (team,pitcher,players) tuples
team_lineups = tuple(zip(teams,pitchers,all_players))
it = iter(team_lineups) # create team_lineups iterable obj's

#for lineup in team_lineups:
#    print(lineup)
#    print()

matchups = tuple(zip(it,it)) # create matchup pairs from team_lineups tuples

#for matchup in matchups:
#    print(matchup)
#    print()

#print(matchups)


#print(player_names, player_positions)
#for lineup in all_players:
#    print(lineup)
