#__author__ = 'schellu'
from random import *
from BoardEnums import *

class Board:
    def __init__(self, rows, columns, minecount):
        self.rows = rows
        self.columns = columns
        self.total_mine_count = minecount
        self.current_mine_count = self.total_mine_count
        self.last_clicked_row = -1
        self.last_clicked_column = -1
        """
        CellState -
        -1: Undefined Status
        0: Closed
        1: Opened
        2: Marked as mine
        3: Marked as suspected mine
        """
        self.cell_status = [[CellStatus.UndefinedStatus \
                            for x in range(columns)] for x in range(rows)]
        """
        CellProperty -
        -2: UndefinedProperty
        -1: Mine
        0: Empty
        1-8: AdjacentMineCount
        """
        self.cell_property = [[CellProperty.UndefinedProperty \
                              for x in range(columns)] for x in range(rows)]
        self.createboard()

    def createboard(self):
        #initialize the Board status and property with Closed and Empty resp.
        for row in range(self.rows):
            for column in range(self.columns):
                self.cell_status[row][column] = CellStatus.Closed
                self.cell_property[row][column] = CellProperty.Empty

        #Use random sample function to get a position list to place mines randomly
        minelist = sample(range(self.rows * self.columns), self.total_mine_count)
        #remove
        print minelist

        #Update the Cell Property based on the mine list in the board
        for i in range(self.total_mine_count):
            row = minelist[i] / self.columns
            column = minelist[i] % self.columns
            self.cell_property[row][column] = CellProperty.Mine

        #Update Adjacent Count in neighboruing cells of a cell which has mines
        for i in range(self.total_mine_count):
            row = minelist[i] / self.columns
            column = minelist[i] % self.columns
            if (row-1 >= 0) and (column-1 >= 0):
                if self.cell_property[row-1][column-1] != CellProperty.Mine:
                    self.cell_property[row-1][column-1] += 1
            if row-1 >= 0:
                if self.cell_property[row-1][column] != CellProperty.Mine:
                    self.cell_property[row-1][column] += 1
            if (row-1 >= 0) and (column+1 < self.columns):
                if self.cell_property[row-1][column+1] != CellProperty.Mine:
                    self.cell_property[row-1][column+1] += 1
            if column+1 < self.columns:
                if self.cell_property[row][column+1] != CellProperty.Mine:
                    self.cell_property[row][column+1] += 1
            if (row+1 < self.rows) and (column+1 < self.columns):
                if self.cell_property[row+1][column+1] != CellProperty.Mine:
                    self.cell_property[row+1][column+1] += 1
            if row+1 < self.rows:
                if self.cell_property[row+1][column] != CellProperty.Mine:
                    self.cell_property[row+1][column] += 1
            if (row+1 < self.rows) and (column-1 >= 0):
                if self.cell_property[row+1][column-1] != CellProperty.Mine:
                    self.cell_property[row+1][column-1] += 1
            if column-1 >= 0:
                if self.cell_property[row][column-1] != CellProperty.Mine:
                    self.cell_property[row][column-1] += 1

        #remove
        for i in range(self.rows):
            print self.cell_property[i]
        return

    def opencell(self, row, column, cell_list):
        '''
        :param row:
        :param column:
        :return: List of cells to be opened
        '''
        if (row < 0) or (row >= self.rows) or (column < 0) or (column >= self.columns):
            return

        #if cell status is already opened or suspected mine it can not be opened??
        if (self.cell_status[row][column] == CellStatus.Opened) or \
            (self.cell_status[row][column] == CellStatus.MarkedAsMine):
            return

        #set the Cell Status to Opened and add it to CellList to be returned
        self.cell_status[row][column] = CellStatus.Opened
        cell_list.append([row, column])

        #Cache the Clicked cell here
        if len(cell_list) == 1:
            self.last_clicked_row = cell_list[0][0]
            self.last_clicked_column = cell_list[0][1]

        '''
        if a cell is empty we should open all the 8 neighbours of the
        clicked cell if they are not already open or marked as mine.
        This rule applies recursively to neighbour cells if they are also empty.
        '''
        if self.cell_property[row][column] == CellProperty.Empty:
            if (row-1 >= 0) and (column-1 >= 0):
                self.opencell(row-1, column-1, cell_list)
            if row-1 >= 0:
                self.opencell(row-1, column, cell_list)
            if (row-1 >= 0) and (column+1 < self.columns):
                self.opencell(row-1, column+1, cell_list)
            if column+1 < self.columns:
                self.opencell(row, column+1, cell_list)
            if (row+1 < self.rows) and (column+1 < self.columns):
                self.opencell(row+1, column+1, cell_list)
            if column-1 >= 0:
                self.opencell(row, column-1, cell_list)
            if row+1 < self.rows:
                self.opencell(row+1, column, cell_list)
            if (row+1 < self.rows) and (column-1 >= 0):
                self.opencell(row+1, column-1, cell_list)

    def setcellstatus(self, row, column, status):
        if (row < 0) or (row >= self.rows) or (column < 0) or (column >= self.columns):
            return CellStatus.UndefinedStatus

        #for MarkedAsMine cell the valid state is only MarkedAsSuspectedMine
        if self.cell_status[row][column] == CellStatus.MarkedAsMine:
            if status != CellStatus.MarkedAsSuspectedMine:
                return CellStatus.UndefinedStatus

        #for MarkedAsSuspectedMine cell the valid states are Open or close
        if self.cell_status[row][column] == CellStatus.MarkedAsSuspectedMine:
            if not((status == CellStatus.Closed) or (status == CellStatus.Opened)):
                return CellStatus.UndefinedStatus

        #if Status that going to set is MarkedAsMine then the earlier state of cell should be Closed
        if status == CellStatus.MarkedAsMine:
            if self.cell_status[row][column] != CellStatus.Closed:
                return CellStatus.UndefinedStatus

        #set the New cell status
        self.cell_status[row][column] = status

        #increase or decrease current mine count based on New Set Status
        if status == CellStatus.MarkedAsMine:
            self.current_mine_count = self.current_mine_count + 1
        elif status == CellStatus.MarkedAsSuspectedMine:
            self.current_mine_count = self.current_mine_count - 1

        return status

    def getcellstatus(self, row, column):
        if (row < 0) or (row >= self.rows) or (column < 0) or (column >= self.columns):
            return CellStatus.UndefinedStatus
        return self.cell_status[row][column]

    def getcellproperty(self, row, column):
        if (row < 0) or (row >= self.rows) or (column < 0) or (column >= self.columns):
            return CellProperty.UndefinedProperty

        return self.cell_property[row][column]

    def continuegame(self):
        if (self.last_clicked_row == -1) and (self.last_clicked_column == -1):
            return GameStatus.GameNotComplete

        if self.cell_property[self.last_clicked_row][self.last_clicked_column] == CellProperty.Mine:
            return GameStatus.GameLost

        if self.current_mine_count != 0:
            return GameStatus.GameNotComplete
        else:
            #if currentminecount is zero, then Game is not complete until all cells are opened
            for row in range(self.rows):
                for col in range(self.columns):
                    if self.cell_status[row][col] == CellStatus.Closed:
                        return GameStatus.GameNotComplete

        return GameStatus.GameWon

    def reset(self):
        self.current_mine_count = self.total_mine_count
        self.last_clicked_row = -1
        self.last_clicked_column = -1
        self.createboard()
        return