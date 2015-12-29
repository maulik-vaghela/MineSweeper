"""
Main implementation file for Minesweeper
"""

import sys
import random

from PyQt4 import QtCore
from PyQt4 import QtGui

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
                button_array[row][col].setIconSize(QtCore.QSize(self.cell_size, self.cell_size))

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

    def __init__(self, rows=10, cols=10, parent=None):
        super(GameUI, self).__init__(parent)

        self.rows = rows
        self.cols = cols

        # prevent resize of main window
        self.setFixedSize(self.sizeHint())

        # prevent reaction to maximize button
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)

        main_widget = BoardUI(self.rows, self.cols, self)

        status_bar = self.statusBar()
        status_bar.showMessage("Ready")
        # remove resizing grip from the main window
        status_bar.setSizeGripEnabled(False)

        self.setCentralWidget(main_widget)
        self.setWindowTitle("Minesweeper")
        self.show()

def main():
    """
    This is the main function.
    :return: None
    """
    app = QtGui.QApplication(sys.argv)
    game_ui = GameUI(10, 20)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
