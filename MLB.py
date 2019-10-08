#from ESPN_Last_7 import get_last7
from datetime import datetime
startTime = datetime.now()


from ESPN_Regular_Season import get_last7db
from Player_Splits import get_player_splits
from MLB_Lineups import get_lineups
import_time = datetime.now() - startTime
db_time = 0
print('\nImport Time: ', import_time)


def main():
    print("Loading DB's...")
    last_7_df = get_last7db()
    lineups_df = get_lineups()
    global db_time
    db_time = ((datetime.now() - startTime) - import_time)
    print('\nDB Time: ', db_time)

    print("Running Algorithm...")
    lineup_splits = get_lineup_splits(lineups_df,last_7_df)
    filter_players(lineup_splits)
    get_weightedAvg(lineup_splits)
    lineup_splits.sort(key=lambda player: player[2], reverse=True)

    # print final output
    print("\nMost Likely Hitters")
    for i, player in enumerate(lineup_splits,0):
        print(f"{i+1}. {player[0][0]}, weightedAvg: {player[2]}")


# get splits for all players in daily_lineup
def get_lineup_splits(lineups_df, last_7_df):
    lineup_splits = []
    try:
        for player in lineups_df.iloc[:, 0]:
            player_info = get_player_info(last_7_df,player)
            if player_info: # player_info will be NoneType if not in last_7_df
                 splits = get_player_splits(player_info[3])
                 lineup_splits.append([player_info,splits])
        return lineup_splits
    except Exception:
        pass

# discard players with undersirable stats or insufficient data
def filter_players(lineup_splits):
    for player in list(lineup_splits):
        #          [      0         1  ]
        # player = [player_info, splits]
        #
        #               [     0         1        2        3     ]
        # player_info = [player_name,last7AB,last7Avg,player_url]

        splits = player[1]
        last7AB = player[0][1]
        last7Avg = player[0][2]

        last_row = (splits.iloc[-1,0])
        faced_pitcher = False

        if 'vs.' in last_row: # check if vs Pitcher history
            faced_pitcher = True
            pitcher_splits = splits.iloc[-1,:]
            vsPitcherAB = int(pitcher_splits[1])
            vsPitcherAvg = float(pitcher_splits[9])

        if faced_pitcher is False: # not enough info
            lineup_splits.remove(player) # if not PitcherHistory discard player

        elif last7Avg < .250 or last7AB < 10: # undersirable stats or sample size to small
            lineup_splits.remove(player)

        elif vsPitcherAvg < .250 or vsPitcherAB < 6: # undersirable stats or sample size to small
            lineup_splits.remove(player)


# use last7GamesAvg and pitcherAvg to calculate weightedAvg
def get_weightedAvg(lineup_splits):
    for i, player in enumerate(lineup_splits, 0):
        #          [      0         1  ]
        # player = [player_info, splits]
        #
        #               [     0         1        2        3     ]
        # player_info = [player_name,last7AB,last7Avg,player_url]
        pitcher_splits =  player[1].iloc[-1,:]
        last7Avg = player[0][2]
        vsPitcherAvg = float(pitcher_splits[9])
        rank_avg = ( (last7Avg + vsPitcherAvg) / 2)
        player.append(rank_avg)

def get_player_info(last_7_df, player_name):
    if player_name[1] == '.':
        first_name, last_name = player_name.split('. ')
    else:
        first_name, last_name = player_name.split()

    for i, player in enumerate(last_7_df.iloc[:, 0], 0):  # search player names in last_7_df
        if player_name == player or (last_name in player and first_name[0] == player[0]):
            AB = int(last_7_df.iloc[i, 2])
            AVG = float(last_7_df.iloc[i, 13])
            player_url = last_7_df.iloc[i, 17][0]  # if names match, return url
            return [player,AB,AVG,player_url]

main()
print('\nTotal Time: ', datetime.now() - startTime)
