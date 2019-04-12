from PyQt5.QtWidgets import QWidget, QLineEdit


class ShidokuCell(QWidget):
    CELL_SIZE = 50
    CELL_MARGIN = 15

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.pos_x = self.x * self.CELL_SIZE + (self.x + 1) * self.CELL_MARGIN
        self.pos_y = self.y * self.CELL_SIZE + (self.y + 1) * self.CELL_MARGIN
        self.__init_ui()

    def __init_ui(self):
        cell = QLineEdit('cell_{x}_{y}'.format(x=self.x, y=self.y), self)
        cell.setGeometry(0, 0, self.CELL_SIZE, self.CELL_SIZE)
        self.setGeometry(self.pos_x, self.pos_y, self.CELL_SIZE, self.CELL_SIZE)
        self.show()
