import math

import PyQt5
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
import random as rd

Cards: dict[int, QPixmap] = {}


class Direction(int):
    Up = 0
    Left = 1
    Down = 2
    Right = 3


def RotateMatrixInv(mat: list[list[int]], times: int) -> list[list[int]]:
    m = mat.copy()
    for i in range(times):
        m = list(zip(*m))
        m.reverse()
    return [list(row) for row in m]


def RotateMatrix(mat: list[list[int]], times: int) -> list[list[int]]:
    m = mat.copy()
    for i in range(4 - times):
        m = list(zip(*m))
        m.reverse()
    return [list(row) for row in m]


def InitCards():
    values = [0]
    for i in range(1, 17):
        values.append(2 ** i)
    for value in values:
        Cards[value] = QPixmap(128, 128)
        Cards[value].fill(QColor(200, 200, 200))
        if value != 0:
            pt = QPainter(Cards[value])
            font = QFont()
            font.setPointSize(int(60 / math.ceil(math.log10(value))))
            pt.setFont(font)
            pt.drawText(Cards[value].rect(), Qt.AlignCenter, str(value))
            pt.end()


class Box(QLabel):
    def __init__(self, parent: QWidget, size: int = 4):
        super().__init__(parent)
        rd.seed(1145141919810)
        self._matrix: list[list[int]] = []
        self.setGeometry(
            0, 0,
            min(parent.height(), parent.width()),
            min(parent.height(), parent.width()))
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setAlignment(Qt.AlignCenter)
        for y in range(size):
            rowNum = []
            for x in range(size):
                rowNum.append(0)
            self._matrix.append(rowNum)
        pm = QPixmap(self.width(), self.height())
        pm.fill(QColor(255, 255, 255))
        self.setPixmap(pm)
        self.RandomGenerate(2)
        self.currentBiggest = 2

    def Draw(self):
        geometrySize = self.parent().size()
        self.setGeometry(
            0, 0,
            min(geometrySize.height(), geometrySize.width()),
            min(geometrySize.height(), geometrySize.width()))
        pm = QPixmap(self.width() - 20, self.height() - 20)
        pm.fill(QColor(255, 255, 255))
        pt = QPainter(pm)
        size = len(self._matrix)
        edgeRatio = 5
        cardRatio = 10
        geometrySizeUnit = pm.width() / (2 * edgeRatio + (cardRatio + 2) * size)
        cardSize = cardRatio * geometrySizeUnit
        cardSizeWithMargin = (cardRatio + 2) * geometrySizeUnit
        halfMargin = geometrySizeUnit
        edgeWidth = edgeRatio * geometrySizeUnit
        for y in range(size):
            for x in range(size):
                rect = QRectF(x * cardSizeWithMargin + edgeWidth, y * cardSizeWithMargin + edgeWidth,
                              cardSize, cardSize)
                pt.drawPixmap(rect, Cards[self._matrix[y][x]], QRectF(Cards[self._matrix[y][x]].rect()))
        pt.end()
        self.setPixmap(pm)

    def RandomGenerate(self, count, maxExp=1):
        empty_pos = [(x, y) for y, row in enumerate(self._matrix) for x, e in enumerate(row) if e == 0]
        maxExp = max(maxExp, 1)
        rand_poses = rd.choices(empty_pos, k=count)
        weights = [2 ** (-1 - i) for i in range(maxExp)]
        numbers = [2 ** (i + 1) for i in range(maxExp)]
        for rand_pos in rand_poses:
            self._matrix[rand_pos[1]][rand_pos[0]] = rd.choices(numbers, weights, k=1)[0]

    def TryMove(self, direction: Direction):
        moved = False

        # 旋转矩阵以统一操作
        self._matrix = RotateMatrix(self._matrix, direction)

        size = len(self._matrix)
        for x in range(size):
            container = []
            last = None
            for y in range(size):
                if 0 == self._matrix[y][x]:
                    if y < size - 1 and self._matrix[y + 1] != 0:
                        moved = True
                    continue
                if last is None or last != self._matrix[y][x]:
                    last = self._matrix[y][x]
                    container.append(last)
                else:
                    container[-1] *= 2
                    self.currentBiggest = max(self.currentBiggest, container[-1])
                    moved = True
                    last = None

            while len(container) != size:
                container.append(0)

            for y in range(size):
                self._matrix[y][x] = container[y]

        self._matrix = RotateMatrixInv(self._matrix, direction)

        if moved:
            self.RandomGenerate(1, int(math.log2(self.currentBiggest)) - 1)
