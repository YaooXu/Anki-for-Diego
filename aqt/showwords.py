from PyQt5.QtWidgets import *
from aqt.forms import showwords
from aqt.qt import *
import aqt.forms
from aqt.utils import saveGeom, restoreGeom, showWarning, askUser, shortcut, \
    tooltip, openHelp, addCloseShortcut, downArrow

# Showwords 初始化接受一个wordlist参数 为要显示的单词
# 具体使用:
# new = Showwords(self.mw,wordlist)
# if new.exec_():
#    newwordlist = new.getwordlist()
# newwordlist 即为 用户 选过的单词
# 调用 exec_()后 会等待new窗口结束

class Showwords(QDialog):
    def __init__(self, mw , wordlist):
        QDialog.__init__(self, None, Qt.Window)
        mw.setupDialogGC(self)
        self.mw = mw
        self.f = ""
        self.newwordlist = wordlist
        self.form = showwords.Ui_Dialog()
        self.form.setupUi(self)
        # 设置connect
        self.form.listWidget.addItems(wordlist)
        self.form.listWidget.clicked.connect(self.check)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contextMenu = QMenu(self)
        self.actionA = self.contextMenu.addAction( u'删除')
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu.triggered[QAction].connect(self.remove)
        self.show()
    
    def check(self,index):
        r = index.row()
        self.f = r;

    def showContextMenu(self):
        #如果有选中项，则显示显示菜单
        items = self.form.listWidget.selectedIndexes()
        if items:
            self.f = items[0].row()
            self.contextMenu.show()
            self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    
    def remove(self,qAction):
        print(self.f)
        #self.form.listWidget.takeItem(self.f)#删除行(实际上是断开了与list的联系)
        #注意：removeItemWidget(self, QListWidgetItem)  # 移除一个Item，无返回值
        #注意：takeItem(self, int)  # 切断一个Item与List的联系，返回该Item
        self.form.listWidget.removeItemWidget(self.form.listWidget.takeItem(int(self.f)))  #删除
        # self.form.listWidget.removeItemWidget(self.form.listWidget.takeItem(self.form.listWidget.row(self.item)))
        count = self.form.listWidget.count()
        # 遍历listwidget中的内容
        self.newwordlist = []
        for i in range(count):
            self.newwordlist.append(self.form.listWidget.item(i).text())
        print(self.newwordlist)

    def getwordlist(self):
        return self.newwordlist