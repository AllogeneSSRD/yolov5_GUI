# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'detect.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(648, 444)
        MainWindow.setMouseTracking(False)
        MainWindow.setTabletTracking(False)
        MainWindow.setWindowOpacity(1.000000000000000)
        self.chenge_model = QAction(MainWindow)
        self.chenge_model.setObjectName(u"chenge_model")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.input = QLabel(self.centralwidget)
        self.input.setObjectName(u"input")
        self.input.setGeometry(QRect(20, 30, 281, 281))
        font = QFont()
        font.setFamilies([u"\u971e\u9e5c\u6587\u6977"])
        font.setPointSize(12)
        font.setBold(False)
        self.input.setFont(font)
        self.input.setScaledContents(True)
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output = QLabel(self.centralwidget)
        self.output.setObjectName(u"output")
        self.output.setGeometry(QRect(340, 30, 281, 281))
        font1 = QFont()
        font1.setFamilies([u"\u971e\u9e5c\u6587\u6977"])
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setUnderline(False)
        self.output.setFont(font1)
        self.output.setScaledContents(True)
        self.output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(310, 10, 20, 311))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.image_detect = QPushButton(self.centralwidget)
        self.image_detect.setObjectName(u"image_detect")
        self.image_detect.setGeometry(QRect(95, 330, 131, 41))
        font2 = QFont()
        font2.setFamilies([u"\u971e\u9e5c\u6587\u6977"])
        font2.setPointSize(14)
        self.image_detect.setFont(font2)
        self.video_detect = QPushButton(self.centralwidget)
        self.video_detect.setObjectName(u"video_detect")
        self.video_detect.setGeometry(QRect(415, 330, 131, 41))
        font3 = QFont()
        font3.setFamilies([u"\u971e\u9e5c\u6587\u6977"])
        font3.setPointSize(14)
        font3.setBold(False)
        self.video_detect.setFont(font3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 648, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        # self.menu_3 = QMenu(self.menubar)
        # self.menu_3.setObjectName(u"menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        # self.menubar.addAction(self.menu_3.menuAction())
        self.menu.addAction(self.chenge_model)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.chenge_model.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u6539\u6a21\u578b", None))
        self.input.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u539f\u59cb\u56fe\u7247", None))
        self.output.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u68c0\u6d4b\u7ed3\u679c", None))
        self.image_detect.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u68c0\u6d4b", None))
        self.video_detect.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u68c0\u6d4b", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u9009\u9879", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        # self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u66f4\u6539\u6a21\u578b", None))
    # retranslateUi

