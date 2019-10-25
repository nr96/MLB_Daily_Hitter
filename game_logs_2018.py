import pandas as pd
from bs4 import BeautifulSoup

'''
    The information used here was obtained free of
    charge from and is copyrighted by Retrosheet.  Interested
    parties may contact Retrosheet at "www.retrosheet.org".

    https://www.retrosheet.org/gamelogs/
'''

def __main__():
    load_db()


def load_db():
    #file = open("GL2018.TXT")
    df = pd.read_csv("GL2018.TXT", header = None)
    #print(df.iloc[1-,:])
    game = df.iloc[0]
    "calendar_date visiting_team visiting_league visitor_game_number home_team home_league home_game_number visiting_score home_score day_night visiting_sp_id  visiting_sp_name home_sp_id  home_sp_name home_hitters"
    "1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 102, 103 104, 105 106-132 133-159"


def build_game_logs(game):
    "calendar_date visiting_team visiting_league visitor_game_number home_team home_league home_game_number visiting_score home_score day_night visiting_sp_id  visiting_sp_name home_sp_id  home_sp_name home_hitters"
    "1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 102, 103 104, 105 106-132 133-159"

    date = game[0]
    visiting_team = game[3]
    visiting_league = game[4]
    visitor_game_number = game[5]
    home_team = game[6]
    home_league = game[7]
    home_game_number = game[8]
    visiting_score = game[9]
    home_score  = game[10]
    day_night = game[12]
    visiting_sp_id  = game[102]
    visiting_sp_name = game[103]
    home_sp_id  = game[104]
    home_sp_name = game[105]

    home_lineup = []
    for i in range(106, 131,3):
        home_lineup.append(game[i])

    away_lineup = []
    for i in range(133, 158,3):
        away_lineup.append(game[i])


__main__()
