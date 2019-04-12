from PyQt5.QtWidgets import QWidget, QPushButton

from game.shidoku_board import ShidokuBoard


class ShidokuApp(QWidget):
    board = None

    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        self.board = ShidokuBoard(self)

        new_game_button = QPushButton('New game', self)
        new_game_button.move(8, self.board.board_size)
        new_game_button.clicked.connect(self.button_click_new_game)

        self.setWindowTitle('Shidoku')
        self.setFixedSize(self.board.board_size, self.board.board_size + 40)

        self.show()

    def button_click_new_game(self):
        self.board.generate_new()
