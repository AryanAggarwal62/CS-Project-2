"""This file reads user data and creates a mapping to othe ruser characteristics"""

import pandas as pd
import pickle
import os


def get_user_data_file(platform: str, mode: str = "save_state") -> dict[int, dict[str, str | set[int] | list[str]]]:
    """function generates a dicitonary object with user attributes from a specific platform"""

    if mode == "save_state":
        with open(f"{platform}/processed_player_data.pkl", "rb") as f:
            player_dict = pickle.load(f)
    else:
        player_info = pd.read_csv(f"{platform}/players.csv")
        game_info = pd.read_csv(f"{platform}/purchased_games.csv")
        achieve_info = pd.read_csv(f"{platform}/history.csv")

        player_dict = player_info.set_index('playerid').to_dict(orient='index')
        game_dict = game_info.set_index('playerid').to_dict(orient='index')
        achieve_dict = achieve_info.groupby('playerid')['achievementid'].apply(list).to_dict()

        for player in player_dict.keys():
            # add game libarary to player id
            if player in game_dict:
                player_dict[player]["library"] = set(eval(game_dict[player]["library"]))
            else:
                player_dict[player]["library"] = []

            # add achievement data to player id
            # modified_achievement_dict = {}
            #
            # for i in achieve_dict[player]:
            #     game = i.split("_")[0]
            #     if game not in modified_achievement_dict:
            #         modified_achievement_dict[game] = 1
            #     else:
            #         modified_achievement_dict[game] += 1

            if player in achieve_dict:
                player_dict[player]["achievements"] = set(achieve_dict[player])
            else:
                player_dict[player]["achievements"] = []

        os.makedirs(platform, exist_ok=True)  # Ensure platform folder exists
        pickle_file = os.path.join(platform, "processed_player_data.pkl")

        # Save the dictionary to a file
        with open(pickle_file, "wb") as f:
            pickle.dump(player_dict, f)

    return player_dict


if __name__ == "__main__":
    for i in ["playstation", "xbox", "steam"]:
        get_user_data_file(i, "generate")
        print(i)





#181212: {'nickname': 'WRARHD', 'country': 'United States', 'library': {32, 3726}, 'achievements': {'32': 0}}}
#181212: {'nickname': 'WRARHD', 'country': 'United States', 'library': [32, 3726], 'achievements': ['32_3794']}}
