__author__ = 'kumarabh'

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

class LeaderBoard:

     def storeScore(self, scoreDict):
         """
         This function will store score (along with other details such as rank and name) in a file, corresponding to selected game level, stored at persistent memory.
         This function will take care of storing information in sorted order based on score, High score->Low score
         :param scoreDict: a Dictionary in form of {'Level':'', 'Name':'', 'Score':''} Eg; {'Level':'Expert', 'Name':'Ak', 'Score':'20'}
         :return: Save information in a file corresponding to selected game level (Beginner.txt OR Intermediate.txt OR Expert.txt)
         """
         index = 0
         dataInserted = 0
         fileObj = open(scoreDict['Level']+".txt", "a+")
         fileData = fileObj.readlines()
         fileObj.close()

         if fileData == []:
            #if currently no data in file, insert new data as the first data at position 1
             fileData.insert(0, "1"+'\t'+scoreDict['Name']+"\t"+scoreDict['Score']+"\n")
         else:
             #find the correct position for new data based on score. Insert new data at its correct position
             for data in fileData:
                 index = index+1
                 if(scoreDict['Score'] > data.split()[2]):
                     dataInserted = 1
                     fileData.insert(index-1, str(index)+'\t'+scoreDict['Name']+"\t"+scoreDict['Score']+"\n")
                     break

             if(dataInserted == 0):
                 #if reach at the end of list and still new data left to be added, simply append new data at the end of list
                 fileData.append(str(index+1)+'\t'+scoreDict['Name']+"\t"+scoreDict['Score']+"\n")

         #Write all data back in file
         fileObj = open(scoreDict['Level']+".txt", "w+")
         rank = 1 #Variable to keep track of rank/order while writing data back in file
         for data in fileData:
            #create list to writeback data in file. We want to re-write first column data based on rank calculated here
             list = data.split()
             fileObj.write(str(rank)+'\t'+list[1]+"\t"+list[2]+"\n")
             rank = rank+1
         fileObj.close()

     def readScore(self, level):
        """
        This function will retrieve scores for selected game level and will display these scores to user
        :param level: Level of game (Beginner, Intermediate, Expert) for which score is required
        :return: UI containing information of rank, name and score
        """
        fileObj  = open(level+".txt", "r+")
        fileData = fileObj.read()
        fileObj.close()

        win  = QtGui.QWidget()

        info_layout = QtGui.QHBoxLayout()
        info_layout.addWidget(QtGui.QLabel("<b>"+ str(level) + " Level Ranking and Scores</b>"+"<br>"))

        score_layout = QtGui.QGridLayout()
        score_layout.addWidget(QtGui.QLabel(fileData), 0, 0)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(info_layout)
        main_layout.addLayout(score_layout)

        win.setLayout(main_layout)
        win.setGeometry(100,100,200,100)
        win.setWindowTitle("Leader Board")
        win.show()
