import pandas as pd
from bs4 import BeautifulSoup
# from espn_last_7 import get_last7
# from MLB_Hot_Hitters import get_hitting_streaks
# from player_splits import get_player_splits
# from MLB_lineups import get_lineups

# import espn_last_7
# import MLB_Hot_Hitters
# import player_splits
# import MLB_lineups


def main():
    print("Loading DB's...")
    last_7_df = espn_last_7.get_last7()
    hitting_streak_df = MLB_Hot_Hitters.get_hitting_streaks()
    lineups_df = MLB_lineups.get_lineups()

    last_7_df = espn_last_7.get_last7()
    hitting_streak_df = MLB_Hot_Hitters.get_hitting_streaks()
    lineups_df = MLB_lineups.get_lineups()

    players_with_hitting_streak = []

# for player in hitting_streak_df.iloc[:, 0]:
#    players_with_hitting_streak.append(player)

# get_hitter_splits(last_7_df, hitting_streak_df, players_with_hitting_streak)
# print(players_with_hitting_streak)
# for url in players_with_hitting_streak:
#	print (get_player_splits(url))

# print(player)
# print(players_with_hitting_streak)
# print_dbs(last_7_df, hitting_streak_df)
# get_player_url(last_7_df)
# get_splits_by_player(last_7_df)
    check_daily_lineups(lineups_df)


def print_dbs(last_7_df, hitting_streak_df):
    print(hitting_streak_df)
    print(last_7_df)


def get_splits_by_player(last_7_df):
    player_url = get_player_url(last_7_df)
    splits = player_splits.get_player_splits(player_url)
    # print(player_splits)
    return splits


def get_player_url(last_7_df):
    player_name = input("Enter name of player: ") # get name of player to search for
    # print("Beginning Search....")
    for i, player in enumerate(last_7_df.iloc[:, 0], 0): # search player names in last_7_df
        if player == player_name:
            player_url = last_7_df.iloc[i, 17][0] # if names match, return url
            # print("player found: ", player_url)
            return player_url


def get_splits():
    pass


def check_daily_lineups(lineups_df):
    player_name = input("Enter name of player: ") # get name of player to search for
    for player in lineups_df.iloc[:, 0]:
        #print(player)
        if player == player_name:
            print ("player found")
            break


def get_hitter_splits(last_7_df, hitting_streak_df, players_with_hitting_streak):
    for i, player1 in enumerate(last_7_df.iloc[:, 0], 0): # go through players in last_7_df
        for j, player2 in enumerate(hitting_streak_df.iloc[:, 0]): # check if player is in hitting_streak_df
            if player1 == player2:
                # print('found: ', player2, "at ", i)
                player_url = last_7_df.iloc[i, 17][0]
                current_streak = hitting_streak_df.iloc[j, 1]
                # print (get_player_splits(player_url))
                p_splits = (player2, get_player_splits(player_url))
                print('\n',
                      p_splits[0], "\n",
                      "Current Hit Streak: ", current_streak, '\n',
                      p_splits[1])
                players_with_hitting_streak.append(p_splits)


main()
