"""
This module implements the Board class for minesweeper implementation.
"""

from random import sample
from BoardEnums import CellProperty, CellStatus, GameStatus

class Board(object):
    """
    This is the core Board class as per the class diagram
    """
    def __init__(self, rows, columns, mine_count):
        """
        This is the constructor.
        :param rows: Grid rows
        :param columns: Grid columns
        :param mine_count: Mines to be placed
        :return: None
        """
        self.rows = rows
        self.columns = columns
        self.total_mine_count = mine_count
        self.current_mine_count = self.total_mine_count
        self.last_clicked_row = -1
        self.last_clicked_column = -1

        # Initialize the cell status to undefined.
        self.cell_status = []
        for row in range(rows):
            self.cell_status.append([CellStatus.UndefinedStatus \
                                     for column in range(columns)])

        # Initialize the cell property to undefined.
        self.cell_property = []
        for row in range(rows):
            self.cell_property.append([CellProperty.UndefinedProperty \
                                       for column in range(columns)])
        self.createboard()

    def createboard(self):
        """
        Initialize the Board status and property with Closed and Empty resp.
        :return: None
        """
        for row in range(self.rows):
            for column in range(self.columns):
                self.cell_status[row][column] = CellStatus.Closed
                self.cell_property[row][column] = CellProperty.Empty

        # Use random sample function to get a position list to place mines randomly
        mine_list = sample(range(self.rows * self.columns), self.total_mine_count)

        # Update the Cell Property based on the mine list in the board
        for i in range(self.total_mine_count):
            row = mine_list[i] // self.columns
            column = mine_list[i] % self.columns
            self.cell_property[row][column] = CellProperty.Mine

        # Update Adjacent Count in neighboruing cells of a cell which has mines
        for i in range(self.total_mine_count):
            row = mine_list[i] // self.columns
            column = mine_list[i] % self.columns
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
        return

    def opencell(self, row, column):
        """
        Open the input cell and return list of affected cells.
        :param row: Row of the cell
        :param column: Column of the cell
        :return: List of cells affected and to be updated
        """
        cell_list = []
        if (row < 0) or (row >= self.rows) or (column < 0) or (column >= self.columns):
            return cell_list

        # if cell status is already opened or suspected mine it can not be opened??
        if (self.cell_status[row][column] == CellStatus.Opened) or \
            (self.cell_status[row][column] == CellStatus.MarkedAsMine):
            return cell_list

        #set the Cell Status to Opened and add it to CellList to be returned
        self.cell_status[row][column] = CellStatus.Opened
        cell_list.append([row, column])

        # Cache the Clicked cell here
        if len(cell_list) == 1:
            self.last_clicked_row = cell_list[0][0]
            self.last_clicked_column = cell_list[0][1]

        # if a cell is empty we should open all the 8 neighbours of the
        # clicked cell if they are not already open or marked as mine.
        # This rule applies recursively to neighbour cells if they are also empty.
        if self.cell_property[row][column] == CellProperty.Empty:
            if (row-1 >= 0) and (column-1 >= 0):
                cell_list.extend(self.opencell(row-1, column-1))
            if row-1 >= 0:
                cell_list.extend(self.opencell(row-1, column))
            if (row-1 >= 0) and (column+1 < self.columns):
                cell_list.extend(self.opencell(row-1, column+1))
            if column+1 < self.columns:
                cell_list.extend(self.opencell(row, column+1))
            if (row+1 < self.rows) and (column+1 < self.columns):
                cell_list.extend(self.opencell(row+1, column+1))
            if column-1 >= 0:
                cell_list.extend(self.opencell(row, column-1))
            if row+1 < self.rows:
                cell_list.extend(self.opencell(row+1, column))
            if (row+1 < self.rows) and (column-1 >= 0):
                cell_list.extend(self.opencell(row+1, column-1))
        return cell_list

    def setcellstatus(self, row, column, status):
        """
        This function sets the cell's status as per input argument.
        :param row: Row of the cell
        :param column: Column of the cell
        :param status: ::CellStatus enum value to be set
        :return: None
        """
        if (row < 0) or (row >= self.rows) or (column < 0) or (column >= self.columns):
            return CellStatus.UndefinedStatus

        # for MarkedAsMine cell the valid state is only MarkedAsSuspectedMine
        if self.cell_status[row][column] == CellStatus.MarkedAsMine:
            if status != CellStatus.MarkedAsSuspectedMine:
                return CellStatus.UndefinedStatus

        # for MarkedAsSuspectedMine cell the valid states are Open or close
        if self.cell_status[row][column] == CellStatus.MarkedAsSuspectedMine:
            if not((status == CellStatus.Closed) or (status == CellStatus.Opened)):
                return CellStatus.UndefinedStatus

        # if Status that going to set is MarkedAsMine then
        # the earlier state of cell should be Closed
        if status == CellStatus.MarkedAsMine:
            if self.cell_status[row][column] != CellStatus.Closed:
                return CellStatus.UndefinedStatus

        # set the New cell status
        self.cell_status[row][column] = status

        # increase or decrease current mine count based on New Set Status
        if status == CellStatus.MarkedAsMine:
            self.current_mine_count = self.current_mine_count - 1
        elif status == CellStatus.MarkedAsSuspectedMine:
            self.current_mine_count = self.current_mine_count + 1

        return status

    def getcellstatus(self, row, column):
        """
        This function returns the cell's status.
        :param row: Row of the cell
        :param column: Column of the cell
        :return: ::CellStatus enum value
        """
        if (row < 0) or (row >= self.rows) or (column < 0) or (column >= self.columns):
            return CellStatus.UndefinedStatus
        return self.cell_status[row][column]

    def getcellproperty(self, row, column):
        """
        This function returns the cell's property.
        :param row: Row of the cell
        :param column: Column of the cell
        :return: ::CellProperty enum value
        """
        if (row < 0) or (row >= self.rows) or (column < 0) or (column >= self.columns):
            return CellProperty.UndefinedProperty

        return self.cell_property[row][column]

    def continuegame(self):
        """
        This function returns GameStatus enum value as per the current status.
        :return: GameWon, GameNotComplete or GameLost
        """
        if (self.last_clicked_row == -1) and (self.last_clicked_column == -1):
            return GameStatus.GameNotComplete

        if self.cell_property[self.last_clicked_row][self.last_clicked_column] == CellProperty.Mine:
            return GameStatus.GameLost

        #print 'Remaining mine count:', self.current_mine_count
        for row in range(self.rows):
            for col in range(self.columns):
                if self.cell_property[row][col] == CellProperty.Mine:
                    continue
                if self.cell_status[row][col] == CellStatus.Closed:
                    return GameStatus.GameNotComplete

        return GameStatus.GameWon

    def reset(self):
        """
        This function resets the board to a fresh instance of game.
        :return: None
        """
        self.current_mine_count = self.total_mine_count
        self.last_clicked_row = -1
        self.last_clicked_column = -1
        self.createboard()
        return
