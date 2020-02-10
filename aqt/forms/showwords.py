# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\showwords.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(484, 654)
        Dialog.setWindowTitle("ChooseWords")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 590, 401, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.ReturnButtonHLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.ReturnButtonHLayout.setContentsMargins(0, 0, 0, 0)
        self.ReturnButtonHLayout.setObjectName("ReturnButtonHLayout")
        self.pushButton_ok = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.ReturnButtonHLayout.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.ReturnButtonHLayout.addWidget(self.pushButton_cancel)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 39, 441, 551))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.WordListHLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.WordListHLayout.setContentsMargins(0, 0, 0, 0)
        self.WordListHLayout.setObjectName("WordListHLayout")
        self.listWidget = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        self.listWidget.setObjectName("listWidget")
        self.WordListHLayout.addWidget(self.listWidget)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 191, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.pushButton_ok.clicked.connect(Dialog.accept)
        self.pushButton_cancel.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_ok.setText(_("确定"))
        self.pushButton_cancel.setText(_("取消"))
        self.label.setText(_("右键单击可以删除单词"))

