# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object,unused-import
from anki.lang import _
# Form implementation generated from reading ui file 'designer/changemap.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChangeMap(object):
    def setupUi(self, ChangeMap):
        ChangeMap.setObjectName("ChangeMap")
        ChangeMap.resize(391, 360)
        self.vboxlayout = QtWidgets.QVBoxLayout(ChangeMap)
        self.vboxlayout.setObjectName("vboxlayout")
        self.label = QtWidgets.QLabel(ChangeMap)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)
        self.fields = QtWidgets.QListWidget(ChangeMap)
        self.fields.setObjectName("fields")
        self.vboxlayout.addWidget(self.fields)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChangeMap)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(ChangeMap)
        self.buttonBox.accepted.connect(ChangeMap.accept)
        self.buttonBox.rejected.connect(ChangeMap.reject)
        self.fields.doubleClicked['QModelIndex'].connect(ChangeMap.accept)
        QtCore.QMetaObject.connectSlotsByName(ChangeMap)

    def retranslateUi(self, ChangeMap):
        _translate = QtCore.QCoreApplication.translate
        ChangeMap.setWindowTitle(_("Import"))
        self.label.setText(_("Target field:"))
