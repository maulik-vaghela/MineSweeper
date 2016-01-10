"""
This module defines the API related to leaderboard handling.
"""

import os
import sys

import Minesweeper

class LeaderBoard(object):
    """
    Class for managing the scores
    """
    ScoreFileDict = {Minesweeper.GameLevel.Beginner: "Beginner.txt", \
                    Minesweeper.GameLevel.Intermediate: "Intermediate.txt", \
                    Minesweeper.GameLevel.Expert: "Expert.txt"
                    }

    def __init__(self):
        pass


    def insertnewscore(self, level, player_name, score):
        """
        This function will store score (along with other details such as rank and name) in a file,
        corresponding to selected game level in descending order of scores

        :param Level: Beginner/Intermediate/Expert
        :param player_name: Player name
        :param score: Score in seconds for the player
        :return: None
        """
        index = 0

        file_name = LeaderBoard.ScoreFileDict[level]
        file_handle = open(file_name, "a+")
        file_data = file_handle.readlines()
        file_handle.close()

        line_to_add = str(player_name).ljust(30) + str(score).ljust(10) + '\n'

        if file_data == []:
            # if currently no data in file, insert new data as the first data
            # at position 1
            file_data.insert(0, line_to_add)
        else:
            # find the correct position for new data based on score.
            # Insert new data at its correct position
            for data in file_data:
                index = index + 1
                temp_score = int(data.split()[len(data.split()) - 1])
                if score < temp_score:
                    file_data.insert(index - 1, line_to_add)
                    break
            else:
                # Add the score at the end
                file_data.append(line_to_add)

        # Write all data back in file
        file_handle = open(file_name, "w+")

        # Variable to keep track of rank/order while writing data back in file
        rank = 1
        for data in file_data:
            # create list to write back data in file.
            # We want to re-write first column data based on rank calculated
            # here.
            file_handle.write(data)
            rank = rank + 1
            if rank > 10:
                break
        file_handle.close()

    def gettopscorerslist(self, level):
        """
        This function will retrieve scores for selected game level and will display these scores to user
        :param level: Level of game (Beginner, Intermediate, Expert) for which score is required
        :return: The list of top scores for input level
        """
        file_name = ""
        top_scores = []
        file_name = LeaderBoard.ScoreFileDict[level]
        file_existence = os.path.exists(file_name)

        # If file does not exist return empty list
        if file_existence is False:
            return top_scores

        file_handle = open(file_name, "r+")
        top_scores = file_handle.readlines()
        file_handle.close()

        return top_scores

def main():
    pass

if __name__ == "__main__":
    sys.exit(int(main() or 0))
