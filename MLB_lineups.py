import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_lineups():

    url = 'https://www.rotowire.com/baseball/daily-lineups.php'

    page = requests.get(url) # get webpage from url
    soup = BeautifulSoup(page.text, 'html.parser') # parse webpage into HTML

    lineup__abbr = soup.find_all('div', attrs={'class': 'lineup__abbr'}) # get team abbrevations
    postponed = soup.find_all('div', attrs={'class': 'heading__desc'})
    lineup_pitchers = soup.find_all('div', attrs={'class': 'lineup__player-highlight-name'}) # get team starting pitchers
    lineups_boxs = soup.find_all('div', attrs={'class': 'lineup__box'}) # get game lineups

    # get team abbrevations
    teams = [team.get_text() for team in lineup__abbr]

    # get team starting pitchers
    pitchers = [pitcher.a.text for pitcher in lineup_pitchers]

    all_players = []
    #all_positions = []

    all_players = get_game_lineups(all_players, lineups_boxs)

    # create list of (team,pitcher,players) tuples
    team_lineups = tuple(zip(teams, pitchers, all_players))
    it = iter(team_lineups) # create team_lineups iterable obj's

    matchups = tuple(zip(it, it)) # create matchup pairs from team_lineups tuples

    if postponed:
        print(" \n WARNING!: A Postponed game has caused errors in team starting pitchers \n ")
        return make_db(matchups)
        print(" \n WARNING!: A Postponed game has caused errors in team starting pitchers \n ")

    else:
        # print_matchups(matchups)
        return (make_db(matchups))


def print_matchups(matchups):
    for matchup in matchups:
        print("     ", 'Home', "             ", 'Away')
        print("     ", matchup[0][0], "              ", matchup[1][0])
        print(matchup[0][1], "     ", matchup[1][1])
        print()
        for i in range(len(matchup[0][2])):
            print(matchup[0][2][i], "       ", matchup[1][2][i])

        print("==================================")


def make_db(matchups):
    rows = []
    headers = ["Player", 'Team', 'Pitcher', 'Opponent', 'Opponent Pitcher', 'Spot']
    for matchup in matchups:
        home = matchup[0][0]
        away = matchup[1][0]
        home_pitch = matchup[0][1]
        away_pitch = matchup[1][1]
        home_lineup = matchup[0][2]
        away_lineup = matchup[1][2]
        for i in range(len(home_lineup)):
            home_player = matchup[0][2][i]
            row = [home_player, home, home_pitch, away, away_pitch, i + 1]
            rows.append(row)
        for i in range(len(away_lineup)):
            away_player = matchup[1][2][i]
            row = [away_player, away, away_pitch, home, home_pitch, i + 1]
            rows.append(row)
    df = pd.DataFrame(rows, columns=headers) # create dataframe from player_db using db_columns
    return df


def get_game_lineups(all_players, lineups_boxs):
    # get team lineups
    for lineup in lineups_boxs[:len(lineups_boxs) - 1]:
        players = lineup.find_all('li', attrs={'class': 'lineup__player'})
        home_players = []
        away_players = []
        # player_positions = []
        for player in players[:9]:  # + players[9:]
            # player_positions.append(player.div.text)
            home_players.append(player.a.text)
        for player in players[9:]:
            away_players.append(player.a.text)

        all_players.append(home_players)
        all_players.append(away_players)
    return all_players


get_lineups()
