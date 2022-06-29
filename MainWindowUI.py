# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'MainWindow.ui'
##
# Created by: Qt User Interface Compiler version 5.15.2
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(1920, 1080)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.Text1_Detected = QLabel(self.centralwidget)
        self.Text1_Detected.setObjectName(u"Text1_Detected")
        self.Text1_Detected.setGeometry(QRect(690, 650, 140, 50))
        self.Text1_Detected.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setPointSize(21)
        self.Text1_Detected.setFont(font)
        self.Text2_3DModel = QLabel(self.centralwidget)
        self.Text2_3DModel.setObjectName(u"Text2_3DModel")
        self.Text2_3DModel.setGeometry(QRect(40, 140, 531, 31))
        self.Text2_3DModel.setSizeIncrement(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(19)
        self.Text2_3DModel.setFont(font1)
        self.Text3_Instruction = QLabel(self.centralwidget)
        self.Text3_Instruction.setObjectName(u"Text3_Instruction")
        self.Text3_Instruction.setGeometry(QRect(300, 60, 1211, 61))
        self.Text3_Instruction.setSizeIncrement(QSize(0, 0))
        font2 = QFont()
        font2.setPointSize(32)
        self.Text3_Instruction.setFont(font2)
        self.Button_Check = QPushButton(self.centralwidget)
        self.Button_Check.setObjectName(u"Button_Check")
        self.Button_Check.setGeometry(QRect(980, 990, 270, 60))
        font3 = QFont()
        font3.setPointSize(24)
        self.Button_Check.setFont(font3)
        self.Button_Retry = QPushButton(self.centralwidget)
        self.Button_Retry.setObjectName(u"Button_Retry")
        self.Button_Retry.setGeometry(QRect(1295, 990, 270, 60))
        self.Button_Retry.setFont(font3)
        self.Button_Restart = QPushButton(self.centralwidget)
        self.Button_Restart.setObjectName(u"Button_Restart")
        self.Button_Restart.setGeometry(QRect(1610, 990, 270, 60))
        self.Button_Restart.setFont(font3)
        self.Label_ImgInput = QLabel(self.centralwidget)
        self.Label_ImgInput.setObjectName(u"Label_ImgInput")
        self.Label_ImgInput.setGeometry(QRect(980, 140, 900, 675))
        self.Label_ImgInput.setScaledContents(True)
        self.Label_DrawSticker = QLabel(self.centralwidget)
        self.Label_DrawSticker.setObjectName(u"Label_DrawSticker")
        self.Label_DrawSticker.setGeometry(QRect(710, 840, 200, 200))
        self.Label_DrawAllSticker = QLabel(self.centralwidget)
        self.Label_DrawAllSticker.setObjectName(u"Label_DrawAllSticker")
        self.Label_DrawAllSticker.setGeometry(QRect(180, 830, 292, 221))
        self.Text4_CountDown = QLabel(self.centralwidget)
        self.Text4_CountDown.setObjectName(u"Text4_CountDown")
        self.Text4_CountDown.setGeometry(QRect(1380, 427, 100, 100))
        font4 = QFont()
        font4.setPointSize(70)
        font4.setBold(True)
        font4.setWeight(75)
        self.Text4_CountDown.setFont(font4)
        self.Text0_Welcome = QLabel(self.centralwidget)
        self.Text0_Welcome.setObjectName(u"Text0_Welcome")
        self.Text0_Welcome.setGeometry(QRect(10, 250, 1901, 471))
        self.Text0_Welcome.setFont(font3)
        self.Text0_Welcome.setLayoutDirection(Qt.LeftToRight)
        self.Text0_Welcome.setAutoFillBackground(True)
        self.Text0_Welcome.setStyleSheet(u"")
        self.Text0_Welcome.setAlignment(Qt.AlignCenter)
        self.Text5_Resolution = QLabel(self.centralwidget)
        self.Text5_Resolution.setObjectName(u"Text5_Resolution")
        self.Text5_Resolution.setGeometry(QRect(980, 820, 411, 161))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Text5_Resolution.sizePolicy().hasHeightForWidth())
        self.Text5_Resolution.setSizePolicy(sizePolicy)
        font5 = QFont()
        font5.setPointSize(14)
        self.Text5_Resolution.setFont(font5)
        self.Text5_Resolution.setScaledContents(False)
        self.Text5_Resolution.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.Text5_Resolution.setWordWrap(True)
        self.Text6_CurStep = QLabel(self.centralwidget)
        self.Text6_CurStep.setObjectName(u"Text6_CurStep")
        self.Text6_CurStep.setGeometry(QRect(30, 80, 151, 41))
        font6 = QFont()
        font6.setPointSize(18)
        self.Text6_CurStep.setFont(font6)
        self.Text7_NextStep = QLabel(self.centralwidget)
        self.Text7_NextStep.setObjectName(u"Text7_NextStep")
        self.Text7_NextStep.setGeometry(QRect(1720, 80, 161, 41))
        self.Text7_NextStep.setFont(font6)
        self.Text9_Judge = QLabel(self.centralwidget)
        self.Text9_Judge.setObjectName(u"Text9_Judge")
        self.Text9_Judge.setGeometry(QRect(1290, 300, 281, 111))
        self.Text9_Judge.setFont(font3)
        self.Text9_Judge.setAlignment(Qt.AlignCenter)
        self.Text9_Judge.setWordWrap(True)
        self.Text10_Notification = QLabel(self.centralwidget)
        self.Text10_Notification.setObjectName(u"Text10_Notification")
        self.Text10_Notification.setGeometry(QRect(1410, 820, 470, 160))
        sizePolicy.setHeightForWidth(
            self.Text10_Notification.sizePolicy().hasHeightForWidth())
        self.Text10_Notification.setSizePolicy(sizePolicy)
        self.Text10_Notification.setFont(font5)
        self.Text10_Notification.setScaledContents(False)
        self.Text10_Notification.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.Text10_Notification.setWordWrap(True)
        self.Text8_2DCube = QLabel(self.centralwidget)
        self.Text8_2DCube.setObjectName(u"Text8_2DCube")
        self.Text8_2DCube.setGeometry(QRect(40, 820, 161, 41))
        self.Text8_2DCube.setFont(font6)
        self.Text11_DetectResult = QLabel(self.centralwidget)
        self.Text11_DetectResult.setObjectName(u"Text11_DetectResult")
        self.Text11_DetectResult.setGeometry(QRect(510, 820, 161, 41))
        self.Text11_DetectResult.setFont(font6)
        self.Label_DrawBackGround = QLabel(self.centralwidget)
        self.Label_DrawBackGround.setObjectName(u"Label_DrawBackGround")
        self.Label_DrawBackGround.setGeometry(QRect(40, 830, 900, 221))
        self.Text2_Video = QLabel(self.centralwidget)
        self.Text2_Video.setObjectName(u"Text2_Video")
        self.Text2_Video.setGeometry(QRect(980, 140, 121, 31))
        self.Text2_Video.setSizeIncrement(QSize(0, 0))
        self.Text2_Video.setFont(font6)
        self.Text12_NamePair = QLabel(self.centralwidget)
        self.Text12_NamePair.setObjectName(u"Text12_NamePair")
        self.Text12_NamePair.setGeometry(QRect(750, 660, 181, 151))
        self.Text12_NamePair.setFont(font5)
        self.Text13_CurLayer = QLabel(self.centralwidget)
        self.Text13_CurLayer.setObjectName(u"Text13_CurLayer")
        self.Text13_CurLayer.setGeometry(QRect(300, 0, 401, 41))
        font7 = QFont()
        font7.setPointSize(20)
        self.Text13_CurLayer.setFont(font7)
        self.Text14_CurFormula = QLabel(self.centralwidget)
        self.Text14_CurFormula.setObjectName(u"Text14_CurFormula")
        self.Text14_CurFormula.setGeometry(QRect(790, 0, 721, 41))
        self.Text14_CurFormula.setFont(font7)
        self.Button_Beginner = QPushButton(self.centralwidget)
        self.Button_Beginner.setObjectName(u"Button_Beginner")
        self.Button_Beginner.setGeometry(QRect(680, 490, 211, 61))
        self.Button_Beginner.setFont(font6)
        self.Button_Kociemba = QPushButton(self.centralwidget)
        self.Button_Kociemba.setObjectName(u"Button_Kociemba")
        self.Button_Kociemba.setGeometry(QRect(1000, 490, 211, 61))
        self.Button_Kociemba.setFont(font6)
        self.Text15_Chosemethod = QLabel(self.centralwidget)
        self.Text15_Chosemethod.setObjectName(u"Text15_Chosemethod")
        self.Text15_Chosemethod.setGeometry(QRect(10, 330, 1901, 241))
        self.Text15_Chosemethod.setFont(font3)
        self.Text15_Chosemethod.setLayoutDirection(Qt.LeftToRight)
        self.Text15_Chosemethod.setAutoFillBackground(True)
        self.Text15_Chosemethod.setStyleSheet(u"")
        self.Text15_Chosemethod.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.Text15_Chosemethod.setMargin(21)
        MainWindow.setCentralWidget(self.centralwidget)
        self.Label_DrawBackGround.raise_()
        self.Button_Check.raise_()
        self.Button_Retry.raise_()
        self.Button_Restart.raise_()
        self.Label_ImgInput.raise_()
        self.Label_DrawSticker.raise_()
        self.Label_DrawAllSticker.raise_()
        self.Text4_CountDown.raise_()
        self.Text1_Detected.raise_()
        self.Text3_Instruction.raise_()
        self.Text0_Welcome.raise_()
        self.Text5_Resolution.raise_()
        self.Text6_CurStep.raise_()
        self.Text7_NextStep.raise_()
        self.Text9_Judge.raise_()
        self.Text10_Notification.raise_()
        self.Text8_2DCube.raise_()
        self.Text11_DetectResult.raise_()
        self.Text2_3DModel.raise_()
        self.Text2_Video.raise_()
        self.Text12_NamePair.raise_()
        self.Text13_CurLayer.raise_()
        self.Text14_CurFormula.raise_()
        self.Text15_Chosemethod.raise_()
        self.Button_Kociemba.raise_()
        self.Button_Beginner.raise_()
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"Demo", None))
        self.Text1_Detected.setText(QCoreApplication.translate(
            "MainWindow", u"\u8bc6\u522b\u7ed3\u679c\uff1a", None))
        self.Text2_3DModel.setText(QCoreApplication.translate(
            "MainWindow", u"3D\u9b54\u65b9\uff1a\uff08\u5de6\u952e\u6309\u4f4f\u8fdb\u884c\u62d6\u62fd\u65cb\u8f6c\uff0c\u53cc\u51fb\u8fd8\u539f\uff09", None))
        self.Text3_Instruction.setText(QCoreApplication.translate(
            "MainWindow", u"\u63d0\u793a\u4fe1\u606f", None))
        self.Button_Check.setText(QCoreApplication.translate(
            "MainWindow", u"\u786e\u8ba4", None))
        self.Button_Retry.setText(QCoreApplication.translate(
            "MainWindow", u"\u91cd\u8bd5", None))
        self.Button_Restart.setText(QCoreApplication.translate(
            "MainWindow", u"\u91cd\u65b0\u5f00\u59cb", None))
        self.Label_ImgInput.setText("")
        self.Label_DrawSticker.setText(QCoreApplication.translate(
            "MainWindow", u"\u5f53\u524d\u8bc6\u522b\u7ed3\u679c\u663e\u793a", None))
        self.Label_DrawAllSticker.setText(QCoreApplication.translate(
            "MainWindow", u"\u7ed8\u52362D\u9b54\u65b9", None))
        self.Text4_CountDown.setText("")
        self.Text0_Welcome.setText(QCoreApplication.translate("MainWindow", u"\u6b22\u8fce\u4f7f\u7528\u9b54\u65b9\u6559\u5b66\u7cfb\u7edf\uff01\n"
                                                              "1.\u8bf7\u5728\u660e\u4eae\u7684\u81ea\u7136\u73af\u5883\u5149\u4e0b\u8bc6\u522b\u9b54\u65b9\n"
                                                              "2.\u8bf7\u786e\u4fdd\u6444\u50cf\u673a\u8fde\u63a5\u6b63\u786e\uff0c\u5e76\u5c06\u6444\u50cf\u673a\u5e73\u653e\u5728\u684c\u9762\u4e0a\uff0c\u955c\u5934\u671d\u5411\u6b63\u524d\u65b9\n"
                                                              "3.\u8bf7\u6ce8\u610f\u9605\u8bfb\u753b\u9762\u4e0a\u65b9\u7684\u6307\u793a\u63d0\u793a\n"
                                                              "4.\u5982\u679c\u8fd8\u539f\u8fc7\u7a0b\u4e2d\u53d1\u73b0\u81ea\u5df1\u8f6c\u9519\u4e86\u8bf7\u70b9\u51fb\u201c\u91cd\u65b0\u5f00\u59cb\u201d\u6309\u94ae\n"
                                                              "\n"
                                                              "\n"
                                                              "\u70b9\u51fb\u201c\u786e\u8ba4\u201d\u6309\u94ae\u5f00\u59cb\u8bc6\u522b\uff01", None))
        self.Text5_Resolution.setText("")
        self.Text6_CurStep.setText(QCoreApplication.translate(
            "MainWindow", u"\u5f53\u524d\u6b65\u9aa4\uff1a", None))
        self.Text7_NextStep.setText(QCoreApplication.translate(
            "MainWindow", u"\u4e0b\u4e00\u6b65\u9aa4\uff1a", None))
        self.Text9_Judge.setText(QCoreApplication.translate(
            "MainWindow", u"TextLabel", None))
        self.Text10_Notification.setText("")
        self.Text8_2DCube.setText(QCoreApplication.translate(
            "MainWindow", u"2D\u5c55\u5f00\u56fe\uff1a", None))
        self.Text11_DetectResult.setText(QCoreApplication.translate(
            "MainWindow", u"\u5f53\u524d\u8bc6\u522b\u7ed3\u679c\uff1a", None))
        self.Label_DrawBackGround.setText("")
        self.Text2_Video.setText(QCoreApplication.translate(
            "MainWindow", u"\u89c6\u9891\u753b\u9762\uff1a", None))
        self.Text12_NamePair.setText(QCoreApplication.translate("MainWindow", u"U-Up\uff08\u4e0a\uff0c\u9ec4\u8272\uff09\n"
                                                                "D-Down\uff08\u4e0b\uff0c\u767d\u8272\uff09\n"
                                                                "L-Left\uff08\u5de6\uff0c\u6a59\u8272\uff09\n"
                                                                "R-Right\uff08\u53f3\uff0c\u7ea2\u8272\uff09\n"
                                                                "F-Front\uff08\u524d\uff0c\u84dd\u8272\uff09\n"
                                                                "B-Back\uff08\u540e\uff0c\u7eff\u8272\uff09", None))
        self.Text13_CurLayer.setText(QCoreApplication.translate(
            "MainWindow", u"\u5f53\u524d\u6b63\u5728\u8fdb\u884c\uff1a", None))
        self.Text14_CurFormula.setText(QCoreApplication.translate(
            "MainWindow", u"\u4f7f\u7528\u7684\u8fd8\u539f\u516c\u5f0f\uff1a", None))
        self.Button_Beginner.setText(QCoreApplication.translate(
            "MainWindow", u"\u521d\u5b66\u8005\u6a21\u5f0f", None))
        self.Button_Kociemba.setText(QCoreApplication.translate(
            "MainWindow", u"\u5feb\u901f\u8fd8\u539f\u6a21\u5f0f", None))
        self.Text15_Chosemethod.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u8981\u4f7f\u7528\u7684\u8fd8\u539f\u65b9\u6cd5\uff1a\n"
                                                                   "\u521d\u5b66\u8005\u6a21\u5f0f\uff1a\u4f7f\u7528\u5c42\u5148\u6cd5\uff0c\u5957\u7528\u516c\u5f0f\u8fd8\u539f\n"
                                                                   "\u5feb\u901f\u8fd8\u539f\u6a21\u5f0f\uff1a\u4f7f\u7528\u8ba1\u7b97\u673a\u7b97\u6cd5\uff0c\u6700\u77ed\u6b65\u9aa4\u8fd8\u539f", None))
    # retranslateUi
