from aqt.qt import *
import aqt.forms
from anki.utils import versionWithBuild
from aqt.utils import supportText, tooltip
from anki.lang import _

class ClosableQDialog(QDialog):
    def reject(self):
        aqt.dialogs.markClosed("NewAbout")
        QDialog.reject(self)

    def accept(self):
        aqt.dialogs.markClosed("NewAbout")
        QDialog.accept(self)

    def closeWithCallback(self, callback):
        self.reject()
        callback()

def show(mw):
    dialog = ClosableQDialog(mw)
    mw.setupDialogGC(dialog)
    abt = aqt.forms.newabout.Ui_NewAbout()
    abt.setupUi(dialog)

    abouttext = """
    <center>
        <img src='/_anki/imgs/code1.jpg' height='200' width='200'>
        <img src='/_anki/imgs/code2.jpg' height='200' width='200'>
        <p>%s</p>
    </center>
"""
    content = '更多关于Diego爸爸, 请扫描以上二维码'
    # abouttext = "" 添加html格式文本即可
    abt.label.setMinimumWidth(600)
    abt.label.setMinimumHeight(400)
    dialog.show()
    abt.label.stdHtml(abouttext % content, js=" ")
    return dialog