"""
Main implementation file for Minesweeper
"""

import sys
import functools
import os.path

from PyQt4 import QtCore
from PyQt4 import QtGui
import MineSweeperBoard
import LeaderBoard
from BoardEnums import GridSize, DifficultyLevel, CellStatus, CellProperty, GameStatus

CURRENT_GAME_LEVEL = 0

def get_grid_size(game_level):
    """
    This function will return Grid size of UI based on difficulty level.
    :rtype : Width and length of the UI
    """
    grid_length = 0
    grid_width = 0
    minecount = 0
    if game_level == DifficultyLevel.BeginnerLevel:
        grid_length = GridSize.BeginnerLength
        grid_width = GridSize.BeginnerWidth
        minecount = 10

    elif game_level == DifficultyLevel.IntermediateLevel:
        grid_length = GridSize.IntermediateLength
        grid_width = GridSize.IntermediateWidth
        minecount = 40

    elif game_level == DifficultyLevel.ExpertLevel:
        grid_length = GridSize.ExpertLength
        grid_width = GridSize.ExpertWidth
        minecount = 99

    return (grid_length, grid_width, minecount)


class BoardUI(QtGui.QWidget):
    """
    This class implements the cell UI. Each cell is referenced by [row][col]
    """

    def __init__(self, rows=10, cols=10, minecount=10, parent=None):
        super(BoardUI, self).__init__(parent)
        self.rows = rows
        self.cols = cols
        self.minecount = minecount
        self.remainingminecount = self.minecount
        self.cell_size = 25
        self.board = MineSweeperBoard.Board(self.rows, self.cols, self.minecount)
        self.button_array = [[QtGui.QPushButton() \
                         for col in range(self.cols)] for row in range(self.rows)]
        self.game_in_progress = True
        self.timer = QtCore.QTimer()
        self.cell_grid_layout = QtGui.QGridLayout()
        self.remainingtime = 999

        for row in range(self.rows):
            for col in range(self.cols):
                self.button_array[row][col].setFixedSize(self.cell_size, self.cell_size)
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/unopenedsquare.png"))
                self.button_array[row][col].setIconSize(QtCore.QSize(self.cell_size,\
                                                                     self.cell_size))
                self.button_array[row][col].clicked.connect(self.handle_left_click)
                self.button_array[row][col].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.button_array[row][col].customContextMenuRequested.connect(\
                    self.handle_right_click)
                self.cell_grid_layout.addWidget(self.button_array[row][col], row, col)

        self.cell_grid_layout.setSpacing(0)

        status_widget_layout = QtGui.QHBoxLayout()

        self.mines_lcd = QtGui.QLCDNumber(3)
        self.mines_lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.mines_lcd.setStyleSheet("background-color:black; color:red")
        self.mines_lcd.display(str(self.remainingminecount))
        status_widget_layout.addWidget(self.mines_lcd)

        status_widget_layout.addStretch()

        self.status_button = QtGui.QPushButton()
        self.status_button.setFixedSize(50, 50)
        self.status_button.setIcon(QtGui.QIcon("icons/smiley1.ico"))
        self.status_button.setIconSize(self.status_button.sizeHint())
        self.status_button.clicked.connect(self.resetgrid)
        status_widget_layout.addWidget(self.status_button)

        status_widget_layout.addStretch()

        self.time_lcd = QtGui.QLCDNumber(3)
        self.time_lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.time_lcd.setStyleSheet("background-color:black; color:red")
        self.time_lcd.display(self.remainingtime)
        status_widget_layout.addWidget(self.time_lcd)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(status_widget_layout)
        main_layout.addLayout(self.cell_grid_layout)

        self.setLayout(main_layout)
        self.timer.timeout.connect(self.timer_change)
        self.timer.start(1000)

    def timer_change(self):
        """
        This function updates the timer lcd
        :return: None
        """
        self.remainingtime -= 1
        self.time_lcd.display(self.remainingtime)

    def resetgrid(self):
        """
        This function resets the grid for a fresh instance of game.
        :return: None
        """
        self.remainingminecount = self.minecount
        self.board.reset()
        self.button_array = [[QtGui.QPushButton() \
                         for col in range(self.cols)] for row in range(self.rows)]
        self.game_in_progress = True
        for row in range(self.rows):
            for col in range(self.cols):
                self.button_array[row][col].setFixedSize(self.cell_size, self.cell_size)
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/unopenedsquare.png"))
                self.button_array[row][col].setIconSize(QtCore.QSize(self.cell_size,\
                                                                     self.cell_size))
                self.button_array[row][col].clicked.connect(self.handle_left_click)
                self.button_array[row][col].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.button_array[row][col].customContextMenuRequested.connect(\
                    self.handle_right_click)
                self.cell_grid_layout.addWidget(self.button_array[row][col], row, col)
        self.mines_lcd.display(str(self.remainingminecount))
        self.status_button.setIcon(QtGui.QIcon("icons/smiley1.ico"))
        self.remainingtime = 999;
        self.time_lcd.display(self.remainingtime)
        self.timer.start(1000)

    def handle_left_click(self):
        '''
        This function handles the left click action on each of the grid cell.
        It will also handle the actions required
        :return: None
        '''
        if not self.game_in_progress:
            return
        sender = self.sender()
        row = 0
        col = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.button_array[row][col] == sender:
                    break
            else:
                continue
            break
        print 'Received left click:', row, ',', col
        celllist = self.board.opencell(row, col)
        if celllist == []:
            return
        for cell in celllist:
            row = cell[0]
            col = cell[1]
            cell_property = self.board.getcellproperty(row, col)
            if cell_property == CellProperty.Empty:
                self.button_array[row][col].setIcon(QtGui.QIcon())
            elif cell_property == CellProperty.Mine:
                # Game over
                for row in range(self.rows):
                    for col in range(self.cols):
                        cell_property = self.board.getcellproperty(row, col)
                        if cell_property == CellProperty.Mine:
                            self.button_array[row][col].setIcon(QtGui.QIcon("icons/mine.ico"))
                self.status_button.setIcon(QtGui.QIcon("icons/smiley3.ico"))
                self.game_in_progress = False
                self.timer.stop()
                return
            elif cell_property == CellProperty.MineCountOne:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/1.png"))
            elif cell_property == CellProperty.MineCountTwo:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/2.png"))
            elif cell_property == CellProperty.MineCountThree:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/3.png"))
            elif cell_property == CellProperty.MineCountFour:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/4.png"))
            elif cell_property == CellProperty.MineCountFive:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/5.png"))
            elif cell_property == CellProperty.MineCountSix:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/6.png"))
            elif cell_property == CellProperty.MineCountSeven:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/7.png"))
            elif cell_property == CellProperty.MineCountEight:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/8.png"))

        game_status = self.board.continuegame()
        print 'Game Status:', game_status
        if game_status == GameStatus.GameWon:
            self.timer.stop()
            self.game_in_progress = False
            player_name = QtGui.QInputDialog.getText(self, "Name Please !!",\
                                                         "Enter your name for leader board:")
            # TODO: Replace 1 with the time taken by the end user.
            LeaderBoard.insertnewscore(CURRENT_GAME_LEVEL, player_name[0], 999 - self.remainingtime)
            self.status_button.setIcon(QtGui.QIcon("icons/smiley.ico"))
            print "You have won the game"

    def handle_right_click(self):
        """
        This function handles the right click action on grid cell.
        :return: None
        """
        if not self.game_in_progress:
            return
        sender = self.sender()
        row = 0
        col = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.button_array[row][col] == sender:
                    break
            else:
                continue
            break
        print 'Received right click:', row, ',', col
        status = self.board.getcellstatus(row, col)
        if status == CellStatus.Opened:
            return
        elif status == CellStatus.Closed:
            self.remainingminecount = self.remainingminecount - 1
            self.mines_lcd.display(str(self.remainingminecount))
            self.board.setcellstatus(row, col, CellStatus.MarkedAsMine)
            self.button_array[row][col].setIcon(QtGui.QIcon("icons/Flag.png"))
        elif status == CellStatus.MarkedAsMine:
            self.remainingminecount = self.remainingminecount + 1
            self.mines_lcd.display(str(self.remainingminecount))
            self.board.setcellstatus(row, col, CellStatus.MarkedAsSuspectedMine)
            self.button_array[row][col].setIcon(QtGui.QIcon("icons/questionmark.png"))
        elif status == CellStatus.MarkedAsSuspectedMine:
            self.board.setcellstatus(row, col, CellStatus.Closed)
            self.button_array[row][col].setIcon(QtGui.QIcon("icons/unopenedsquare.png"))

class GameUI(QtGui.QMainWindow):
    """
    This class defines the Main Window class for the game.
    This is responsible for menus, game board, status bars.
    """

    def __init__(self, rows, cols, minecount, parent=None):
        super(GameUI, self).__init__(parent)

        # prevent resize of main window
        self.setFixedSize(self.sizeHint())

        # prevent reaction to maximize button
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)

        main_widget = BoardUI(rows, cols, minecount, self)

        # Add menu bar
        self.add_menu_bar()
        status_bar = self.statusBar()

        status_bar.showMessage("Ready")
        # remove resizing grip from the main window
        status_bar.setSizeGripEnabled(False)

        self.setCentralWidget(main_widget)
        self.setWindowTitle("Minesweeper")
        self.show()

    def about(self):
        """
        This function displays information about game.
        This function just displays game version and basic info about game.
        :return: VOID
        """
        QtGui.QMessageBox.about(self, "About Menu",
                                "MineSweeper 1.0 \n"
                                "This is python implementation of famous Minesweeper Game \n\n"
                                "For Source code, check following link:\n"
                                "https://github.com/maulik-vaghela/MineSweeper\n\n"
                                "Enjoy the game :) \n")

    def game_help(self):
        """
        This function displays help about game
        This function will pop up message box to user
        It will display following contents:
        1. how to play game
        2. Hints and tips
        :return: VOID
        """
        QtGui.QMessageBox.about(self, "How to Play game",
                                "<b>How to Play</b><br>"
                                "The rules in Minesweeper are simple:<br><br>"
                                "<b>1.</b> Uncover a mine and that's end of game <br>"
                                "<b>2.</b> Uncover empty cell and "
                                "it opens surrounding empty cells too<br>"
                                "<b>3.</b> Uncover a number "
                                "and it tells you how many mines are hidden in"
                                "surrounding 8 cells.<br>"
                                "<b>4.</b> Use this information to "
                                "deduce which squares are safe to click.<br>"
                                "<b>5.</b> Uncover all cells and "
                                "mark cells with mine to win the game <br><br>"

                                "<b>Hints</b> <br>"
                                "<b>1.Mark as Mine </b> <br>"
                                "   If you suspect that cell as mine, "
                                "right click twice to put a question mark.<br>"
                                "<b>2.Study surrounding cells </b><br>"
                                "  Study all neighbour cells before opening any cell"
                                "to make sure whether its mine or not.<br><br>"
                                "Enjoy the game :) <br>")

    def showtopscores(self):
        """
        This function handles the event of user asking for leaderboard.
        :return: None
        """
        top_scores = LeaderBoard.gettopscorerslist(CURRENT_GAME_LEVEL)
        print top_scores
        level_string = ""
        if CURRENT_GAME_LEVEL == DifficultyLevel.ExpertLevel:
            level_string = "Expert level"
        elif CURRENT_GAME_LEVEL == DifficultyLevel.BeginnerLevel:
            level_string = "Beginner level"
        else:
            level_string = "Intermediate level"
        leaderboard = "Rank\tName\tScore\n"
        for score in top_scores:
            leaderboard = leaderboard + score
        QtGui.QMessageBox.about(self, "Leaderboard for " + level_string, leaderboard)

    def add_menu_bar(self):
        """
            This function will add menu bar to the GUI.
            First we'll define all the actions which are required inside menu.
            Then we'll create menu bar and add menu's and actions.
        """
        # File menu option to change difficulty level
        beginner_level_action = QtGui.QAction(QtGui.QIcon(""), '&Beginner', self)
        beginner_level_action.setShortcut('Ctrl+B')
        beginner_level_action.setStatusTip('Set difficulty level to "Beginner" ')
        beginner_level_action.triggered.connect(functools.partial(self.change_game_level,\
                                                DifficultyLevel.BeginnerLevel))

        # File menu option to change difficulty level
        intermediate_level_action = QtGui.QAction(QtGui.QIcon(""), '&Intermediate', self)
        intermediate_level_action.setShortcut('Ctrl+I')
        intermediate_level_action.setStatusTip('Set difficulty level to "Intermediate" ')
        intermediate_level_action.triggered.connect(functools.partial(self.change_game_level,\
                                                    DifficultyLevel.IntermediateLevel))

        # File menu option to change difficulty level
        expert_level_action = QtGui.QAction(QtGui.QIcon(""), '&Expert', self)
        expert_level_action.setShortcut('Ctrl+E')
        expert_level_action.setStatusTip('Set difficulty level to "Expert" ')
        expert_level_action.triggered.connect(functools.partial(self.change_game_level,\
                                                DifficultyLevel.ExpertLevel))

        # File menu option "About" which gives information about game
        about_game_action = QtGui.QAction(QtGui.QIcon(""), '&About', self)
        about_game_action.setShortcut('Ctrl+A')
        about_game_action.setStatusTip("Show Application's ABOUT box")
        about_game_action.triggered.connect(self.about)

        # File menu option "About" which gives information about game
        game_help_action = QtGui.QAction(QtGui.QIcon(""), '&Help', self)
        game_help_action.setShortcut('Ctrl+H')
        game_help_action.setStatusTip("Show game's help")
        game_help_action.triggered.connect(self.game_help)

        # File Menu option to view the score.
        view_leaderboard_action = QtGui.QAction(QtGui.QIcon(""), '&View Score', self)
        view_leaderboard_action.setShortcut('Ctrl+V')
        view_leaderboard_action.setStatusTip("View current game's leader board")
        view_leaderboard_action.triggered.connect(self.showtopscores)

        # File Menu option for exit the game.
        exit_game_action = QtGui.QAction(QtGui.QIcon("exit.png"), '&Exit', self)
        exit_game_action.setShortcut('Ctrl+Q')
        exit_game_action.setStatusTip('Exit application')
        exit_game_action.triggered.connect(QtGui.QApplication.quit)

        # create a menu bar and we need to add 2 menus
        # 1. File and 2. Help
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        help_menu = menubar.addMenu('&Help')

        # Inside File menu create a submenu to change gane level
        # This sub menu has 3 actions (3 levels to choose from)
        change_level_sub_menu = file_menu.addMenu('&Game Level')
        change_level_sub_menu.addAction(beginner_level_action)
        change_level_sub_menu.addAction(intermediate_level_action)
        change_level_sub_menu.addAction(expert_level_action)

        # Add other actions in file menu after game level.
        file_menu.addAction(view_leaderboard_action)

        # Add seperator (visible line) before showing exit.
        file_menu.addSeparator().setText("Alignment")
        file_menu.addAction(exit_game_action)

        # Add actions (sub menus) for help menu.
        help_menu.addAction(about_game_action)
        help_menu.addAction(game_help_action)

    def change_game_level(self, change_level):
        """
            This function helps in changing game level
            When user clicks on change game level from File menu
            this function will change height and width of grid.
        """
        global CURRENT_GAME_LEVEL
        file_object = open("Level.txt", "w")
        file_object.write(str(change_level))
        file_object.close()
        CURRENT_GAME_LEVEL = change_level

        if change_level == DifficultyLevel.BeginnerLevel:
            grid_length = GridSize.BeginnerLength
            grid_width = GridSize.BeginnerWidth
            minecount = 10

        elif change_level == DifficultyLevel.IntermediateLevel:
            grid_length = GridSize.IntermediateLength
            grid_width = GridSize.IntermediateWidth
            minecount = 40

        elif change_level == DifficultyLevel.ExpertLevel:
            grid_length = GridSize.ExpertLength
            grid_width = GridSize.ExpertWidth
            minecount = 99

        self.close()
        self.__init__(grid_length, grid_width, minecount)


def main():
    """
    This is the main function.
    :return: None
    """
    global CURRENT_GAME_LEVEL
    app = QtGui.QApplication(sys.argv)

    file_existence = os.path.exists("Level.txt")

    # If file exist read level from file to restore previous level.
    if file_existence is True:
        file_object = open("Level.txt", "r")
        level = int(file_object.read())
        file_object.close()
    # If file doesn't exist, assume default level as beginner and start game.
    else:
        file_object = open("Level.txt", "w")
        level = DifficultyLevel.BeginnerLevel
        file_object.write(str(level))
        file_object.close()

    # save current game level in global which can be used by others.
    CURRENT_GAME_LEVEL = level
    (length, width, minecount) = get_grid_size(level)

    GameUI(length, width, minecount)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
