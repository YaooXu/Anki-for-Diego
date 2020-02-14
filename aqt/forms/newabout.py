# -*- coding: utf-8 -*-
from anki.lang import _
from aqt.webview import AnkiWebView
# Form implementation generated from reading ui file 'designer\newabout.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewAbout(object):
    def setupUi(self, NewAbout):
        NewAbout.setObjectName("Dialog")
        NewAbout.resize(609, 490)
        self.pushButton = QtWidgets.QPushButton(NewAbout)
        self.pushButton.setGeometry(QtCore.QRect(530, 460, 75, 23))
        self.pushButton.setObjectName("pushButton")
        # self.label = QtWidgets.QLabel(Dialog)
        # self.label.setGeometry(QtCore.QRect(20, 20, 54, 12))
        self.label = AnkiWebView(NewAbout)
        self.label.setProperty("url", QtCore.QUrl("about:blank"))
        self.label.setObjectName("label")

        self.retranslateUi(NewAbout)
        self.pushButton.clicked.connect(NewAbout.accept)
        QtCore.QMetaObject.connectSlotsByName(NewAbout)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "OK"))
