"""
Main implementation file for Minesweeper
"""

import sys
import functools
import random

from PyQt4 import QtGui
from PyQt4.QtCore import QSize, Qt
from BoardEnums import GridSize, DifficultyLevel


class BoardUI(QtGui.QWidget):
    """
    This class implements the cell UI. Each cell is referenced by [row][col]
    """

    def __init__(self, rows=10, cols=10, parent=None):
        super(BoardUI, self).__init__(parent)
        self.rows = rows
        self.cols = cols
        self.cell_size = 25
        button_array = [[QtGui.QPushButton() \
                         for col in range(self.cols)] for row in range(self.rows)]

        cell_grid_layout = QtGui.QGridLayout()

        for row in range(self.rows):
            for col in range(self.cols):
                button_array[row][col].setFixedSize(self.cell_size, self.cell_size)
                button_array[row][col].setIcon(QtGui.QIcon("icons/unopenedsquare.png"))
                button_array[row][col].setIconSize(QSize(self.cell_size, self.cell_size))

                cell_grid_layout.addWidget(button_array[row][col], row, col)

        # Simulation for mock UI
        for row in range(self.rows):
            # Disable couple of buttons for demo to simulate empty cells
            col = random.choice(range(self.cols))
            button_array[row][col].setIcon(QtGui.QIcon())

            # Simulate mines
            col = random.choice(range(self.cols))
            button_array[row][col].setIcon(QtGui.QIcon("icons/mine.ico"))
            # button_array[x][y].setStyleSheet("background-color: grey")

            # Simulate mine flags
            col = random.choice(range(self.cols))
            button_array[row][col].setIcon(QtGui.QIcon("icons/Flag.png"))

            # Simulate suspected mine flags
            col = random.choice(range(self.cols))
            button_array[row][col].setIcon(QtGui.QIcon("icons/questionmark.png"))

        cell_grid_layout.setSpacing(0)

        status_widget_layout = QtGui.QHBoxLayout()

        mines_lcd = QtGui.QLCDNumber(3)
        mines_lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        mines_lcd.setStyleSheet("background-color:black; color:red")
        status_widget_layout.addWidget(mines_lcd)

        status_widget_layout.addStretch()

        status_button = QtGui.QPushButton()
        status_button.setFixedSize(50, 50)
        status_button.setIcon(QtGui.QIcon("icons/smiley1.ico"))
        # status_button.setIconSize(QSize(50, 50))
        status_button.setIconSize(status_button.sizeHint())
        status_widget_layout.addWidget(status_button)

        status_widget_layout.addStretch()

        time_lcd = QtGui.QLCDNumber(3)
        time_lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        time_lcd.setStyleSheet("background-color:black; color:red")
        status_widget_layout.addWidget(time_lcd)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(status_widget_layout)
        main_layout.addLayout(cell_grid_layout)

        self.setLayout(main_layout)


class GameUI(QtGui.QMainWindow):
    """
    This class defines the Main Window class for the game.
    This is responsible for menus, game board, status bars.
    """

    def __init__(self, rows, cols, parent=None):
        super(GameUI, self).__init__(parent)
        self.rows = rows
        self.cols = cols

        # prevent resize of main window
        self.setFixedSize(self.sizeHint())

        # prevent reaction to maximize button
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        main_widget = BoardUI(self.rows, self.cols, self)

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
        beginner_level_action.triggered.connect(functools.partial(self.change_game_level, 1))

        # File menu option to change difficulty level
        intermediate_level_action = QtGui.QAction(QtGui.QIcon(""), '&Intermediate', self)
        intermediate_level_action.setShortcut('Ctrl+I')
        intermediate_level_action.setStatusTip('Set difficulty level to "Intermediate" ')
        intermediate_level_action.triggered.connect(functools.partial(self.change_game_level, 2))

        # File menu option to change difficulty level
        expert_level_action = QtGui.QAction(QtGui.QIcon(""), '&Expert', self)
        expert_level_action.setShortcut('Ctrl+E')
        expert_level_action.setStatusTip('Set difficulty level to "Expert" ')
        expert_level_action.triggered.connect(functools.partial(self.change_game_level, 3))

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

        # File Menu option to save the score.
        # TODO : Change function call after Leaderboard implementation.
        save_score_action = QtGui.QAction(QtGui.QIcon(""), '&Save', self)
        save_score_action.setShortcut('Ctrl+S')
        save_score_action.setStatusTip('Save current game score')
        save_score_action.triggered.connect(QtGui.QApplication.quit)

        # File Menu option to view the score.
        # TODO : Change function call after Leaderboard implementation.
        view_leaderboard_action = QtGui.QAction(QtGui.QIcon(""), '&View Score', self)
        view_leaderboard_action.setShortcut('Ctrl+V')
        view_leaderboard_action.setStatusTip("View current game's leader board")
        view_leaderboard_action.triggered.connect(QtGui.QApplication.quit)

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
        file_menu.addAction(save_score_action)
        # Add seperator (visible line) before showing exit.
        file_menu.addSeparator().setText("Alignment")
        file_menu.addAction(exit_game_action)

        # Add actions (sub menus) for help menu.
        help_menu.addAction(about_game_action)
        help_menu.addAction(game_help_action)

    def change_game_level(self, level):
        """
            This function helps in changing game level
            When user clicks on change game level from File menu
            this function will change height and width of grid.
        """
        if level == DifficultyLevel.BeginnerLevel:
            grid_length = GridSize.BeginnerLength
            grid_width = GridSize.BeginnerWidth

        elif level == DifficultyLevel.IntermediateLevel:
            grid_length = GridSize.IntermediateLength
            grid_width = GridSize.IntermediateWidth

        elif level == DifficultyLevel.ExpertLevel:
            grid_length = GridSize.ExpertLength
            grid_width = GridSize.ExpertWidth
        self.close()
        self.__init__(grid_length, grid_width)


def main():
    """
    This is the main function.
    :return: None
    """
    app = QtGui.QApplication(sys.argv)
    GameUI(GridSize.BeginnerLength, GridSize.BeginnerWidth)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
