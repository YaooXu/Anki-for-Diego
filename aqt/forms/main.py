# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object,unused-import
from anki.lang import _
# Form implementation generated from reading ui file 'designer/main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 650)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(400, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/anki.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 412, 22))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuCol = QtWidgets.QMenu(self.menubar)
        self.menuCol.setObjectName("menuCol")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setMenuRole(QtWidgets.QAction.AboutRole)
        self.actionAbout.setObjectName("actionAbout")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setEnabled(False)
        self.actionUndo.setObjectName("actionUndo")
        self.actionCheckMediaDatabase = QtWidgets.QAction(MainWindow)
        self.actionCheckMediaDatabase.setObjectName("actionCheckMediaDatabase")
        self.actionOpenPluginFolder = QtWidgets.QAction(MainWindow)
        self.actionOpenPluginFolder.setObjectName("actionOpenPluginFolder")
        self.actionDonate = QtWidgets.QAction(MainWindow)
        self.actionDonate.setObjectName("actionDonate")
        self.actionDownloadSharedPlugin = QtWidgets.QAction(MainWindow)
        self.actionDownloadSharedPlugin.setStatusTip("")
        self.actionDownloadSharedPlugin.setObjectName("actionDownloadSharedPlugin")
        self.actionFullDatabaseCheck = QtWidgets.QAction(MainWindow)
        self.actionFullDatabaseCheck.setObjectName("actionFullDatabaseCheck")
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionSwitchProfile = QtWidgets.QAction(MainWindow)
        self.actionSwitchProfile.setObjectName("actionSwitchProfile")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionStudyDeck = QtWidgets.QAction(MainWindow)
        self.actionStudyDeck.setObjectName("actionStudyDeck")
        self.actionEmptyCards = QtWidgets.QAction(MainWindow)
        self.actionEmptyCards.setObjectName("actionEmptyCards")
        self.actionCreateFiltered = QtWidgets.QAction(MainWindow)
        self.actionCreateFiltered.setObjectName("actionCreateFiltered")
        self.actionNoteTypes = QtWidgets.QAction(MainWindow)
        self.actionNoteTypes.setObjectName("actionNoteTypes")
        self.actionAdd_ons = QtWidgets.QAction(MainWindow)
        self.actionAdd_ons.setObjectName("actionAdd_ons")
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionDonate)
        self.menuHelp.addAction(self.actionAbout)
        self.menuEdit.addAction(self.actionUndo)
        self.menuCol.addAction(self.actionSwitchProfile)
        self.menuCol.addSeparator()
        self.menuCol.addAction(self.actionImport)
        self.menuCol.addAction(self.actionExport)
        self.menuCol.addSeparator()
        self.menuCol.addAction(self.actionExit)
        self.menuTools.addAction(self.actionStudyDeck)
        self.menuTools.addAction(self.actionCreateFiltered)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionFullDatabaseCheck)
        self.menuTools.addAction(self.actionCheckMediaDatabase)
        self.menuTools.addAction(self.actionEmptyCards)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionAdd_ons)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionNoteTypes)
        self.menuTools.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuCol.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_("Anki"))
        self.menuHelp.setTitle(_("&Help"))
        self.menuEdit.setTitle(_("&Edit"))
        self.menuCol.setTitle(_("&File"))
        self.menuTools.setTitle(_("&Tools"))
        self.actionExit.setText(_("E&xit"))
        self.actionExit.setShortcut(_("Ctrl+Q"))
        self.actionPreferences.setText(_("&Preferences..."))
        self.actionPreferences.setStatusTip(_("Configure interface language and options"))
        self.actionPreferences.setShortcut(_("Ctrl+P"))
        self.actionAbout.setText(_("&About..."))
        self.actionUndo.setText(_("&Undo"))
        self.actionUndo.setShortcut(_("Ctrl+Z"))
        self.actionCheckMediaDatabase.setText(_("Check &Media..."))
        self.actionCheckMediaDatabase.setStatusTip(_("Check the files in the media directory"))
        self.actionOpenPluginFolder.setText(_("&Open Add-ons Folder..."))
        self.actionDonate.setText(_("&Support Anki..."))
        self.actionDownloadSharedPlugin.setText(_("&Browse and Install..."))
        self.actionFullDatabaseCheck.setText(_("&Check Database"))
        self.actionDocumentation.setText(_("&Guide..."))
        self.actionDocumentation.setShortcut(_("F1"))
        self.actionSwitchProfile.setText(_("&Switch Profile"))
        self.actionSwitchProfile.setShortcut(_("Ctrl+Shift+P"))
        self.actionExport.setText(_("&Export..."))
        self.actionExport.setShortcut(_("Ctrl+E"))
        self.actionImport.setText(_("&Import..."))
        self.actionImport.setShortcut(_("Ctrl+Shift+I"))
        self.actionStudyDeck.setText(_("Study Deck..."))
        self.actionStudyDeck.setShortcut(_("/"))
        self.actionEmptyCards.setText(_("Empty Cards..."))
        self.actionCreateFiltered.setText(_("Create Filtered Deck..."))
        self.actionCreateFiltered.setShortcut(_("F"))
        self.actionNoteTypes.setText(_("Manage Note Types"))
        self.actionNoteTypes.setShortcut(_("Ctrl+Shift+N"))
        self.actionAdd_ons.setText(_("Add-ons"))
        self.actionAdd_ons.setShortcut(_("Ctrl+Shift+A"))
from . import icons_rc
