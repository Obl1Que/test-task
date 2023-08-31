import os

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPainter, QColor, QPen
from coordinates import Coordinates
from viewer import Viewer
import cv2

class Window(QtWidgets.QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.curpath_1 = ""
        self.curpath_2 = ""
        self.imgc_1 = 0
        self.imgc_2 = 0
        self.imgpath_1 = ""
        self.imgpath_2 = ""
        self.img_1 = None
        self.img_2 = None
        self.img_1_dots = {}
        self.img_2_dots = {}

        self.view_1 = Viewer(self)
        self.view_2 = Viewer(self)
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 1280, 1024)

        self.btnOpen = QtWidgets.QToolButton(self)
        self.btnOpen.setText('Choose directory')
        self.btnOpen.clicked.connect(self.openDirectory)

        self.btnSetDelta = QtWidgets.QToolButton(self)
        self.btnSetDelta.setText('Set delta time')
        self.btnSetDelta.clicked.connect(self.setDeltaTime)

        self.btnSwhMode = QtWidgets.QToolButton(self)
        self.btnSwhMode.setText('Switch mode')
        self.btnSwhMode.clicked.connect(self.view_1.switchMode)
        self.btnSwhMode.clicked.connect(self.view_2.switchMode)

        self.btnReset = QtWidgets.QToolButton(self)
        self.btnReset.setText('Reset')
        self.btnReset.clicked.connect(self.reset)

        self.btnSave = QtWidgets.QToolButton(self)
        self.btnSave.setText('Save')
        self.btnSave.clicked.connect(self.save)

        self.now = QtWidgets.QLabel(self)
        self.last = QtWidgets.QLabel(self)
        self.cnt = QtWidgets.QLabel(self)
        self.delta_time_label = QtWidgets.QLabel(self)

        self.view_1.mousePressed.connect(self.addCoord)
        self.view_1.mouseMoved.connect(self.showNow)

        self.btnLast_1 = QtWidgets.QToolButton(self)
        self.btnLast_1.setText("<<")
        self.btnLast_1.setMinimumSize(100, 30)
        self.btnLast_1.clicked.connect(self.goImg)

        self.btnNext_1 = QtWidgets.QToolButton(self)
        self.btnNext_1.setText(">>")
        self.btnNext_1.setMinimumSize(100, 30)
        self.btnNext_1.clicked.connect(self.goImg)

        self.curImgC1Label = QtWidgets.QLabel(self)
        self.curImgC1Label.setText(f"Image counter: {self.imgc_1}")

        self.view_2.mousePressed.connect(self.addCoord)
        self.view_2.mouseMoved.connect(self.showNow)

        self.btnLast_2 = QtWidgets.QToolButton(self)
        self.btnLast_2.setText("<<")
        self.btnLast_2.setMinimumSize(100, 30)
        self.btnLast_2.clicked.connect(self.goImg)


        self.btnNext_2 = QtWidgets.QToolButton(self)
        self.btnNext_2.setText(">>")
        self.btnNext_2.setMinimumSize(100, 30)
        self.btnNext_2.clicked.connect(self.goImg)

        self.curImgC2Label = QtWidgets.QLabel(self)
        self.curImgC2Label.setText(f"Image counter: {self.imgc_2}")

        btnsLayout = QtWidgets.QHBoxLayout()
        btnsLayout.setAlignment(QtCore.Qt.AlignLeft)
        btnsLayout.addWidget(self.btnOpen)
        btnsLayout.addWidget(self.btnSetDelta)
        btnsLayout.addWidget(self.btnSwhMode)
        btnsLayout.addWidget(self.btnReset)
        btnsLayout.addWidget(self.btnSave)

        lblsLayout = QtWidgets.QHBoxLayout()
        lblsLayout.setAlignment(QtCore.Qt.AlignLeft)
        lblsLayout.addWidget(self.now)
        lblsLayout.addWidget(self.last)
        lblsLayout.addWidget(self.cnt)
        lblsLayout.addWidget(self.delta_time_label)

        lnntns1Layout = QtWidgets.QHBoxLayout()
        lnntns1Layout.setAlignment(QtCore.Qt.AlignCenter)
        lnntns1Layout.addWidget(self.btnLast_1)
        lnntns1Layout.addWidget(self.btnNext_1)

        lnntns2Layout = QtWidgets.QHBoxLayout()
        lnntns2Layout.setAlignment(QtCore.Qt.AlignCenter)
        lnntns2Layout.addWidget(self.btnLast_2)
        lnntns2Layout.addWidget(self.btnNext_2)

        vbLayout = QtWidgets.QVBoxLayout(self)
        vbLayout.addLayout(btnsLayout)
        vbLayout.addWidget(self.view_1)
        vbLayout.addWidget(self.curImgC1Label)
        vbLayout.addLayout(lnntns1Layout)
        vbLayout.addWidget(self.view_2)
        vbLayout.addWidget(self.curImgC2Label)
        vbLayout.addLayout(lnntns2Layout)
        vbLayout.addLayout(lblsLayout)

        self.reset()
        self.show()

    def openDirectory(self):
        self.reset()
        dirname = QFileDialog.getExistingDirectory(self, "Choose directory", ".")

        self.setCurPaths(dirname)
        self.setFirstImg()

    def reset(self):
        self.coords = Coordinates()
        self.now.setText('Now: -, -')
        self.last.setText('Last: -, -')
        self.cnt.setText('Cnt: 0')
        self.delta_time_label.setText('Delta time: -')

    def save(self):
        self.coords.save()
        self.reset()

    def addCoord(self, pos):
        sender = self.sender()

        if self.view_1.dragMode() == QtWidgets.QGraphicsView.NoDrag or self.view_2.dragMode() == QtWidgets.QGraphicsView.NoDrag:
            x = pos.x() * 100 // 10 / 10
            y = pos.y() * 100 // 10 / 10
            self.coords.add(x, y)
            self.addPoint(int(x), int(y), sender)
            self.last.setText('Last: %.1f, %.1f' % (x, y))
            self.cnt.setText('Cnt: %d' % (self.coords.getSize()))

    def showNow(self, pos):
        x = pos.x() * 100 // 10 / 10
        y = pos.y() * 100 // 10 / 10
        self.now.setText('Now: %.1f, %.1f' % (x, y))

    def setCurPaths(self, dirname):
        self.curpath_1 = os.path.join(dirname, os.listdir(dirname)[0])
        self.curpath_2 = os.path.join(dirname, os.listdir(dirname)[1])

    def setFirstImg(self):
        self.imgc_1 = 0
        self.imgc_2 = 0

        self.imgpath_1 = os.path.join(self.curpath_1, os.listdir(self.curpath_1)[self.imgc_1])
        self.imgpath_2 = os.path.join(self.curpath_2, os.listdir(self.curpath_2)[self.imgc_2])

        self.img_1 = QtGui.QPixmap(self.imgpath_1)
        self.img_2 = QtGui.QPixmap(self.imgpath_2)

        self.view_1.setImage(self.img_1)
        self.view_2.setImage(self.img_2)

    def goImg(self):
        sender = self.sender()

        if self.imgpath_1 or self.imgpath_2:
            if sender == self.btnNext_1:
                self.imgc_1 += 1

                try:
                    self.imgpath_1 = os.path.join(self.curpath_1, os.listdir(self.curpath_1)[self.imgc_1])
                    self.img_1 = QtGui.QPixmap(self.imgpath_1)
                    self.view_1.setImage(self.img_1)
                except:
                    self.imgc_1 -= 1
            elif sender == self.btnNext_2:
                self.imgc_2 += 1

                try:
                    self.imgpath_2 = os.path.join(self.curpath_2, os.listdir(self.curpath_2)[self.imgc_2])
                    self.img_2 = QtGui.QPixmap(self.imgpath_2)
                    self.view_2.setImage(self.img_2)
                except:
                    self.imgc_2 -= 1
            elif sender == self.btnLast_1:
                if self.imgc_1 > 0:
                    self.imgc_1 -= 1

                try:
                    self.imgpath_1 = os.path.join(self.curpath_1, os.listdir(self.curpath_1)[self.imgc_1])
                    self.img_1 = QtGui.QPixmap(self.imgpath_1)
                    self.view_1.setImage(self.img_1)
                except:
                    self.imgc_1 += 1

            elif sender == self.btnLast_2:
                if self.imgc_2 > 0:
                    self.imgc_2 -= 1

                try:
                    self.imgpath_2 = os.path.join(self.curpath_2, os.listdir(self.curpath_2)[self.imgc_2])
                    self.img_2 = QtGui.QPixmap(self.imgpath_2)
                    self.view_2.setImage(QtGui.QPixmap(self.img_2))
                except:
                    self.imgc_2 += 1
            self.view_1.setSwitchMode()
            self.view_2.setSwitchMode()
            self.curImgC1Label.setText(f"Image counter: {self.imgc_1}")
            self.curImgC2Label.setText(f"Image counter: {self.imgc_2}")
        
    def setDeltaTime(self):
        self.delta_time = self.imgc_1 - self.imgc_2
        self.delta_time_label.setText(f'Delta time: {self.delta_time}')

    def addPoint(self, x: int, y: int, sender):
        try:
            if sender == self.view_1:
                paint = self.img_1
                img_filename = os.listdir(self.curpath_1)[self.imgc_1]

                if img_filename not in self.img_1_dots:
                    self.img_1_dots[img_filename] = []

                self.img_1_dots[img_filename].append((x, y))
            else:
                paint = self.img_2
                img_filename = os.listdir(self.curpath_2)[self.imgc_2]

                if img_filename not in self.img_2_dots:
                    self.img_2_dots[img_filename] = []

                self.img_2_dots[img_filename].append((x, y))

            painter = QPainter(paint)
            pen = QPen(QColor(255, 0, 0))
            painter.setPen(pen)

            painter.drawEllipse(x - 2, y - 2, 4, 4)
            painter.end()
            sender.updateImage(paint)

            print(self.img_1_dots)
            print(self.img_2_dots)
        except Exception as ex:
            print(ex)