from PyQt5 import QtWidgets
from window import Window
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
