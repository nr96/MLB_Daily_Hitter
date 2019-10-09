from ESPN_Regular_Season import get_last7db
from Player_Splits import get_player_splits
from MLB_Lineups import get_lineups


def main():
    print("Loading DB's...")
    last_7_df = get_last7db()
    lineups_df = get_lineups()

    print("Running Algorithm...")
    lineup_splits = get_lineup_splits(lineups_df,last_7_df)
    filter_players(lineup_splits)
    get_weightedAvg(lineup_splits)
    lineup_splits.sort(key=lambda player: player[2], reverse=True)

    # final output
    if len(lineup_splits):
        print("\nMost Likely Hitters")
        for i, player in enumerate(lineup_splits,0):
            print(f"{i+1}. {player[0][0]}, weightedAvg: {player[2]}")
    else:
        print('No desirable hitters')

# get splits for all players in daily_lineup
def get_lineup_splits(lineups_df, last_7_df):
    lineup_splits = []
    for i, player in enumerate(lineups_df.iloc[:,0],0):
        opp_picther = lineups_df.iloc[i,4]
        player_info = get_player_info(last_7_df,player)
        if player_info: # player_info will be NoneType if not in last_7_df
             splits = get_player_splits(player_info[3])
             player_info.append(opp_picther)
             lineup_splits.append([player_info,splits])
    return lineup_splits


# discard players with undersirable stats or insufficient data
def filter_players(lineup_splits):
    for player in list(lineup_splits):
        splits = player[1]

        last_row = (splits.iloc[-1,0])
        faced_pitcher = False
        opp_pitcher_f, opp_pitcher_l = player[0][4].split()

        if f'vs. {opp_pitcher_l}' in last_row: # check if vs Pitcher history
            faced_pitcher = True
            pitcher_splits = splits.iloc[-1,:]
            vsPitcherAB = int(pitcher_splits[1])
            vsPitcherAvg = float(pitcher_splits[9])

        if faced_pitcher is False: # not enough info
            lineup_splits.remove(player) # if not PitcherHistory discard player

        elif vsPitcherAvg < .250 or vsPitcherAB < 6: # undersirable stats or sample size to small
            lineup_splits.remove(player)


# use last7GamesAvg and pitcherAvg to calculate weightedAvg
def get_weightedAvg(lineup_splits):
    for i, player in enumerate(lineup_splits, 0):
        pitcher_splits =  player[1].iloc[-1,:]
        last7Avg = player[0][2]
        vsPitcherAvg = float(pitcher_splits[9])
        print(player[0][0],last7Avg, vsPitcherAvg)
        weightedAvg = ( (last7Avg + vsPitcherAvg) / 2)
        player.append(weightedAvg)

def get_player_info(last_7_df, player_name):
    if player_name[1] == '.': first_name, last_name = player_name.split('. ')
    else: first_name, last_name = player_name.split()

    for i, player in enumerate(last_7_df.iloc[:, 0], 0):  # search player names in last_7_df
        if player_name == player or (last_name in player and first_name[0] == player[0]):
            AB = int(last_7_df.iloc[i, 2])
            AVG = float(last_7_df.iloc[i, 13])
            player_url = last_7_df.iloc[i, 17][0]  # if names match, return url

            if AVG > .250 and AB > 10: # undersirable stats or sample size to small
                return [player,AB,AVG,player_url]

main()
