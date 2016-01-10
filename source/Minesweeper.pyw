"""
Main implementation file for Minesweeper
"""

import Game
import LeaderBoard

import sys
import functools
import os.path
import random

from PyQt4 import QtCore
from PyQt4 import QtGui

class GameLevel(object):
    """
    Class for managing the game level and game parameters
    """
    Beginner = 1
    Intermediate = 2
    Expert = 3

    # Dict format is Level: (rows, columns, mines)
    GameParamDict = {Beginner: (9, 9, 10), Intermediate:(16, 16, 40), Expert:(16, 30, 99)}
    
    settingsFile = "Minesweeper.ini"

    def __init__(self):
        self.currentLevel = GameLevel.Beginner

        if os.path.exists(GameLevel.settingsFile):
            file = open(GameLevel.settingsFile, "r")
            self.currentLevel = int(file.read())
            file.close()
        else:
            # If file doesn't exist, assume default level as beginner and start game.
            file = open(GameLevel.settingsFile, "w")            
            file.write(str(self.currentLevel))
            file.close()

    def getGameLevel(self):        
        """
        Returns the current difficulty level
        """
        return self.currentLevel

    def setGameLevel(self, level):
        """
        Sets the difficulty level
        """
        self.currentLevel = level
        file = open(GameLevel.settingsFile, "w")
        file.write(str(level))
        file.close()

    def getGameParams(self, level=None):
        """
        Returns the game params for the level from the game params dictionary
        If level is not specified, then returns the parameters for current level
        """
        if level == None:
            return GameLevel.GameParamDict[self.currentLevel]
        else:
            return GameLevel.GameParamDict[level]


def GenerateMineList(rows, columns, minecount):
    selectedMineNumbers = random.sample(range(rows * columns), minecount)
    mine_list = []
    for mineNumber in selectedMineNumbers:
        row = mineNumber // columns
        col = mineNumber % columns
        mine_list.append((row,col))
    
    return mine_list

class BoardWidget(QtGui.QWidget):
    """
    This class implements the cell UI. Each cell is referenced by [row][col]
    """

    def __init__(self, rows=10, cols=10, minecount=10, parent=None):
        super(BoardWidget, self).__init__(parent)
        self.rows = rows
        self.columns = cols
        self.minecount = minecount        
        self.parent = parent
        self.remainingminecount = self.minecount
        self.cell_size = 25
        self.button_array = [[QtGui.QPushButton() \
                         for col in range(self.columns)] for row in range(self.rows)]
        self.game_in_progress = True
        self.first_click = True
        self.timer = QtCore.QTimer()
        self.time = 0
        
        self.cell_grid_layout = QtGui.QGridLayout()
        

        for row in range(self.rows):
            for col in range(self.columns):
                self.button_array[row][col].setFixedSize(self.cell_size, self.cell_size)
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/unopenedsquare.png"))
                self.button_array[row][col].setIconSize(QtCore.QSize(self.cell_size,\
                                                                     self.cell_size))                
                leftClickLambda = lambda x=row, y=col : self.handleLeftClick (x,y)                
                self.connect(self.button_array[row][col], QtCore.SIGNAL('clicked()'), leftClickLambda)
                
                # 'v' is for chomping the QPoint argument.
                rightClickLambda = lambda v, x=row, y=col : self.handleRightClick (x,y)
                self.button_array[row][col].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.connect(self.button_array[row][col], QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), rightClickLambda)
                
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
        self.time_lcd.display(self.time)
        status_widget_layout.addWidget(self.time_lcd)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(status_widget_layout)
        main_layout.addLayout(self.cell_grid_layout)

        self.setLayout(main_layout)
        
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.timerHandler)

        self.mine_list = GenerateMineList(self.rows, self.columns, self.minecount)
        self.board = Game.Board(self.rows, self.columns, self.mine_list)

    def timerHandler(self):
        """
        This function updates the timer lcd
        :return: None
        """
        if self.time < 999:
            self.time += 1
            self.time_lcd.display(self.time)
        else:
            self.timer.stop()

    def resetgrid(self):
        """
        This function resets the grid for a fresh instance of game.
        :return: None
        """
        self.remainingminecount = self.minecount
        self.game_in_progress = True
        self.first_click = True
        self.timer.stop()
        
        for row in range(self.rows):
            for col in range(self.columns):                
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/unopenedsquare.png"))
                self.button_array[row][col].setIconSize(QtCore.QSize(self.cell_size,\
                                                                     self.cell_size))
                
        self.mines_lcd.display(str(self.remainingminecount))
        self.status_button.setIcon(QtGui.QIcon("icons/smiley1.ico"))
        self.time = 0
        self.time_lcd.display(self.time)

        
        self.mine_list = GenerateMineList(self.rows, self.columns, self.minecount)

        # Create a new board
        self.board = Game.Board(self.rows, self.columns, self.mine_list)

    def handleLeftClick(self, row, col):
        """
        This function handles the left click action on each of the grid cell.
        It will also handle the actions required
        :return: None
        """
        if not self.game_in_progress:
            return
        if self.first_click:
            self.first_click = False
            self.timer.start(1000)

        celllist = self.board.opencell(row, col)
        
        if celllist == []:
            return
        
        for cell in celllist:
            row = cell[0]
            col = cell[1]
            cell_property = self.board.getcellproperty(row, col)
            
            if cell_property == Game.CellProperty.Empty:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/OpenedSquare.png"))
            elif cell_property == Game.CellProperty.Mine:
                # Game over. expose all mines
                for minePos in self.mine_list:
                    row = minePos[0]
                    col = minePos[1]
                    self.button_array[row][col].setIcon(QtGui.QIcon("icons/mine.ico"))

                self.status_button.setIcon(QtGui.QIcon("icons/smiley3.ico"))
                self.game_in_progress = False
                self.timer.stop()
                return
            elif cell_property == Game.CellProperty.MineCountOne:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/1.png"))
            elif cell_property == Game.CellProperty.MineCountTwo:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/2.png"))
            elif cell_property == Game.CellProperty.MineCountThree:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/3.png"))
            elif cell_property == Game.CellProperty.MineCountFour:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/4.png"))
            elif cell_property == Game.CellProperty.MineCountFive:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/5.png"))
            elif cell_property == Game.CellProperty.MineCountSix:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/6.png"))
            elif cell_property == Game.CellProperty.MineCountSeven:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/7.png"))
            elif cell_property == Game.CellProperty.MineCountEight:
                self.button_array[row][col].setIcon(QtGui.QIcon("icons/8.png"))

        game_status = self.board.getGameStatus()
        
        if game_status == Game.GameStatus.Won:
            self.timer.stop()
            self.game_in_progress = False
            self.status_button.setIcon(QtGui.QIcon("icons/smiley.ico"))

            self.parent.postUserWinCallback(self.time)

    def handleRightClick(self, row, col):
        """
        This function handles the right click action on grid cell.
        :return: None
        """
        if not self.game_in_progress:
            return
        if self.first_click:
            self.first_click = False
            self.timer.start(1000)
        
        status = self.board.getcellstatus(row, col)
        if status == Game.CellStatus.Opened:
            return
        elif status == Game.CellStatus.Closed:
            self.remainingminecount = self.remainingminecount - 1
            self.mines_lcd.display(str(self.remainingminecount))
            self.board.setcellstatus(row, col, Game.CellStatus.MarkedAsMine)
            self.button_array[row][col].setIcon(QtGui.QIcon("icons/Flag.png"))
        elif status == Game.CellStatus.MarkedAsMine:
            self.remainingminecount = self.remainingminecount + 1
            self.mines_lcd.display(str(self.remainingminecount))
            self.board.setcellstatus(row, col, Game.CellStatus.MarkedAsSuspectedMine)
            self.button_array[row][col].setIcon(QtGui.QIcon("icons/questionmark.png"))
        elif status == Game.CellStatus.MarkedAsSuspectedMine:
            self.board.setcellstatus(row, col, Game.CellStatus.Closed)
            self.button_array[row][col].setIcon(QtGui.QIcon("icons/unopenedsquare.png"))

class MainWindow(QtGui.QMainWindow):
    """
    This class defines the Main Window class for the game.
    This is responsible for menus, game board, status bars.
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.gameLevel = GameLevel()
        self.leaderBoard = LeaderBoard.LeaderBoard()
        
        (rows, columns, minecount) = self.gameLevel.getGameParams()

        main_widget = BoardWidget(rows, columns, minecount, self)
        
        # prevent resize of main window
        self.setFixedSize(self.sizeHint())

        # prevent reaction to maximize button
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)               

        # Add menu bar
        self.add_menu_bar()
        
        status_bar = self.statusBar()
        status_bar.showMessage("Ready")

        # remove resizing grip from the main window
        status_bar.setSizeGripEnabled(False)

        self.setCentralWidget(main_widget)
        self.setWindowTitle("Minesweeper")
        self.show()

    def postUserWinCallback (self, time):
        """
        This function is called when the human player wins the game
        """
        player_name = QtGui.QInputDialog.getText(self, "Name Please !!",\
                                                         "Enter your name for leader board:")
        
        self.leaderBoard.insertnewscore(self.gameLevel.getGameLevel(), player_name[0], time)

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

    def showHelp(self):
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
        GameLevelStrDict = {GameLevel.Beginner: "Beginner Level",\
                            GameLevel.Intermediate: "Intermediate Level", \
                            GameLevel.Expert: "Expert Level"
                            }
        
        level = self.gameLevel.getGameLevel()
        top_scores = self.leaderBoard.gettopscorerslist(level)
        
        leaderboard = "Rank".ljust(10) + "Player Name".ljust(30) + "Score".ljust(10) + '\n'
        
        rank = 1
        for score in top_scores:
            score = str(rank).ljust(10) + score
            
            leaderboard = leaderboard + score
            rank = rank + 1
        QtGui.QMessageBox.about(self, "Leaderboard for " + GameLevelStrDict[level], leaderboard)

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
                                                GameLevel.Beginner))

        # File menu option to change difficulty level
        intermediate_level_action = QtGui.QAction(QtGui.QIcon(""), '&Intermediate', self)
        intermediate_level_action.setShortcut('Ctrl+I')
        intermediate_level_action.setStatusTip('Set difficulty level to "Intermediate" ')
        intermediate_level_action.triggered.connect(functools.partial(self.change_game_level,\
                                                    GameLevel.Intermediate))

        # File menu option to change difficulty level
        expert_level_action = QtGui.QAction(QtGui.QIcon(""), '&Expert', self)
        expert_level_action.setShortcut('Ctrl+E')
        expert_level_action.setStatusTip('Set difficulty level to "Expert" ')
        expert_level_action.triggered.connect(functools.partial(self.change_game_level,\
                                                GameLevel.Expert))

        # File menu option "About" which gives information about game
        about_game_action = QtGui.QAction(QtGui.QIcon(""), '&About', self)
        about_game_action.setShortcut('Ctrl+A')
        about_game_action.setStatusTip("Show Application's ABOUT box")
        about_game_action.triggered.connect(self.about)

        # File menu option "About" which gives information about game
        game_help_action = QtGui.QAction(QtGui.QIcon(""), '&Help', self)
        game_help_action.setShortcut('Ctrl+H')
        game_help_action.setStatusTip("Show game's help")
        game_help_action.triggered.connect(self.showHelp)

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
            this function will start a new game at the new level
        """
        if self.gameLevel.getGameLevel() != change_level:
            self.gameLevel.setGameLevel(change_level)
            self.close()
            self.__init__()

            
def main():
    """
    This is the main function.
    :return: None
    """
    app = QtGui.QApplication(sys.argv)

    MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
