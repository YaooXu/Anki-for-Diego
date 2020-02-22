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
        <p>&nbsp;&nbsp;Diego爸爸，北京高校计算机博士，聋哑英语使用者。他在儿子Diego五岁的时候开始专注探索家庭儿童英语学习方法，历经八年研究，整合了现有的英语学习理论、工具和材料，提倡用技术重塑孩子的英语学习过程，提出“家庭是孩子英语学习的主战场”的观点并成功落地。</p>
        <p>&nbsp;&nbsp;Diego在爸爸的训练下，轻松自然地学习英语，在10岁时获得剑桥高级英语证书CAE，英语水平接近母语。10岁时独立参加清华大学线上英语课程《通用学术英语CAP》的学习，获得94分的优秀成绩。2019年11月作为儿童代表参加在德国柏林举办的第14届联合国互联网治理大会（IGF），用英文进行主旨发言并进行互动交流。</p>
        <p>&nbsp;&nbsp;2019年3月，Diego爸爸将多年实战经验写成一本科学、系统、易拷贝的《我带孩子学英语：英语小达人训练手册》，由机械工业出版社出版发行。本书一经出版，即获得家长广泛认可，成为万千家长的手头必备参考书。</p>
        <p>&nbsp;&nbsp;欢迎扫码关注Diego爸爸训练营微信公众号，获得更多帮助。
        <center>
            <img src='/_anki/imgs/code2.jpg' height='200' width='200'>
        </center>
        <p>&nbsp;&nbsp;扫码联系Diego爸爸，加入“Diego爸爸家长训练营”微信群，和全国万千关注孩子英语学习的家长一起互通有无，共同进步。</p>
        <center>
             <img src='/_anki/imgs/code1.jpg' height='200' width='200'>
        </center>
"""
    # abouttext = "" 添加html格式文本即可
    abt.label.setMinimumWidth(600)
    abt.label.setMinimumHeight(400)
    dialog.show()
    abt.label.stdHtml(abouttext, js=" ")
    return dialog
