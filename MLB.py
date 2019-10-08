#from ESPN_Last_7 import get_last7
from ESPN_Regular_Season import get_last7db
from Player_Splits import get_player_splits
from MLB_Lineups import get_lineups


def main():
    print("Loading DB's...")
    last_7_df = get_last7db()
    lineups_df = get_lineups()
    lineup_splits = get_lineup_splits(lineups_df,last_7_df)
    lineup_splits = filter_players(lineup_splits)
    get_weightedAvg(lineup_splits)
    lineup_splits.sort(key=lambda player: player[3], reverse=True)
    for player in lineup_splits:
        print(player[0])


# get splits for all players in daily_lineup
def get_lineup_splits(lineups_df, last_7_df):
    lineup_splits = []
    try:
        for player in lineups_df.iloc[:, 0]:
            player_url = get_player_url(last_7_df, player)
            if player_url:
                last7 = get_player_last7(last_7_df, player_url)
                lineup_splits.append([player, get_player_splits(player_url),last7, None])
        return lineup_splits
    except Exception:
        pass

def filter_players(lineup_splits):
    for player in list(lineup_splits):
        splits = player[1]
        last7AB = int(player[2][0])
        last7Avg = float(player[2][1])
        last_row = (splits.iloc[-1,0])
        faced_pitcher = False

        if 'vs.' in last_row: # check if vs Pitcher history
            faced_pitcher = True
            pitcher_splits = splits.iloc[-1,:]
            vsPitcherAB = int(pitcher_splits[1])
            vsPitcherAvg = float(pitcher_splits[9])

        if faced_pitcher is False:
            lineup_splits.remove(player) # if not PitcherHistory discard player

        elif last7Avg < .250 or last7AB < 10:
            lineup_splits.remove(player)

        elif vsPitcherAvg < .250 or vsPitcherAB < 6:
            lineup_splits.remove(player)

    return lineup_splits

def get_weightedAvg(lineup_splits):
    for i, player in enumerate(lineup_splits, 0):
        pitcher_splits =  player[1].iloc[-1,:]
        last7Avg = float(player[2][1])
        vsPitcherAvg = float(pitcher_splits[9])
        rank_avg = ( (last7Avg + vsPitcherAvg) / 2)
        player[3] = rank_avg

# get ESPN player url from last_7_df
def get_player_url(last_7_df, player_name):
    if player_name[1] == '.':
        first_initial, last_name = player_name.split('. ')
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

main()
