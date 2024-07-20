import PyQt5
import sys
from PyQt5.QtWidgets import QApplication
from M2048Window import M2048Window

app = QApplication(sys.argv)
window = M2048Window()
window.show()
sys.exit(app.exec_())

