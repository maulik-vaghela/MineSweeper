"""
This module defines the API related to leaderboard handling.
"""

import os
from BoardEnums import DifficultyLevel

def insertnewscore(level, player_name, score):
    """
    This function will store score (along with other details such as rank and name) in a file,
    corresponding to selected game level, stored at persistent memory.
    This function will take care of storing information in sorted order based on score,
    High score->Low score
    :param DifficultyLevel: Beginner/Intermediate/Expert
    :param player_name: Player name
    :param score: Score in seconds for the player
    :return: None
    """
    index = 0
    file_name = ""
    if level == DifficultyLevel.BeginnerLevel:
        file_name = "Beginner.txt"
    elif level == DifficultyLevel.IntermediateLevel:
        file_name = "Intermediate.txt"
    elif level == DifficultyLevel.ExpertLevel:
        file_name = "Expert.txt"
    else:
        print "Exception"
        return
    file_handle = open(file_name, "a+")
    file_data = file_handle.readlines()
    file_handle.close()

    if file_data == []:
        # if currently no data in file, insert new data as the first data at position 1
        file_data.insert(0, "1" + '\t' + player_name + "\t" + str(score) + '\n')
    else:
        # find the correct position for new data based on score.
        # Insert new data at its correct position
        for data in file_data:
            index = index + 1
            if score > data.split('\t')[2]:
                file_data.insert(index - 1, str(index) + '\t' + player_name\
                                 + "\t" + str(score) + '\n')
                break
        else:
            # Add the score at the end
            file_data.insert(index, str(index + 1) + '\t' + player_name\
                             + "\t" + str(score) + '\n')

    # Write all data back in file
    file_handle = open(file_name, "w+")

    # Variable to keep track of rank/order while writing data back in file
    rank = 1
    for data in file_data:
        # create list to write back data in file.
        # We want to re-write first column data based on rank calculated here.
        file_handle.write(data)
        rank = rank + 1
        if rank > 10:
            break
    file_handle.close()

def gettopscorerslist(level):
    """
    This function will retrieve scores for selected game level and will display these scores to user
    :param level: Level of game (Beginner, Intermediate, Expert) for which score is required
    :return: The list of top scores for input level
    """
    file_name = ""
    top_scores = []
    if level == DifficultyLevel.ExpertLevel:
        file_name = "Expert.txt"
    elif level == DifficultyLevel.IntermediateLevel:
        file_name = "Intermediate.txt"
    elif level == DifficultyLevel.BeginnerLevel:
        file_name = "Beginner.txt"
    else:
        return top_scores

    file_existence = os.path.exists(file_name)

    # If file does not exist return empty list
    if file_existence is False:
        return top_scores

    file_handle = open(file_name, "r+")
    top_scores = file_handle.readlines()
    file_handle.close()

    return top_scores
