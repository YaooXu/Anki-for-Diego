# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object,unused-import
from anki.lang import _
# Form implementation generated from reading ui file 'designer/smart_add.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SmartAdd(object):
    def setupUi(self, SmartAdd):
        SmartAdd.setObjectName("SmartAdd")
        SmartAdd.resize(415, 326)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("designer\\icons/anki.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SmartAdd.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(SmartAdd)
        self.groupBox.setGeometry(QtCore.QRect(270, 20, 141, 181))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.primary = QtWidgets.QRadioButton(self.groupBox)
        self.primary.setObjectName("primary")
        self.verticalLayout.addWidget(self.primary)
        self.middle = QtWidgets.QRadioButton(self.groupBox)
        self.middle.setObjectName("middle")
        self.verticalLayout.addWidget(self.middle)
        self.high = QtWidgets.QRadioButton(self.groupBox)
        self.high.setObjectName("high")
        self.verticalLayout.addWidget(self.high)
        self.cet4 = QtWidgets.QRadioButton(self.groupBox)
        self.cet4.setObjectName("cet4")
        self.verticalLayout.addWidget(self.cet4)
        self.cet6 = QtWidgets.QRadioButton(self.groupBox)
        self.cet6.setObjectName("cet6")
        self.verticalLayout.addWidget(self.cet6)
        self.file_choose_bt = QtWidgets.QPushButton(SmartAdd)
        self.file_choose_bt.setGeometry(QtCore.QRect(280, 210, 121, 41))
        self.file_choose_bt.setObjectName("file_choose_bt")
        self.smart_add_bt = QtWidgets.QPushButton(SmartAdd)
        self.smart_add_bt.setGeometry(QtCore.QRect(280, 270, 121, 41))
        self.smart_add_bt.setObjectName("smart_add_bt")
        self.textEdit = QtWidgets.QTextEdit(SmartAdd)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 251, 291))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(SmartAdd)
        QtCore.QMetaObject.connectSlotsByName(SmartAdd)

    def retranslateUi(self, SmartAdd):
        _translate = QtCore.QCoreApplication.translate
        SmartAdd.setWindowTitle(_("智能单词添加"))
        self.groupBox.setTitle(_("选择单词难度"))
        self.primary.setText(_("小学"))
        self.middle.setText(_("初中"))
        self.high.setText(_("高中"))
        self.cet4.setText(_("四级"))
        self.cet6.setText(_("六级"))
        self.file_choose_bt.setText(_("选择文本文件"))
        self.smart_add_bt.setText(_("智能添加单词"))
