from PyQt5.QtWidgets import *
from aqt.forms import smart_add

from aqt.qt import *
import aqt.forms
from aqt.utils import saveGeom, restoreGeom, showWarning, askUser, shortcut, \
    tooltip, openHelp, addCloseShortcut, downArrow
from anki.sound import clearAudioQueue
from anki.hooks import addHook, remHook, runHook
from anki.utils import htmlToTextLine, isMac
import aqt.editor, aqt.modelchooser, aqt.deckchooser


class SmartAdd(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, None, Qt.Window)
        mw.setupDialogGC(self)
        self.mw = mw
        self.form = smart_add.Ui_SmartAdd()
        self.form.setupUi(self)
        self.show()
