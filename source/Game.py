"""
This module implements the Board class for minesweeper implementation.
"""

class CellStatus(object):
    """
    CellState -
    0: Closed
    1: Opened
    2: Marked as mine
    3: Marked as suspected mine
    """
    Closed = 0
    Opened = 1
    MarkedAsMine = 2
    MarkedAsSuspectedMine = 3

    def __init__(self):
        pass

class CellProperty(object):
    """
    CellProperty -
    -1: Mine
    0: Empty
    1-8: AdjacentMineCount
    """
    Mine = -1
    Empty = 0
    MineCountOne = 1
    MineCountTwo = 2
    MineCountThree = 3
    MineCountFour = 4
    MineCountFive = 5
    MineCountSix = 6
    MineCountSeven = 7
    MineCountEight = 8

    def __init__(self):
        pass

class GameStatus(object):
    """
    GameStatus -
    0: GameLost (When user clicked cell is a mine)
    1: GameNotComplete
    2: GameWon (When user has marked all mines properly and opened all remaining cells)
    """
    Lost = 0
    InProgress = 1
    Won = 2

    def __init__(self):
        pass



class Board(object):
    """
    This is the core Board class as per the class diagram
    """
    def __init__(self, rows, columns, mine_list):
        """
        This is the constructor.
        :param rows: Grid rows
        :param columns: Grid columns
        :param mine_count: Mines to be placed
        :return: None
        """
        self.rows = rows
        self.columns = columns
        self.mine_list = mine_list
        self.total_mine_count = len(self.mine_list)
        self.current_mine_count = self.total_mine_count
        self.last_clicked_row = -1
        self.last_clicked_column = -1

        self.createboard()

    def createboard(self):
        """
        Initialize the Board status and property with Closed and Empty resp.
        :return: None
        """
        self.cell_status = [[CellStatus.Closed for col in range(self.columns)] for row in range(self.rows)]
        self.cell_property = [[CellProperty.Empty for col in range(self.columns)] for row in range(self.rows)]


        for minePos in self.mine_list:
            self.cell_property[minePos[0]][minePos[1]] = CellProperty.Mine

        # Update Adjacent Count in neighbouring cells of a cell which has mines
        for minePos in self.mine_list:
            row = minePos[0]
            column = minePos[1]
            if (row - 1 >= 0) and (column - 1 >= 0):
                if self.cell_property[row - 1][column - 1] != CellProperty.Mine:
                    self.cell_property[row - 1][column - 1] += 1
            if row - 1 >= 0:
                if self.cell_property[row - 1][column] != CellProperty.Mine:
                    self.cell_property[row - 1][column] += 1
            if (row - 1 >= 0) and (column + 1 < self.columns):
                if self.cell_property[row - 1][column + 1] != CellProperty.Mine:
                    self.cell_property[row - 1][column + 1] += 1
            if column + 1 < self.columns:
                if self.cell_property[row][column + 1] != CellProperty.Mine:
                    self.cell_property[row][column + 1] += 1
            if (row + 1 < self.rows) and (column + 1 < self.columns):
                if self.cell_property[row + 1][column + 1] != CellProperty.Mine:
                    self.cell_property[row + 1][column + 1] += 1
            if row + 1 < self.rows:
                if self.cell_property[row + 1][column] != CellProperty.Mine:
                    self.cell_property[row + 1][column] += 1
            if (row + 1 < self.rows) and (column - 1 >= 0):
                if self.cell_property[row + 1][column - 1] != CellProperty.Mine:
                    self.cell_property[row + 1][column - 1] += 1
            if column - 1 >= 0:
                if self.cell_property[row][column - 1] != CellProperty.Mine:
                    self.cell_property[row][column - 1] += 1
        return

    def opencell(self, row, column):
        """
        Open the input cell and return list of affected cells.
        :param row: Row of the cell
        :param column: Column of the cell
        :return: List of cells affected and to be updated
        """
        assert (row >= 0 and row <= self.rows and column >= 0 and column <= self.columns)

        cellList = []

        # if cell status is already opened or marked as mine or suspected mine,
        # ignore
        if (self.cell_status[row][column] == CellStatus.Opened) or \
            (self.cell_status[row][column] == CellStatus.MarkedAsMine) or \
            (self.cell_status[row][column] == CellStatus.MarkedAsSuspectedMine):
            return cellList

        #set the Cell Status to Opened and add it to CellList to be returned
        self.cell_status[row][column] = CellStatus.Opened
        cellList.append([row, column])

        # Cache the Clicked cell here
        if len(cellList) == 1:
            self.last_clicked_row = cellList[0][0]
            self.last_clicked_column = cellList[0][1]

        # if a cell is empty we should open all the 8 neighbours of the
        # clicked cell if they are not already open or marked as mine.
        # This rule applies recursively to neighbour cells if they are also
        # empty.
        if self.cell_property[row][column] == CellProperty.Empty:
            if (row - 1 >= 0) and (column - 1 >= 0):
                cellList.extend(self.opencell(row - 1, column - 1))
            if row - 1 >= 0:
                cellList.extend(self.opencell(row - 1, column))
            if (row - 1 >= 0) and (column + 1 < self.columns):
                cellList.extend(self.opencell(row - 1, column + 1))
            if column + 1 < self.columns:
                cellList.extend(self.opencell(row, column + 1))
            if (row + 1 < self.rows) and (column + 1 < self.columns):
                cellList.extend(self.opencell(row + 1, column + 1))
            if column - 1 >= 0:
                cellList.extend(self.opencell(row, column - 1))
            if row + 1 < self.rows:
                cellList.extend(self.opencell(row + 1, column))
            if (row + 1 < self.rows) and (column - 1 >= 0):
                cellList.extend(self.opencell(row + 1, column - 1))
        return cellList

    def setcellstatus(self, row, column, status):
        """
        This function sets the cell's status as per input argument.
        :param row: Row of the cell
        :param column: Column of the cell
        :param status: ::CellStatus enum value to be set
        :return: None
        """
        assert (row >= 0 and row <= self.rows and column >= 0 and column <= self.columns)

        # Only state transitions noted below are allowed.  Illegal state
        # transtion requests are ignored
        # MarkedAsMine -> MarkedAsSuspectedMine
        # MarkedAsSuspectedMine -> Closed
        # Closed -> [Opened, MarkedAsMine]

        if self.cell_status[row][column] == CellStatus.MarkedAsMine:
            if status == CellStatus.MarkedAsSuspectedMine:
                self.cell_status[row][column] = CellStatus.MarkedAsSuspectedMine
                self.current_mine_count = self.current_mine_count + 1
                return

        if self.cell_status[row][column] == CellStatus.MarkedAsSuspectedMine:
            if status == CellStatus.Closed:
                self.cell_status[row][column] = CellStatus.Closed
                return

        if self.cell_status[row][column] == CellStatus.Closed:
            if status == CellStatus.MarkedAsMine:
                self.cell_status[row][column] = CellStatus.MarkedAsMine
                self.current_mine_count = self.current_mine_count - 1
                return
            elif status == CellStatus.Opened:
                self.cell_status[row][column] = CellStatus.Opened
                return

    def getcellstatus(self, row, column):
        """
        This function returns the cell's status.
        :param row: Row of the cell
        :param column: Column of the cell
        :return: ::CellStatus enum value
        """
        assert (row >= 0 and row <= self.rows and column >= 0 and column <= self.columns)
        return self.cell_status[row][column]

    def getcellproperty(self, row, column):
        """
        This function returns the cell's property.
        :param row: Row of the cell
        :param column: Column of the cell
        :return: ::CellProperty enum value
        """
        assert (row >= 0 and row <= self.rows and column >= 0 and column <= self.columns)
        return self.cell_property[row][column]

    def getGameStatus(self):
        """
        This function returns GameStatus enum value as per the current status.
        :return: GameWon, GameNotComplete or GameLost
        """
        if (self.last_clicked_row == -1) and (self.last_clicked_column == -1):
            return GameStatus.InProgress

        if self.cell_property[self.last_clicked_row][self.last_clicked_column] == CellProperty.Mine:
            return GameStatus.Lost

        #print 'Remaining mine count:', self.current_mine_count
        for row in range(self.rows):
            for col in range(self.columns):
                if self.cell_property[row][col] == CellProperty.Mine:
                    continue
                if self.cell_status[row][col] == CellStatus.Closed:
                    return GameStatus.InProgress

        return GameStatus.Won
