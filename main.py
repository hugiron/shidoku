import sys

from PyQt5.QtWidgets import QApplication

from game.shidoku_app import ShidokuApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = ShidokuApp()
    sys.exit(app.exec_())

