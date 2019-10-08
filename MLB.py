#import pandas as pd
#from ESPN_Last_7 import get_last7
from ESPN_Regular_Season import get_last7db
from MLB_Hot_Hitters import get_hitting_streaks
from Player_Splits import get_player_splits
from MLB_Lineups import get_lineups


def main():
    print("Loading DB's...")
    last_7_df = get_last7db()
    hitting_streak_df = get_hitting_streaks()
    lineups_df = get_lineups()
    #print(last_7_df)
    lineup_splits = get_lineup_splits(lineups_df,last_7_df)
    lineup_splits = filter_players(lineup_splits)
    get_weightedAvg(lineup_splits)
    lineup_splits.sort(key=lambda player: player[3], reverse=True)
    for player in lineup_splits:
        print(player[0])
    #print((lineup_splits))
    #get_top_hitters(hitting_streak_df, last_7_df, lineups_df)


    # for player in hitting_streak_df.iloc[:, 0]:
    #    players_with_hitting_streak.append(player)
    #    print(player)
    #
    # for player in lineups_df.iloc[:,0]:
    #     print(player)

# get_hitter_splits(last_7_df, hitting_streak_df, players_with_hitting_streak)
# print(players_with_hitting_streak)
# for url in players_with_hitting_streak:
#   print (get_player_splits(url))

# print(player)
# print(players_with_hitting_streak)
# print_dbs(last_7_df, hitting_streak_df)
# get_player_url(last_7_df)
# get_splits_by_player(last_7_df)

def get_top_hitters(hitting_streak_df, last_7_df, lineups_df):
    in_lineup = []
    lineup_urls = []

    #check for players with in top 10 active hitting streak
    for player in hitting_streak_df.iloc[:,0]:
       if check_daily_lineups(lineups_df, player):
           lineup_urls.append(get_player_url(last_7_df, player))

    # get players not in top 10 hiting streaks
    # for player in lineups_df.iloc[:,0]:
    #     print(player)
    #     url = get_player_url(last_7_df, player)
    #     if url not in lineup_urls:
    #         lineup_urls.append(url)

    player_splits = []
    for url in lineup_urls:
        #print(url)
        splits = get_player_splits(url)
        print(splits, '\n')
        print(splits.iloc[:,1])
        player_splits.append(splits)

# get splits for all players in daily_lineup
def get_lineup_splits(lineups_df, last_7_df):
    lineup_splits = []
    try:
        for player in lineups_df.iloc[:, 0]:
            player_url = get_player_url(last_7_df, player)
            #print(last7)
            #print(player, player_url)
            if player_url:
                last7 = get_player_last7(last_7_df, player_url)
                lineup_splits.append([player, get_player_splits(player_url),last7, None])
        return lineup_splits
    except Exception:
        pass

def filter_players(lineup_splits):
    for player in list(lineup_splits):
        name = player[0]
        splits = player[1]
        # get last7Avg and Last7AB
        #last7 = player[2]
        #print(last7)
        last7AB = int(player[2][0])
        last7Avg = float(player[2][1])
        last_row = (splits.iloc[-1,0])
        faced_pitcher = False

        if 'vs.' in last_row: # check if vs Pitcher history
            faced_pitcher = True
            pitcher_splits = splits.iloc[-1,:]
            vsPitcherAB = int(pitcher_splits[1])
            vsPitcherAvg = float(pitcher_splits[9])
            #print(pitcher_splits)
            #print('ABs:',pitcher_splits[1])
            #print('AVG:', pitcher_splits[9])

        if faced_pitcher is False:
            #print(f"{name} has never faced pitcher")
            lineup_splits.remove(player) # if not PitcherHistory discard player

        elif last7Avg < .250 or last7AB < 10:
            #print(f"{name} sucks")
            lineup_splits.remove(player)

        elif vsPitcherAvg < .250 or vsPitcherAB < 6:
            #print(f"{name} sucks vs pitcher")
            lineup_splits.remove(player)

    return lineup_splits

def get_weightedAvg(lineup_splits):
    for i, player in enumerate(lineup_splits, 0):
        #splits = player[1]
        pitcher_splits =  player[1].iloc[-1,:]
        last7Avg = float(player[2][1])
        vsPitcherAvg = float(pitcher_splits[9])
        rank_avg = ( (last7Avg + vsPitcherAvg) / 2)
        player[3] = rank_avg
    #return lineup_splits
    #sorted(lineup_splits, rank_avg)

# print DB's
def print_dbs(last_7_df, hitting_streak_df):
    print(hitting_streak_df)
    print(last_7_df)


def get_splits_by_player(last_7_df):
    player_url = get_player_url(last_7_df)
    splits = get_player_splits(player_url)
    return splits

# get ESPN player url from last_7_df
def get_player_url(last_7_df, player_name):
    #player_name = input("Enter name of player: ")  # get name of player to search for
    if player_name[1] == '.':
        first_initial, last_name = player_name.split('. ')
        #print(first_initial,last_name)
        for i, player in enumerate(last_7_df.iloc[:, 0], 0):  # search player names in last_7_df
            if last_name in player and first_initial == player[0]:
                player_url = last_7_df.iloc[i, 17][0]  # if names match, return url
                return player_url
    else:
        for i, player in enumerate(last_7_df.iloc[:, 0], 0):  # search player names in last_7_df
            if player == player_name:
                player_url = last_7_df.iloc[i, 17][0]  # if names match, return url
                return player_url

def get_player_last7(last_7_df, url):
    for i, player_url in enumerate(last_7_df.iloc[:, 17], 0):  # search player names in last_7_df
        if player_url[0] == url:
            AB = last_7_df.iloc[i, 2]
            AVG = last_7_df.iloc[i, 13]
            return (AB, AVG)

# check if a player is listed in daily_lineup
def check_daily_lineups(lineups_df, player_name): # Check if a player is playing today
    #player_name = input("Enter name of player: ")  # get name of player to search for
    for player in lineups_df.iloc[:, 0]:
        if player == player_name:
            return True
            #print("player found")
            #break


def get_hitter_splits(last_7_df, hitting_streak_df, players_with_hitting_streak):

    for i, player1 in enumerate(last_7_df.iloc[:, 0], 0):  # go through players in last_7_df

        # check if player is in hitting_streak_df
        for j, player2 in enumerate(hitting_streak_df.iloc[:, 0]):
            if player1 == player2:
                player_url = last_7_df.iloc[i, 17][0]
                current_streak = hitting_streak_df.iloc[j, 1]
                p_splits = (player2, get_player_splits(player_url))
                print('\n',
                      p_splits[0], "\n",
                      "Current Hit Streak: ", current_streak, '\n',
                      p_splits[1])
                players_with_hitting_streak.append(p_splits)


main()
