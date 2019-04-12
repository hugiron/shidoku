from typing import Optional

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QCursor, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLineEdit


class ShidokuCell(QWidget):
    CELL_SIZE = 50
    CELL_MARGIN = 15

    cell = None

    def __init__(self, parent: QWidget, event_enter_number, x: int, y: int):
        super().__init__()
        self.__parent = parent
        self.__event_enter_number = event_enter_number
        self.type = 'user'
        self.x = x
        self.y = y
        self.pos_x = self.x * self.CELL_SIZE + (self.x + 1) * self.CELL_MARGIN
        self.pos_y = self.y * self.CELL_SIZE + (self.y + 1) * self.CELL_MARGIN
        self.__init_ui()

    def __init_ui(self) -> None:
        # Configure font
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)

        # Configure cell
        self.cell = QLineEdit(self.__parent)
        self.cell.setFont(font)
        self.cell.setCursor(QCursor(Qt.ArrowCursor))
        self.cell.setGeometry(self.pos_x, self.pos_y, self.CELL_SIZE, self.CELL_SIZE)
        self.default_style()

        # Configure validator
        reg_ex = QRegExp("[1-4]?")
        input_validator = QRegExpValidator(reg_ex, self.cell)
        self.cell.setValidator(input_validator)

        # Set handler
        self.cell.textChanged.connect(self.__event_enter_number)

    def default_style(self):
        self.cell.setStyleSheet('qproperty-alignment: "AlignCenter";')

    def success_style(self):
        self.cell.setStyleSheet('qproperty-alignment: "AlignCenter"; border: 2px solid green;')

    def invalid_style(self):
        self.cell.setStyleSheet('qproperty-alignment: "AlignCenter"; border: 2px solid red;')

    def change_border_color(self, color: str):
        self.cell.setStyle()

    def value(self, value: int = None) -> Optional[int]:
        if value is not None:
            if 1 <= value <= 4:
                self.cell.setText(str(value))
        value = self.cell.text()
        return int(value) if value else None

    def change_type(self, type: str):
        if type == 'source':
            self.cell.setReadOnly(True)
        else:
            self.cell.setReadOnly(False)
        self.type = type
