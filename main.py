import sys

from PyQt5.QtWidgets import QApplication

from game.shidoku_board import ShidokuBoard

if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = ShidokuBoard()
    sys.exit(app.exec_())

