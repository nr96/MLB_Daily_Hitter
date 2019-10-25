from ESPN_Regular_Season import get_last7db
from ESPN_Pitcher_Stats import get_espn_pitchers
from Player_Splits import get_player_splits

from MLB_Player_Cards import get_player_card
from ESPN_BvP import get_pitcher_splits, get_team_id
from MLB_Lineups import get_lineups_df
import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="use's test lineup instead of live lineup", action='store_true')
    args = parser.parse_args()
    load_dbs(args)

def load_dbs(args):
    print("Loading DB's...")
    pitcher_db = get_espn_pitchers()
    #last7_df = get_last7db()
    if args.test:
        print("Using Test Lineup")
        #lineups_df = pd.read_excel('MLB_lineups.xlsx')
        lineups_df = get_lineups_df()
        get_hitters_test(lineups_df,pitcher_db)
    else:
        lineups_df = get_lineups_df()
        #get_hitters(lineups_df,last7_df)


def get_hitters_test(lineups_df,pitcher_db):
    print("Running Algorithm...")
    lineup_splits = get_lineup_splits_test(lineups_df,pitcher_db)
    #lineup_splits = pd.read_excel('output.xlsx')
    #print(lineup_splits)
    players = filter_players_test(lineup_splits)
    hitters = get_weightedAvg_test(players)
    hitters.sort(key=lambda player: player[1], reverse=True)

    if len(hitters):
        print("\nMost Likely Hitters")
        for i, player in enumerate(hitters,0):
            print(f"{i+1}. {player[0]}, weightedAvg: {player[1]}")
    else:
        print('No desirable hitters')

def get_hitters(lineups_df,last7_df):
    print("Running Algorithm...")
    lineup_splits = get_lineup_splits(lineups_df,last7_df)
    #print(lineup_splits)
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
def get_lineup_splits(lineups_df, last7_df):
    lineup_splits = []
    for i, player in enumerate(lineups_df.iloc[:,0]):
        opp_picther = lineups_df.iloc[i,4]
        player_info = get_player_info(last7_df,player)
        if player_info: # player_info will be NoneType if not in last7_df
             splits = get_player_splits(player_info[3])
             player_info.append(opp_picther)
             lineup_splits.append([player_info,splits])
    return lineup_splits


def get_lineup_splits_test(lineups_df,pitcher_db):
    lineup_splits = []
    last_pitcher = ''
    last_pitcher_df = None
    pitcher_db.set_index('PLAYER',inplace=True)

    print(f"Loading Splits....")
    for index, player in lineups_df.iterrows():
        name = player[0]
        team = player[1]
        opp_team = player[3]
        opp_pitcher = player[4]
        opp_pitcher_hand = player[5]
        player_link = player[6]

        #print(f"Loading {name} card....")
        player_splits = get_player_card(player_link)

        if last_pitcher != opp_pitcher: # cache opp_pitcher info
            last_pitcher = opp_pitcher
            last_pitch_url = get_opp_pitch_url(opp_pitcher,pitcher_db)
            team_id = get_team_id(team)
            opp_pitcher_id = get_player_id(last_pitch_url)
            last_pitcher_df = get_PitcherHistory(opp_pitcher_id,team_id)

        for index,player_faced in last_pitcher_df.iterrows(): # get BvP History
            get_BvP(player_splits,player_faced,name,opp_pitcher)

        lineup_splits.append((name,player_splits))


        #headers = player_splits.columns
    #lineup_splits.to_excel('splits.xlsx')
    #build_xlsx(lineup_splits,headers)
    #pd.DataFrame(lineup_splits).to_excel('output.xlsx', header=['Name, Splits'], index=False)
    return lineup_splits

# def build_xlsx(lineup_splits, headers):
#     rows = []
#     headers = ['Name', 'Splits'] + headers
#     for name, splits in lineup_splits:
#         for split in splits:
#             rows.append([name,split])
#     print(rows[0])

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
    #print(new_url)
    df = get_pitcher_splits(new_url)
    return(df)

def get_opp_pitch_url(opp_pitcher,pitcher_db):
    #print(pitcher_db)
    url = pitcher_db.loc[opp_pitcher][-1]
    if url: return(url)

def get_player_id(url):
    id = [ch for ch in url if ch.isdigit()]
    id = ''.join(id)
    return(id)

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


def filter_players_test(lineup_splits):
    for player, splits in list(lineup_splits):
        last_7 = splits.iloc[0,:]

        vsPitcherAB = None
        vsPitcherAvg = None
        last_row = splits.iloc[-1,:]

        if (float(last_7[9]) < .250): # not enough info
            #print(f"removing {player} AVG:{last_7[9]}...1")
            lineup_splits.remove((player,splits)) # if not PitcherHistory discard player
            continue
        if f'vs' in last_row[0]:
            pitcher_splits = last_row
            vsPitcherAB = int(pitcher_splits[1])
            vsPitcherAvg = float(pitcher_splits[9])
            if (vsPitcherAvg < .250) or (vsPitcherAB < 5): # undersirable stats or sample size to small
                #print(f"removing {player} AVG:{vsPitcherAvg} AB:{vsPitcherAB} ...2")
                lineup_splits.remove((player,splits))

    return lineup_splits


def get_weightedAvg_test(lineup_splits):
    hitters = []
    for player, splits in lineup_splits:
        AVGs = [float(splits.iloc[i,9]) for i in range(len(splits))]
        weightedAvg = (sum(AVGs)/len(AVGs))
        if weightedAvg > .265:
            hitters.append((player,weightedAvg))

    return hitters


# use last7GamesAvg and vsPitcherAvg to calculate weightedAvg
def get_weightedAvg(lineup_splits):
    for i, player in enumerate(lineup_splits, 0):
        pitcher_splits =  player[1].iloc[-1,:]
        last7Avg = player[0][2]
        vsPitcherAvg = float(pitcher_splits[9])
        #print(player[0][0],last7Avg, vsPitcherAvg)
        weightedAvg = ((last7Avg + vsPitcherAvg)/2)
        player.append(weightedAvg)

# get player info [name, ABs, AVG, player_url] from last7db
def get_player_info(last7_df, player_name):
    if player_name[1] == '.': first_name, last_name = player_name.split('. ')
    else: first_name, last_name = player_name.split()
    #print(player_name)
    for i, player in enumerate(last7_df.iloc[:, 0], 0):  # search player names in last7_df
        if player_name == player or (last_name in player and first_name[0] == player[0]):
            AB = int(last7_df.iloc[i, 2])
            AVG = float(last7_df.iloc[i, 13])
            player_url = last7_df.iloc[i, 17]  # if names match, return url

            if AVG > .250 and AB > 10: # undersirable stats or sample size to small
                return [player,AB,AVG,player_url]

if __name__ == "__main__":
    main()
