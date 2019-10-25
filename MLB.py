from ESPN_Pitcher_Stats import get_espn_pitchers
from MLB_Player_Cards import get_player_card
from ESPN_BvP import get_pitcher_splits, get_team_id
from MLB_lineups import get_lineups_df
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="use's test lineup instead of live lineup", action='store_true')
    args = parser.parse_args()
    load_dbs(args)

# load dbs according to args
def load_dbs(args):
    print("Loading DB's...")
    pitcher_db = get_espn_pitchers()
    if args.test:
        print("Using Test Lineup")
        lineups_df = get_lineups_df('https://www.baseballpress.com/lineups/2019-10-22')
        get_hitters(lineups_df,pitcher_db)
    else:
        lineups_df = get_lineups_df('https://www.baseballpress.com/lineups?q=%2Flineups%2F')
        if len(lineups_df) > 9:
            get_hitters(lineups_df,pitcher_db)
        else:
            print(" \nLineups not loaded, have they been released yet?")
            print('https://www.baseballpress.com/lineups?q=%2Flineups%2F\n')

# run algorithm for selecting hitters
def get_hitters(lineups_df,pitcher_db):
    print("Running Algorithm...")
    lineup_splits = get_lineup_splits(lineups_df,pitcher_db)
    players = filter_players(lineup_splits)
    hitters = get_weightedAvg(players)
    hitters.sort(key=lambda player: player[1], reverse=True)

    if len(hitters):
        print("\nMost Likely Hitters")
        for i, player in enumerate(hitters,0):
            print(f"{i+1}. {player[0]}, {round(player[1],3)}")
    else:
        print('No desirable hitters')


# get splits for all players in daily_lineup
def get_lineup_splits(lineups_df,pitcher_db):
    lineup_splits = []
    last_pitcher = ''
    last_pitcher_df = None
    pitcher_db.set_index('PLAYER',inplace=True)

    print(f"Loading Splits....")
    for index, player in lineups_df.iterrows():
        opp_pitcher = player[4]

        player_splits = get_player_card(player[6])

        if last_pitcher != opp_pitcher: # cache opp_pitcher info
            last_pitcher = opp_pitcher
            last_pitch_url = get_opp_pitch_url(opp_pitcher,pitcher_db)
            team_id = get_team_id(player[1])
            opp_pitcher_id = get_player_id(last_pitch_url)
            last_pitcher_df = get_PitcherHistory(opp_pitcher_id,team_id)

        for index,player_faced in last_pitcher_df.iterrows(): # get BvP History
            get_BvP(player_splits,player_faced,player[0],opp_pitcher)

        lineup_splits.append((player[0],player_splits))

    return lineup_splits

# get batter vs pitcher history
def get_BvP(player_splits,player_faced,name,opp_pitcher):
    hitter_name = player_faced[0]
    if hitter_name == name:
        ABs = player_faced[1]
        hits = player_faced[2]
        HRs = player_faced[5]
        RBIs = player_faced[6]
        BBs = player_faced[7]
        SOs= player_faced[8]
        AVG = player_faced[9]
        OBP = player_faced[10]
        SLG = player_faced[11]
        bvp_hitory = [f'vs {opp_pitcher}',ABs, '-',hits,HRs,RBIs,BBs,SOs, '-',AVG,OBP,SLG]
        player_splits.loc[3] = bvp_hitory


def get_PitcherHistory(opp_pitcher_id,team_id):
    new_url = f'http://www.espn.com/mlb/player/batvspitch/_/id/{opp_pitcher_id}/teamId/{team_id}'
    df = get_pitcher_splits(new_url)
    return df


def get_opp_pitch_url(opp_pitcher,pitcher_db):
    url = pitcher_db.loc[opp_pitcher][-1]
    if url: return url


def get_player_id(url):
    id = [ch for ch in url if ch.isdigit()] # parse url for digits
    id = ''.join(id) # join digits
    return id


# discard players with undersirable stats or insufficient data
def filter_players(lineup_splits):
    for player, splits in list(lineup_splits):
        last_7 = splits.iloc[0,:]

        vsPitcherAB = None
        vsPitcherAvg = None
        last_row = splits.iloc[-1,:] # get last row in splits

        if (float(last_7[9]) < .250): # check Avg over last7
            lineup_splits.remove((player,splits)) # undersirable stats
            continue
        if f'vs' in last_row[0]: # check for history vs pitcher
            pitcher_splits = last_row
            vsPitcherAB = int(pitcher_splits[1]) # get vsPitcherABs
            vsPitcherAvg = float(pitcher_splits[9]) # get vsPitcherAvg
            if (vsPitcherAvg < .250) or (vsPitcherAB < 5): # undersirable stats or sample size to small
                lineup_splits.remove((player,splits))

    return lineup_splits


# calculate weightedAvg using splits
def get_weightedAvg(lineup_splits):
    hitters = []
    for player, splits in lineup_splits:
        AVGs = [float(splits.iloc[i,9]) for i in range(len(splits))]
        weightedAvg = (sum(AVGs)/len(AVGs))
        if weightedAvg > .265:
            hitters.append((player,weightedAvg))

    return hitters

if __name__ == "__main__":
    main()
