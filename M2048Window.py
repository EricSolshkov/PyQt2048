import math

import PyQt5
from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QKeyEvent, QFont, QResizeEvent
import random as rd

Cards: dict[int, QPixmap] = {}


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
        for y in range(size):
            rowNum = []
            for x in range(size):
                rowNum.append(0)
            self._matrix.append(rowNum)
        pm = QPixmap(self.width(), self.height())
        pm.fill(QColor(255, 255, 255))
        self.setPixmap(pm)
        self.RandomGenerate(2)

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

        rand_poses = rd.choices(empty_pos, k=count)
        for rand_pos in rand_poses:
            self._matrix[rand_pos[1]][rand_pos[0]] = 2 ** (rd.randint(1, maxExp))

    def TryMoveUp(self):
        moved = False
        size = len(self._matrix)
        for x in range(size):
            container = []
            last = None
            for y in range(size):
                if 0 == self._matrix[y][x]:
                    moved = True
                    continue
                if last is None or last != self._matrix[y][x]:
                    last = self._matrix[y][x]
                    container.append(last)
                else:
                    container[-1] *= 2
                    moved = True
                    last = None

            while len(container) != size:
                container.append(0)

            for y in range(size):
                self._matrix[y][x] = container[y]

        if moved:
            self.RandomGenerate(1)

    def TryMoveDown(self):
        moved = False
        size = len(self._matrix)
        for x in range(size):
            container = []
            last = None
            for y in range(size - 1, -1, -1):
                if 0 == self._matrix[y][x]:
                    moved = True
                    continue
                if last is None or last != self._matrix[y][x]:
                    last = self._matrix[y][x]
                    container.append(last)
                else:
                    container[-1] *= 2
                    moved = True
                    last = None

            while len(container) != size:
                container.append(0)

            for y in range(size):
                self._matrix[y][x] = container[-1 - y]

        if moved:
            self.RandomGenerate(1)

    def TryMoveLeft(self):
        moved = False
        size = len(self._matrix)
        for y in range(size):
            container = []
            last = None
            for x in range(size):
                if 0 == self._matrix[y][x]:
                    moved = True
                    continue
                if last is None or last != self._matrix[y][x]:
                    last = self._matrix[y][x]
                    container.append(last)
                else:
                    container[-1] *= 2
                    moved = True
                    last = None

            while len(container) != size:
                container.append(0)

            for x in range(size):
                self._matrix[y][x] = container[x]

        if moved:
            self.RandomGenerate(1)

    def TryMoveRight(self):
        moved = False
        size = len(self._matrix)
        for y in range(size):
            container = []
            last = None
            for x in range(size - 1, -1, -1):
                if 0 == self._matrix[y][x]:
                    moved = True
                    continue
                if last is None or last != self._matrix[y][x]:
                    last = self._matrix[y][x]
                    container.append(last)
                else:
                    container[-1] *= 2
                    moved = True
                    last = None

            while len(container) != size:
                container.append(0)

            for x in range(size):
                self._matrix[y][x] = container[-1 - x]

        if moved:
            self.RandomGenerate(1)


class M2048Window(QMainWindow):
    def __init__(self):
        super().__init__()
        InitCards()
        central = QWidget(self)
        central.setGeometry(self.rect())
        self.setCentralWidget(central)
        self.box = Box(self.centralWidget(), size=4)

        hLayout = QHBoxLayout(central)
        hLayout.addWidget(self.box)

        self.Update()

    def keyPressEvent(self, ev: QKeyEvent):
        if ev.key() == Qt.Key_Escape:
            self.close()
        elif ev.key() == Qt.Key_Up:
            self.box.TryMoveUp()
        elif ev.key() == Qt.Key_Down:
            self.box.TryMoveDown()
        elif ev.key() == Qt.Key_Left:
            self.box.TryMoveLeft()
        elif ev.key() == Qt.Key_Right:
            self.box.TryMoveRight()

        self.Update()

    def Update(self):
        self.box.Draw()

    def resizeEvent(self, event: QResizeEvent):
        self.Update()
