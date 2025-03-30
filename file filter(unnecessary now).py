"""This file reads user data and creates a mapping to othe ruser characteristics"""

import pandas as pd
# import pickle
import os
import random


def create_user_data_file(platform: str) -> dict[int, dict[str, str | int | list]]:
    """Creates and returns user data as a complex dictionary"""
    random.seed(1234)
    """function generates a dicitonary object with user attributes from a specific platform"""
    valid_players = set()
    player_info = pd.read_csv(f"archive/{platform}/players.csv")
    game_info = pd.read_csv(f"archive/{platform}/purchased_games.csv")
    achieve_info = pd.read_csv(f"archive/{platform}/history.csv")

    player_dict = player_info.set_index('playerid').to_dict(orient='index')
    game_dict = game_info.set_index('playerid').to_dict(orient='index')
    achieve_dict = achieve_info.groupby('playerid')['achievementid'].apply(list).to_dict()

    for player in player_dict.keys():
        if player in game_dict:
            if player in achieve_dict:
                if game_dict[player]["library"] != [] and achieve_dict[player] != []:
                    valid_players.add(player)

    valid_players = set(random.sample(list(valid_players), 1000))

    # Filter the DataFrame to keep only the specified player IDs
    filtered_players = player_info[player_info['playerid'].isin(valid_players)]
    filtered_games = game_info[game_info['playerid'].isin(valid_players)]
    filtered_achieve = achieve_info[achieve_info['playerid'].isin(valid_players)]

    os.makedirs(platform, exist_ok=True)

    # Save the filtered DataFrame to a new CSV file
    filtered_players.to_csv(f'{platform}/players.csv', index=False)
    filtered_games.to_csv(f'{platform}/purchased_games.csv', index=False)
    filtered_achieve.to_csv(f'{platform}/history.csv', index=False)

    return player_dict


if __name__ == "__main__":
    for i in ["playstation", "steam", "xbox"]:
        print("starting ", i)
        create_user_data_file(i)
        print("finished ", i)

