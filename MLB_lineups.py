import pandas as pd
import requests
from bs4 import BeautifulSoup

#url = 'https://www.baseballpress.com/lineups?q=%2Flineups%2F'
#url = 'https://www.baseballpress.com/lineups/2019-09-29'
url = 'https://www.baseballpress.com/lineups/2019-10-22'

def get_lineups_df(url):
    page = requests.get(url) # get webpage from url
    soup = BeautifulSoup(page.text, 'html5lib') # parse webpage into HTML

    lineup_cards = soup.find_all('div', attrs={'class': 'lineup-card'}) # lineup_cards

    rows = build_rows(lineup_cards)
    headers = ["Player", 'Team', 'Pitcher', 'Opponent', 'Opponent Pitcher','Opp Hand', 'Link']
    df = pd.DataFrame(rows, columns=headers) # create dataframe from player_db using db_columns

    return(df)

def build_rows(lineup_cards):
    rows = []
    for card in lineup_cards:
        team_abbrs = card.find_all('a', attrs={'class': 'mlb-team-logo bc'})
        teams = [get_team_abbrs(team) for team in team_abbrs]

        starting_pitchers_html = card.find_all('div', attrs={'class': 'col col--min player'})
        pitchers = [get_starting_pitcher(pitcher) for pitcher in starting_pitchers_html]

        player_links = card.find_all('a', attrs={'class': 'player-link'})
        away_players = [get_starting_players(player) for player in player_links[2:11]]
        home_players = [get_starting_players(player) for player in player_links[11:]]

        home = teams[1]
        away = teams[0]
        home_pitch = pitchers[1][0]
        home_pitch_hand = pitchers[1][1]
        away_pitch = pitchers[0][0]
        away_pitch_hand = pitchers[0][1]
        for i in range(len(away_players)):
            away_player = away_players[i][0]
            link = away_players[i][1]
            row = [away_player, away, away_pitch, home, home_pitch, home_pitch_hand, link]
            rows.append(row)
        for i in range(len(home_players)):
            home_player = home_players[i][0]
            link = home_players[i][1]
            row = [home_player, home, home_pitch, away, away_pitch, away_pitch_hand, link]
            rows.append(row)
    return rows


def get_starting_players(player_html):
    name_d = player_html.find('span') # get non-standard long pitcher name
    link = str(player_html.get('href'))
    if name_d:
        return((name_d.get_text(),link))
    return((player_html.get_text(),link))


def get_starting_pitcher(pitcher):
    name = pitcher.find('a') # get standard pitcher name
    name_d = pitcher.find('span') # get non-standard long pitcher name
    hand = pitcher.get_text()[-2]

    if name_d:
        return((name_d.get_text(),hand))
    return((name.get_text(),hand))


def get_team_abbrs(team):
    href = str(team.get('href')).upper()
    return(href.split('/')[-1])

if __name__ == "__main__":
    df = get_lineups_df(url)
    print(df)
