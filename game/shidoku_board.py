import os
from typing import Set, Tuple
import xml.etree.cElementTree as ET

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QFrame

from game.shidoku_cell import ShidokuCell
from game.shidoku_generator import generate


class ShidokuBoard(QWidget):
    BLOCK_CELLS = 2
    BOARD_CELLS = 4
    FILENAME = 'shidoku.xml'

    board = None
    board_size = None

    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
        self.__init_ui()

    def __init_ui(self):
        # Calc board size
        self.board_size = self.BOARD_CELLS * ShidokuCell.CELL_SIZE + (self.BOARD_CELLS + 1) * ShidokuCell.CELL_MARGIN

        # Initialize cells
        self.board = [[ShidokuCell(self.__parent, self.validate_event, x, y) for x in range(self.BOARD_CELLS)] for y in range(self.BOARD_CELLS)]

        # Initialize horizontal and vertical lines
        line_position = self.BLOCK_CELLS * (ShidokuCell.CELL_SIZE + ShidokuCell.CELL_MARGIN) + ShidokuCell.CELL_MARGIN // 2
        vertical_line = QFrame(self.__parent)
        vertical_line.setGeometry(QRect(line_position, 0, 2, self.board_size))
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        horizontal_line = QFrame(self.__parent)
        horizontal_line.setGeometry(QRect(0, line_position, self.board_size, 2))
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        if os.path.exists(self.FILENAME):
            self.fread()
        else:
            self.generate_new()

    def is_complete(self) -> bool:
        for y in range(self.BLOCK_CELLS):
            for x in range(self.BLOCK_CELLS):
                cell_value = self.board[y][x].value()
                if cell_value is None:
                    return False
        return True

    def validate_event(self, e):
        for y in range(self.BOARD_CELLS):
            for x in range(self.BOARD_CELLS):
                self.board[y][x].default_style()

        invalid_cells = self.validate_board()
        if invalid_cells:
            for y, x in invalid_cells:
                self.board[y][x].invalid_style()
        else:
            if self.is_complete():
                for y in range(self.BOARD_CELLS):
                    for x in range(self.BOARD_CELLS):
                        self.board[y][x].success_style()

        self.fsync()

    def validate_board(self) -> Set[Tuple[int, int]]:
        result = set()

        block_count = self.BOARD_CELLS // self.BLOCK_CELLS
        for x in range(block_count):
            for y in range(block_count):
                result |= self.__validate_block(x, y)

        for index in range(self.BOARD_CELLS):
            result |= self.__validate_horizontal_line(index)
            result |= self.__validate_vertical_line(index)

        return result

    def __validate_block(self, index_x, index_y) -> Set[Tuple[int, int]]:
        exists_nums = dict()
        for y in range(index_y * self.BLOCK_CELLS, (index_y + 1) * self.BLOCK_CELLS):
            for x in range(index_x * self.BLOCK_CELLS, (index_x + 1) * self.BLOCK_CELLS):
                cell_value = self.board[y][x].value()
                if cell_value is not None:
                    if cell_value not in exists_nums:
                        exists_nums[cell_value] = set()
                    exists_nums[cell_value].add((y, x))
        result = set()
        for num, indexes in exists_nums.items():
            if len(indexes) > 1:
                result |= indexes
        return result

    def __validate_horizontal_line(self, index_y) -> Set[Tuple[int, int]]:
        exists_nums = dict()
        for i in range(self.BOARD_CELLS):
            cell_value = self.board[index_y][i].value()
            if cell_value is not None:
                if cell_value not in exists_nums:
                    exists_nums[cell_value] = set()
                exists_nums[cell_value].add((index_y, i))
        result = set()
        for num, indexes in exists_nums.items():
            if len(indexes) > 1:
                result |= indexes
        return result

    def __validate_vertical_line(self, index_x) -> Set[Tuple[int, int]]:
        exists_nums = dict()
        for i in range(self.BOARD_CELLS):
            cell_value = self.board[i][index_x].value()
            if cell_value is not None:
                if cell_value not in exists_nums:
                    exists_nums[cell_value] = set()
                exists_nums[cell_value].add((i, index_x))
        result = set()
        for num, indexes in exists_nums.items():
            if len(indexes) > 1:
                result |= indexes
        return result

    def fsync(self):
        root = ET.Element('board')
        for y in range(self.BOARD_CELLS):
            for x in range(self.BOARD_CELLS):
                cell_value = self.board[y][x].value()
                cell_type = self.board[y][x].type
                if cell_value is not None:
                    ET.SubElement(root, "cell", y=str(y), x=str(x), type=cell_type).text = str(cell_value)
        tree = ET.ElementTree(root)
        tree.write(self.FILENAME)

    def fread(self):
        tree = ET.parse(self.FILENAME)
        root = tree.getroot()
        for cell in root:
            try:
                x = int(cell.get('x'))
                y = int(cell.get('y'))
                type = cell.get('type')
                value = int(cell.text)
                self.board[y][x].value(value)
                self.board[y][x].change_type(type)
            except:
                pass
        self.validate_event(None)

    def reset_board(self):
        for y in range(self.BOARD_CELLS):
            for x in range(self.BOARD_CELLS):
                self.board[y][x].cell.setText('')
                self.board[y][x].default_style()
                self.board[y][x].change_type('user')

    def generate_new(self):
        self.reset_board()
        grid = generate(self.BLOCK_CELLS)
        for y in range(self.BOARD_CELLS):
            for x in range(self.BOARD_CELLS):
                cell_value = grid[y][x]
                if cell_value != 0:
                    self.board[y][x].value(cell_value)
                    self.board[y][x].change_type('source')
        self.fsync()
