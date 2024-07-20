import PyQt5
from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QKeyEvent, QFont, QResizeEvent
from M2048Core import *


class M2048Window(QMainWindow):
    def __init__(self):
        super().__init__()
        InitCards()
        central = QWidget(self)
        central.setGeometry(self.rect())
        self.setCentralWidget(central)
        self.box = Box(self.centralWidget(), size=12)

        hLayout = QHBoxLayout(central)
        hLayout.addWidget(self.box)

        self.Update()

    def keyPressEvent(self, ev: QKeyEvent):
        if ev.key() == Qt.Key_Escape:
            self.close()
        elif ev.key() == Qt.Key_Up:
            self.box.TryMove(Direction.Up)
        elif ev.key() == Qt.Key_Down:
            self.box.TryMove(Direction.Down)
        elif ev.key() == Qt.Key_Left:
            self.box.TryMove(Direction.Left)
        elif ev.key() == Qt.Key_Right:
            self.box.TryMove(Direction.Right)

        self.Update()

    def Update(self):
        self.box.Draw()

    def resizeEvent(self, event: QResizeEvent):
        self.Update()
