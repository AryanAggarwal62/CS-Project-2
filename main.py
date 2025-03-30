"""This file calls the graph classes in generate_graph to create graphs"""

from typing import Any
from file_parsing import get_user_data_file
from generate_graph import WeightedGraph
import pickle
import time

# Provided a userid, find the corresponding user node in the graph

# after finding the user node, return the players the user has the most in common with

# CLUSTERING
#


def get_weight(user_1: Any, user_2: Any, data: dict[int, dict], prefs: dict[str, float]) -> float:
    """ Return the weight between two nodes(user_1 and user_2) in a graph (data) by calculating
    their similarity and scaling by user preferences in prefs

    #TODO Doctests

    #TODO Precondtions
        -

    """
    if user_1 in data and user_2 in data:

        # getting game_similarity as a preference
        similar_games = data[user_1]["library"].intersection(data[user_2]["library"])
        all_games = data[user_1]["library"].union(data[user_2]["library"])
        game_similarity = prefs["library"] * (len(similar_games)/len(all_games))

        # getting achievement similarity for similar games
        similar_achevs = data[user_1]["achievements"].intersection(data[user_2]["achievements"])
        all_achevs = data[user_1]["achievements"].union(data[user_2]["achievements"])
        achievement_similarity = prefs["achievements"] * (len(similar_achevs) / len(all_achevs))

        # 3. Final weight calculation
        return game_similarity + achievement_similarity

    else:
        raise NameError


def main(platform):
    """main function to run graph generation"""
    # TODO add the necessary pygame elements
    mode = "save_state"  # -----------------add pygame option selection
    # platform = "playstation" # -----------add pygame option selection
    playerid = "371169"  # -----------------add pygame option selection
    prefs = {"library": 1, "achievements": 1}

    if mode != "save_state":
        platform_graph = WeightedGraph()
        # generating the platform data
        user_data = get_user_data_file(platform, mode)

        # adding player vertices to the graph
        for user in user_data.keys():
            platform_graph.add_vertex(user)

        # adding edges between players
        for user_1 in user_data.keys():
            for user_2 in user_data.keys():
                if user_1 != user_2 and not platform_graph.check_connected(user_1, user_2):

                    weight = get_weight(user_1, user_2, user_data, prefs)
                    platform_graph.add_edge(user_1, user_2, weight)
    else:
        with open(f'{platform}/platform_graph.pkl', 'rb') as graph:
            platform_graph = pickle.load(graph)

    return platform_graph


if __name__ == "__main__":
    print(main("playstation").cluster())
