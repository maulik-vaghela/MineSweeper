#__author__ = 'schellu'
from random import *
from BoardEnums import *

class Board:
    def __init__(self, rows, columns, minecount):
        self.Rows = rows
        self.Columns = columns
        self.TotalMineCount = minecount
        self.CurrentMineCount = self.TotalMineCount
        self.LastClickedRow = -1
        self.LastClickedColumn = -1
        """
        CellState -
        -1: Undefined Status
        0: Closed
        1: Opened
        2: Marked as mine
        3: Marked as suspected mine
        """
        self.CellStatus = [[CellStatus.UndefinedStatus \
                            for x in range(columns)] for x in range(rows)]
        """
        CellProperty -
        -2: UndefinedProperty
        -1: Mine
        0: Empty
        1-8: AdjacentMineCount
        """
        self.CellProperty = [[CellProperty.UndefinedProperty \
                              for x in range(columns)] for x in range(rows)]
        self.CreateBoard()

    def CreateBoard(self):
        #initialize the Board status and property with Closed and Empty resp.
        for row in range(self.Rows):
            for column in range(self.Columns):
                self.CellStatus[row][column] = CellStatus.Closed
                self.CellProperty[row][column] = CellProperty.Empty

        #Use random sample function to get a position list to place mines randomly
        minelist = sample(range(self.Rows * self.Columns), self.TotalMineCount)
        #remove
        print minelist

        #Update the Cell Property based on the mine list in the board
        for i in range(self.TotalMineCount):
            row = minelist[i] / self.Columns
            column = minelist[i] % self.Columns
            self.CellProperty[row][column] = CellProperty.Mine

        #Update Adjacent Count in neighboruing cells of a cell which has mines
        for i in range(self.TotalMineCount):
            row = minelist[i] / self.Columns
            column = minelist[i] % self.Columns
            if (row-1 >= 0) and (column-1 >= 0):
                if self.CellProperty[row-1][column-1] != CellProperty.Mine:
                    self.CellProperty[row-1][column-1] += 1
            if row-1 >= 0:
                if self.CellProperty[row-1][column] != CellProperty.Mine:
                    self.CellProperty[row-1][column] += 1
            if (row-1 >= 0) and (column+1 < self.Columns):
                if self.CellProperty[row-1][column+1] != CellProperty.Mine:
                    self.CellProperty[row-1][column+1] += 1
            if column+1 < self.Columns:
                if self.CellProperty[row][column+1] != CellProperty.Mine:
                    self.CellProperty[row][column+1] += 1
            if (row+1 < self.Rows) and (column+1 < self.Columns):
                if self.CellProperty[row+1][column+1] != CellProperty.Mine:
                    self.CellProperty[row+1][column+1] += 1
            if row+1 < self.Rows:
                if self.CellProperty[row+1][column] != CellProperty.Mine:
                    self.CellProperty[row+1][column] += 1
            if (row+1 < self.Rows) and (column-1 >= 0):
                if self.CellProperty[row+1][column-1] != CellProperty.Mine:
                    self.CellProperty[row+1][column-1] += 1
            if column-1 >= 0:
                if self.CellProperty[row][column-1] != CellProperty.Mine:
                    self.CellProperty[row][column-1] += 1

        #remove
        for i in range(self.Rows):
            print self.CellProperty[i]
        return

    def OpenCell(self, row, column, CellList):
        '''
        :param row:
        :param column:
        :return: List of cells to be opened
        '''
        if (row < 0) or (row >= self.Rows) or (column < 0) or (column >= self.Columns):
            return

        #if cell status is already opened or suspected mine it can not be opened??
        if (self.CellStatus[row][column] == CellStatus.Opened) or \
            (self.CellStatus[row][column] == CellStatus.MarkedAsMine):
            return

        #set the Cell Status to Opened and add it to CellList to be returned
        self.CellStatus[row][column] = CellStatus.Opened
        CellList.append([row, column])

        #Cache the Clicked cell here
        if len(CellList) == 1:
            self.LastClickedRow = CellList[0][0]
            self.LastClickedColumn = CellList[0][1]

        '''
        if a cell is empty we should open all the 8 neighbours of the
        clicked cell if they are not already open or marked as mine.
        This rule applies recursively to neighbour cells if they are also empty.
        '''
        if self.CellProperty[row][column] == CellProperty.Empty:
            if (row-1 >= 0) and (column-1 >= 0):
                self.OpenCell(row-1, column-1, CellList)
            if row-1 >= 0:
                self.OpenCell(row-1, column, CellList)
            if (row-1 >= 0) and (column+1 < self.Columns):
                self.OpenCell(row-1, column+1, CellList)
            if column+1 < self.Columns:
                self.OpenCell(row, column+1, CellList)
            if (row+1 < self.Rows) and (column+1 < self.Columns):
                self.OpenCell(row+1, column+1, CellList)
            if column-1 >= 0:
                self.OpenCell(row, column-1, CellList)
            if row+1 < self.Rows:
                self.OpenCell(row+1, column, CellList)
            if (row+1 < self.Rows) and (column-1 >= 0):
                self.OpenCell(row+1, column-1, CellList)

    def SetCellStatus(self, row, column, status):
        if (row < 0) or (row >= self.Rows) or (column < 0) or (column >= self.Columns):
            return CellStatus.UndefinedStatus

        #for MarkedAsMine cell the valid state is only MarkedAsSuspectedMine
        if self.CellStatus[row][column] == CellStatus.MarkedAsMine:
            if status != CellStatus.MarkedAsSuspectedMine:
                return CellStatus.UndefinedStatus

        #for MarkedAsSuspectedMine cell the valid states are Open or close
        if self.CellStatus[row][column] == CellStatus.MarkedAsSuspectedMine:
            if not((status == CellStatus.Closed) or (status == CellStatus.Opened)):
                return CellStatus.UndefinedStatus

        #if Status that going to set is MarkedAsMine then the earlier state of cell should be Closed
        if status == CellStatus.MarkedAsMine:
            if self.CellStatus[row][column] != CellStatus.Closed:
                return CellStatus.UndefinedStatus

        #set the New cell status
        self.CellStatus[row][column] == status

        #increase or decrease current mine count based on New Set Status
        if status == CellStatus.MarkedAsMine:
            self.CurrentMineCount = self.CurrentMineCount + 1
        elif status == CellStatus.MarkedAsSuspectedMine:
            self.CurrentMineCount = self.CurrentMineCount - 1

        return status

    def GetCellStatus(self, row, column):
        if (row < 0) or (row >= self.Rows) or (column < 0) or (column >= self.Columns):
            return CellStatus.UndefinedStatus
        return self.CellStatus[row][column]

    def GetCellProperty(self, row, column):
        if (row < 0) or (row >= self.Rows) or (column < 0) or (column >= self.Columns):
            return CellProperty.UndefinedProperty

        return self.CellProperty[row][column]

    def ContinueGame(self):
        if (self.LastClickedRow == -1) and (self.LastClickedColumn == -1):
            return GameStatus.GameNotComplete

        if self.CellProperty[self.LastClickedRow][self.LastClickedColumn] == CellProperty.Mine:
            return GameStatus.GameLost

        if self.CurrentMineCount != 0:
            return GameStatus.GameNotComplete
        else:
            #if currentminecount is zero, then Game is not complete until all cells are opened
            for row in range(self.Rows):
                for col in range(self.Columns):
                    if self.CellStatus[row][col] == CellStatus.Closed:
                        return GameStatus.GameNotComplete

        return GameStatus.GameWon

    def Reset(self):
        self.CurrentMineCount = self.TotalMineCount
        self.LastClickedRow = -1
        self.LastClickedColumn = -1
        self.CreateBoard()
        return