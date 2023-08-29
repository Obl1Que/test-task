from PyQt5 import QtCore, QtGui, QtWidgets
from coordinates import Coordinates
from viewer import Viewer

class Window(QtWidgets.QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.view = Viewer(self)
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 900, 600)

        self.btnOpen = QtWidgets.QToolButton(self)
        self.btnOpen.setText('Open image')
        self.btnOpen.clicked.connect(self.openImage)

        self.btnSwhMode = QtWidgets.QToolButton(self)
        self.btnSwhMode.setText('Switch mode')
        self.btnSwhMode.clicked.connect(self.view.switchMode)

        self.btnReset = QtWidgets.QToolButton(self)
        self.btnReset.setText('Reset')
        self.btnReset.clicked.connect(self.reset)

        self.btnSave = QtWidgets.QToolButton(self)
        self.btnSave.setText('Save')
        self.btnSave.clicked.connect(self.save)

        self.now = QtWidgets.QLabel(self)
        self.last = QtWidgets.QLabel(self)
        self.cnt = QtWidgets.QLabel(self)

        self.view.mousePressed.connect(self.addCoord)
        self.view.mouseMoved.connect(self.showNow)

        btnsLayout = QtWidgets.QHBoxLayout()
        btnsLayout.setAlignment(QtCore.Qt.AlignLeft)
        btnsLayout.addWidget(self.btnOpen)
        btnsLayout.addWidget(self.btnSwhMode)
        btnsLayout.addWidget(self.btnReset)
        btnsLayout.addWidget(self.btnSave)

        lblsLayout = QtWidgets.QHBoxLayout()
        lblsLayout.setAlignment(QtCore.Qt.AlignLeft)
        lblsLayout.addWidget(self.now)
        lblsLayout.addWidget(self.last)
        lblsLayout.addWidget(self.cnt)

        vbLayout = QtWidgets.QVBoxLayout(self)
        vbLayout.addLayout(btnsLayout)
        vbLayout.addWidget(self.view)
        vbLayout.addLayout(lblsLayout)

        self.reset()
        self.show()

    def openImage(self):
        self.reset()
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open image", None, "Image (*.png *.jpg)")[0]
        self.view.setImage(QtGui.QPixmap(fname))

    def reset(self):
        self.coords = Coordinates()
        self.now.setText('Now: -, -')
        self.last.setText('Last: -, -')
        self.cnt.setText('Cnt: 0')

    def save(self):
        self.coords.save()
        self.reset()

    def addCoord(self, pos):
        if self.view.dragMode() == QtWidgets.QGraphicsView.NoDrag:
            x = pos.x() * 100 // 10 / 10
            y = pos.y() * 100 // 10 / 10
            self.coords.add(x, y)
            self.last.setText('Last: %.1f, %.1f' % (x, y))
            self.cnt.setText('Cnt: %d' % (self.coords.getSize()))

    def showNow(self, pos):
        x = pos.x() * 100 // 10 / 10
        y = pos.y() * 100 // 10 / 10
        self.now.setText('Now: %.1f, %.1f' % (x, y))
