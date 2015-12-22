__author__ = 'aiyer1'
"""
Main implementation file for Minesweeper
"""
import sys
import random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class BoardUI(QWidget):
    """
    This class implements the cell UI. Each cell is referenced by [row][col]
    """
    def __init__(self, rows=10, cols=10, parent=None):
        super(BoardUI, self).__init__(parent)
        self.rows = rows
        self.cols = cols
        self.cellSize = 25
        ButtonArray = [[QPushButton() for col in range(self.cols)] for row in range(self.rows)]

        CellGridLayout = QGridLayout()

        for row in range(self.rows):
            for col in range(self.cols):
                ButtonArray[row][col].setFixedSize(self.cellSize, self.cellSize)
                ButtonArray[row][col].setIcon(QIcon("icons/unopenedsquare.png"))
                ButtonArray[row][col].setIconSize(QSize(self.cellSize,self.cellSize))

                CellGridLayout.addWidget(ButtonArray[row][col], row, col)

        # Simulation for mock UI
        for row in range(self.rows):
            # Disable couple of buttons for demo to simulate empty cells
            col = random.choice(range(self.cols))
            ButtonArray[row][col].setIcon(QIcon())

            # Simulate mines
            col = random.choice(range(self.cols))
            ButtonArray[row][col].setIcon(QIcon("icons/mine.ico"))
            #button_array[x][y].setStyleSheet("background-color: grey")

            # Simulate mine flags
            col = random.choice(range(self.cols))
            ButtonArray[row][col].setIcon(QIcon("icons/Flag.png"))

            # Simulate suspected mine flags
            col = random.choice(range(self.cols))
            ButtonArray[row][col].setIcon(QIcon("icons/questionmark.png"))

        CellGridLayout.setSpacing(0)


        StatusWidgetsLayout = QHBoxLayout()

        Mines = QLCDNumber(3)
        Mines.setSegmentStyle(QLCDNumber.Flat)
        Mines.setStyleSheet("background-color:black; color:red")
        StatusWidgetsLayout.addWidget(Mines)

        StatusWidgetsLayout.addStretch()

        statusBtn = QPushButton()
        statusBtn.setFixedSize(50,50)
        statusBtn.setIcon(QIcon("icons/smiley1.ico"))
        #statusBtn.setIconSize(QSize(50,50))
        statusBtn.setIconSize(statusBtn.sizeHint())
        StatusWidgetsLayout.addWidget(statusBtn)

        StatusWidgetsLayout.addStretch()

        Time = QLCDNumber(3)
        Time.setSegmentStyle(QLCDNumber.Flat)
        Time.setStyleSheet("background-color:black; color:red")
        StatusWidgetsLayout.addWidget(Time)

        MainLayout = QVBoxLayout()
        MainLayout.addLayout(StatusWidgetsLayout)
        MainLayout.addLayout(CellGridLayout)

        self.setLayout(MainLayout)

class GameUI(QMainWindow):
    def __init__(self, rows=10, cols=10, parent=None):
        super(GameUI, self).__init__(parent)

        self.rows = rows
        self.cols = cols

        # prevent resize of main window
        self.setFixedSize(self.sizeHint())

        # prevent reaction to maximize button
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        MainWidget = BoardUI(self.rows, self.cols, self)

        StatusBar = self.statusBar()
        StatusBar.showMessage("Ready")
        # remove resizing grip from the main window
        StatusBar.setSizeGripEnabled(False)

        self.setCentralWidget(MainWidget)
        self.setWindowTitle("Minesweeper")
        self.show()

def main():
    app = QApplication(sys.argv)
    w = GameUI(10, 20)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



